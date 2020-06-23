import copy
import importlib
import os

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.tsort as tsort

MANDATORY_CHANNEL_KEYS = {"sources",
                          'logicengines', "transforms", "publishers"}
MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}


CONFIG_FILE_NAME = "decision_engine.conf"

def _verify_not_empty(config_file):
    if os.path.getsize(config_file) == 0:
        raise RuntimeError(f"Empty configuration file {config_file}")

def _config_from_file(config_file):
    _verify_not_empty(config_file)
    global_config = None
    try:
        with open(config_file) as f:
            try:
                global_config = eval(f.read())
            except Exception as msg:
                raise RuntimeError(f"Configuration file {config_file} contains errors:\n{msg}")
    except Exception as msg:
        raise RuntimeError(f"Failed to read configuration file {config_file}\n{msg}")

    if not isinstance(global_config, dict):
        raise RuntimeError("The configuration file must be a Python dictionary.")
    return global_config

def _make_logger(global_config):
    if 'logger' not in global_config:
        raise RuntimeError("No logger configuration has been specified.")
    try:
        logger_config = global_config['logger']
        de_logger.set_logging(log_file_name=logger_config['log_file'],
                              max_file_size=logger_config['max_file_size'],
                              max_backup_count=logger_config['max_backup_count'],
                              log_level=logger_config.get('log_level', 'WARNING'))
        return de_logger.get_logger()
    except Exception as msg:
        raise RuntimeError(f"Failed to create log: {msg}")

def _check_keys(channel_conf_dict):
    """
    check that channel config has mandatory keys
    :type data: :obj:`dict`
    """
    channel_keys = set(channel_conf_dict.keys())
    diff = MANDATORY_CHANNEL_KEYS - channel_keys
    if diff:
        missing = list(diff)
        raise RuntimeError(f"channel is missing one or more mandatory keys {missing}")
    for name in MANDATORY_CHANNEL_KEYS:
        conf = channel_conf_dict[name]
        for module_name, module_conf in conf.items():
            try:
                module_keys = set(module_conf.keys())
            except Exception as msg:
                raise RuntimeError(f"{name} module {module_name} is not a dictionary, {msg}")
            diff = MANDATORY_MODULE_KEYS - module_keys
            if diff:
                missing_keys = str(list(diff))
                raise RuntimeError(f"{name} module {module_name} is missing one or more mandatory keys {missing_keys} ")

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

    def __init__(self):
        self.config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
        if not os.path.isdir(self.config_dir):
            raise Exception(f"Config dir '{self.config_dir}' not found")
        self.channel_config_dir = os.getenv("CHANNEL_CONFIG_PATH",
                                            os.path.join(self.config_dir, "config.d"))
        if not os.path.isdir(self.channel_config_dir):
            raise Exception(f"Channel config dir '{self.channel_config_dir}' not found")
        self.global_config = {}
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

    def reload(self, config_file_name=CONFIG_FILE_NAME):
        old_global_config = copy.deepcopy(self.global_config)
        old_config = copy.deepcopy(self.config)
        try:
            self.load(config_file_name)
        except Exception:
            self.global_config = copy.deepcopy(old_global_config)
            self.config = copy.deepcopy(old_config)
            raise RuntimeError

    def load(self, config_file_name=CONFIG_FILE_NAME):
        config_file = os.path.join(self.config_dir, config_file_name)
        if not os.path.isfile(config_file):
            raise Exception(f"Config file '{config_file}' not found")
        self.last_update_time = os.stat(config_file).st_mtime
        self.global_config = _config_from_file(config_file)
        if not self.logger:
            self.logger = _make_logger(self.global_config)
        self._load_channels()

    def is_updated(self):
        return

    def get_channels(self):
        return self.channels

    def get_global_config(self):
        return self.global_config

    def _load_channels(self):
        for entry in os.scandir(self.channel_config_dir):
            name, path = entry.name, entry.path
            if not name.endswith(".conf"):
                continue
            _verify_not_empty(path)
            try:
                with open(path) as f:
                    try:
                        self.channels[name] = eval(f.read())
                    except Exception as msg:
                        self.logger.error(f"Channel configuration file {path} "
                                          f"contains error\n-> {msg}\nSKIPPING channel")
                        continue
            except Exception as msg:
                self.logger.error(f"Failed to open channel configuration file {path} "
                                  f"contains error\n-> {msg}\nSKIPPING channel")

            # Verify channel configuration contains necessary keys.
            # If keys are missing, the channel is removed and an error
            # message is logged.
            try:
                _validate_channel(self.channels[name])
            except Exception as msg:
                self.logger.error(f"{name} {msg}, REMOVING the channel")
                del self.channels[name]
                continue

    @staticmethod
    def create(module_name, class_name, parameters):
        """
        Factory method:  create instance of dynamically loaded module
        """
        my_module = importlib.import_module(module_name)
        clazz = getattr(my_module, class_name)
        instance = clazz(parameters)
        return instance


if __name__ == "__main__":
    c = ConfigManager()
    c.load()
