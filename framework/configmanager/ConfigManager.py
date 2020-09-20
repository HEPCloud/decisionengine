import copy
import importlib
import os
import _jsonnet
import json
import sys

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.tsort as tsort

_MANDATORY_CHANNEL_KEYS = {'sources', 'logicengines', 'transforms', 'publishers'}
_ALLOWED_CHANNEL_KEYS = _MANDATORY_CHANNEL_KEYS | {'task_manager'}
_MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}

_CONFIG_FILE_NAME = 'decision_engine.jsonnet'

def _convert_to_json(config_file):
    """
    Attempt to convert JSON non-compliant configuration into a compliant one.

    This is a temporary facility to aid the migration of Python-based
    configurations to Jsonnet-based ones.  Python dictionaries that
    are similar in structure to JSON documents are generally trivially
    convertible.
    """
    global_config = None
    try:
        with open(config_file) as f:
            try:
                global_config = eval(f.read())
            except Exception as msg:
                raise RuntimeError(f"Configuration file {config_file} contains errors:\n{msg}\n"
                                   "The supplied configuration must be a valid Jsonnet/JSON document.")
    except Exception as msg:
        raise RuntimeError(f"Failed to read configuration file {config_file}\n{msg}")

    if not isinstance(global_config, dict):
        raise RuntimeError("The supplied configuration must be a valid Jsonnet/JSON document.")

    json_config = None
    try:
        json_config = json.dumps(global_config)
    except Exception:
        raise RuntimeError("The supplied configuration is not convertible to a Jsonnet/JSON document.")

    print(f"The supplied configuration file {config_file} is not a valid Jsonnet/JSON document.\n"
          "It has been converted to a valid JSON construct, but it should be fixed.",
          file=sys.stderr)
    return json_config

def _config_from_file(config_file):
    if os.path.getsize(config_file) == 0:
        raise RuntimeError(f"Empty configuration file {config_file}")

    config_str = None
    basename, ext = os.path.splitext(config_file)
    try:
        config_str = _jsonnet.evaluate_file(config_file)
        if ext != '.jsonnet':
            print(f"Please rename '{config_file}' to '{basename}.jsonnet'.",
                  file=sys.stderr)
    except Exception:
        # Conversion allowed only for files that do not yet have a
        # '.jsonnet' extension.
        if ext != '.jsonnet':
            config_str = _convert_to_json(config_file)
        else:
            raise

    return json.loads(config_str)

def _make_logger(global_config):
    if 'logger' not in global_config:
        raise RuntimeError("No logger configuration has been specified.")
    try:
        logger_config = global_config['logger']
        de_logger.set_logging(log_level=logger_config.get('log_level', 'INFO'),
                              file_rotate_by=logger_config.get('file_rotate_by',"size"),
                              rotation_time_unit=logger_config.get('rotation_time_unit','D'),
                              rotation_interval=logger_config.get('rotation_time_interval',1),
                              max_backup_count=logger_config.get('max_backup_count',6),
                              max_file_size=logger_config['max_file_size'],
                              log_file_name=logger_config['log_file'])
        return de_logger.get_logger()
    except Exception as msg:
        raise RuntimeError(f"Failed to create log: {msg}")

def _check_keys(channel_conf_dict):
    """
    check that channel config has mandatory keys
    :type data: :obj:`dict`
    """
    channel_keys = set(channel_conf_dict.keys())
    diff = _MANDATORY_CHANNEL_KEYS - channel_keys
    if diff:
        missing = list(diff)
        raise RuntimeError(f"channel is missing one or more mandatory keys:\n{missing}")
    for name in _MANDATORY_CHANNEL_KEYS:
        conf = channel_conf_dict[name]
        for module_name, module_conf in conf.items():
            try:
                module_keys = set(module_conf.keys())
            except Exception as msg:
                raise RuntimeError(f"{name} module {module_name} is not a dictionary:\n{msg}")
            diff = _MANDATORY_MODULE_KEYS - module_keys
            if diff:
                missing_keys = str(list(diff))
                raise RuntimeError(f"{name} module {module_name} is missing one or more mandatory keys:\n{missing_keys} ")

def _validate_channel(channel):
    """
    Validate channels
    :type channel: :obj:`dict`
    """
    _check_keys(channel)

    # Sources
    sources = channel.get('sources')
    all_produces = set()
    for sname, conf in sources.items():
        my_module = importlib.import_module(conf.get('module'))
        try:
            produces = getattr(my_module, 'PRODUCES')
            all_produces |= set(produces)
        except AttributeError:
            raise RuntimeError(f"source module {sname} does not have required PRODUCES list")

    all_consumes = set()

    # Transforms
    transforms = channel.get('transforms')
    transform_map = {}

    for tname, conf in transforms.items():
        my_module = importlib.import_module(conf.get('module'))
        try:
            consumes = set(getattr(my_module, 'CONSUMES'))
            produces = set(getattr(my_module, 'PRODUCES'))
            all_consumes |= consumes
            all_produces |= produces
            transform_map[tname] = {'consumes': consumes,
                                    'produces': produces}
        except AttributeError as msg:
            raise RuntimeError(f"transform module {tname} does not have required lists {msg}")

    if not all_consumes.issubset(all_produces):
        extra_keys = list(all_consumes - all_produces)
        raise RuntimeError(f"consumes are not subset of produce, extra keys {extra_keys}")

    # graph contains pairs of modules and lists of modules that depends on
    # this module, e.g.:
    # { "A" : [B,C,D],
    # "D" : [C,B] }
    graph = {}
    for i in range(len(transform_map)):
        k1 = list(transform_map.keys())[i]
        c1 = set(transform_map[k1].get('consumes', []))
        p1 = set(transform_map[k1].get('produces', []))
        added = False
        for j in range(i + 1, len(transform_map)):
            k2 = list(transform_map.keys())[j]
            c2 = set(transform_map[k2].get('consumes', []))
            p2 = set(transform_map[k2].get('produces', []))
            if c2 & p1:
                added = True
                graph.setdefault(k1, []).append(k2)
            if p2 & c1:
                added = True
                graph.setdefault(k2, []).append(k1)
        if not added:
            graph.setdefault(k1, [])

    # sort modules using topological sort
    # sorted_modules are transform modules in order of execution
    sorted_modules, cyclic_modules = tsort.tsort(graph)

    if cyclic_modules:
        raise RuntimeError(f"cyclic dependency detected for modules {list(cyclic_modules)}")


class ConfigManager():

    def __init__(self, program_options=None):
        self.config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
        if not os.path.isdir(self.config_dir):
            raise Exception(f"Config dir '{self.config_dir}' not found")
        self.channel_config_dir = os.getenv("CHANNEL_CONFIG_PATH",
                                            os.path.join(self.config_dir, "config.d"))
        if not os.path.isdir(self.channel_config_dir):
            raise Exception(f"Channel config dir '{self.channel_config_dir}' not found")
        self.program_options = program_options
        self.global_config = None
        self.channels = {}
        self.config = {}
        self.logger = None
        self.last_update_time = 0.0

    def get_produces(self, channel_config):
        produces = {}
        for i in ('sources', 'transforms'):
            modules = channel_config.get(i, {})
            for name, conf in modules.items():
                my_module = importlib.import_module(conf.get('module'))
                try:
                    produces.setdefault(name, []).extend(
                        getattr(my_module, 'PRODUCES'))
                except AttributeError:
                    pass
        return produces

    def reload(self, config_file_name=None):
        old_global_config = copy.deepcopy(self.global_config)
        old_config = copy.deepcopy(self.config)
        try:
            self.load(config_file_name)
        except Exception:
            self.global_config = copy.deepcopy(old_global_config)
            self.config = copy.deepcopy(old_config)
            raise RuntimeError

    def load(self, config_file_name=None):
        if not config_file_name:
            config_file_name = _CONFIG_FILE_NAME
        config_file = os.path.join(self.config_dir, config_file_name)
        if not os.path.isfile(config_file):
            raise Exception(f"Config file '{config_file}' not found")
        self.last_update_time = os.stat(config_file).st_mtime
        self.global_config = _config_from_file(config_file)
        # If present, the configuration as specified via program
        # options takes precedence.
        if self.program_options:
            self.global_config.update(self.program_options)
        if not self.logger:
            self.logger = _make_logger(self.global_config)
        self._load_channels()

    def is_updated(self):
        return

    def get_channels(self):
        return self.channels

    def get_global_config(self):
        return self.global_config

    def print_channel_config(self, channel):
        return json.dumps(self.channels[channel], sort_keys=True, indent=2)

    def print_global_config(self):
        return json.dumps(self.get_global_config(), sort_keys=True, indent=2)

    def _load_channels(self):
        for entry in os.scandir(self.channel_config_dir):
            name, path = entry.name, entry.path
            basename, ext = os.path.splitext(name)
            if ext not in {'.conf', '.jsonnet'}:
                continue
            try:
                self.channels[basename] = _config_from_file(path)
            except Exception as msg:
                self.logger.error(f"Failed to open channel configuration file {path} "
                                  f"contains error\n-> {msg}\nSKIPPING channel")
                continue

            # Verify channel configuration contains necessary keys.
            # If keys are missing, the channel is removed and an error
            # message is logged.
            try:
                _validate_channel(self.channels[basename])
            except Exception as msg:
                self.logger.error(f"{name}\n{msg}\nREMOVING the channel")
                del self.channels[basename]
                continue

    @staticmethod
    def create(module_name, class_name, parameters):
        """
        Factory method:  create instance of dynamically loaded module
        """
        my_module = importlib.import_module(module_name)
        class_type = getattr(my_module, class_name)
        return class_type(parameters)


if __name__ == "__main__":
    c = ConfigManager()
    c.load()
