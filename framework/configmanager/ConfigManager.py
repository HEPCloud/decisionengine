import copy
import importlib
import os

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.tsort as tsort

MANDATORY_CHANNEL_KEYS = {"sources",
                          'logicengines', "transforms", "publishers"}
MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}


CONFIG_FILE_NAME = "decision_engine.conf"


class ConfigManager():

    def __init__(self, config_file_name=CONFIG_FILE_NAME):
        self.config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
        if not os.path.isdir(self.config_dir):
            raise Exception("Config dir '%s' not found" % self.config_dir)
        self.config_file = os.path.join(self.config_dir, config_file_name)
        if not os.path.isfile(self.config_file):
            raise Exception("Config file '%s' not found" % self.config_file)
        self.channel_config_dir = os.path.join(self.config_dir, "config.d")
        self.global_config = {}
        self.channels = {}
        self.config = {}
        self.logger = None
        self.last_update_time = 0.0

    def check_keys(self, channel_conf_dict):
        """
        check that channel config has mandatory keys
        :type data: :obj:`dict`
        """
        channel_keys = set(channel_conf_dict.keys())
        diff = MANDATORY_CHANNEL_KEYS - channel_keys
        if diff:
            raise RuntimeError(f"channel is missing one or more mandatory keys {list(diff)} ")
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

    def validate_channel(self, channel):
        """
        Validate channels
        :type channel: :obj:`dict`
        """
        self.check_keys(channel)
        """
        sources
        """
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

        """
        transforms
        """
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

        """
        graph contains pairs of modules and lists of modules that depends on
        this module, e.g.:
        { "A" : [B,C,D],
        "D" : [C,B] }
        """

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

        """
        sort modules using topological sort
        sorted_modules are transform modules in order of execution
        """
        sorted_modules, cyclic_modules = tsort.tsort(graph)

        if cyclic_modules:
            raise RuntimeError(f"cyclic dependency detected for modules {list(cyclic_modules)}")

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

    def reload(self):
        old_global_config = copy.deepcopy(self.global_config)
        old_config = copy.deepcopy(self.config)
        try:
            self.load()
        except Exception:
            self.global_config = copy.deepcopy(old_global_config)
            self.config = copy.deepcopy(old_config)
            raise RuntimeError

    def load(self):
        self.last_update_time = os.stat(self.config_file).st_mtime
        code = None
        try:
            with open(self.config_file, "r") as f:
                code = "self.global_config=" + "".join(f.readlines())
            if code:
                try:
                    exec(code)
                except Exception as msg:
                    raise RuntimeError(f"Configuration file {self.config_file} contains errors:\n{msg}")
            else:
                raise RuntimeError(f"Empty configuration file {self.config_file}")
        except Exception as msg:
            raise RuntimeError(f"Failed to read configuration file {self.config_file}\n{msg}")

        if not isinstance(self.global_config, dict):
            raise RuntimeError("The configuration file must be a Python dictionary.")

        if not self.logger:
            if 'logger' not in self.global_config:
                raise RuntimeError("No logger configuration has been specified.")
            try:
                logger_config = self.global_config['logger']
                de_logger.set_logging(log_file_name=logger_config['log_file'],
                                      max_file_size=logger_config['max_file_size'],
                                      max_backup_count=logger_config['max_backup_count'],
                                      log_level=logger_config.get('log_level', 'WARNING'))
                self.logger = de_logger.get_logger()
            except Exception as msg:
                raise RuntimeError(f"Failed to create log: {msg}")

        """
        load channels
        """

        for direntry in os.listdir(self.channel_config_dir):
            if not direntry.endswith(".conf"):
                continue
            name = direntry.split('.')[0]
            channel_conf = os.path.join(self.channel_config_dir, direntry)
            try:
                with open(os.path.abspath(channel_conf), "r") as f:
                    code = "self.channels[name]=" + "".join(f.readlines())
                    try:
                        exec(code)
                    except Exception as msg:
                        self.logger.error(f"Channel configuration file {channel_conf} \
                                            contains error {msg}, SKIPPING")
                        continue
            except Exception as msg:
                self.logger.error(f"Failed to open channel configuration file {channel_conf} \
                                  contains error {msg}, SKIPPING")

            """
            check that channel configuration contains necessary keys
            if keys are missing channel is removed and error is printed
            """
            try:
                self.validate_channel(self.channels[name])
            except Exception as msg:
                self.logger.error(f"{name} {msg}, REMOVING the channel")
                del self.channels[name]
                continue

    def is_updated(self):
        return

    def get_channels(self):
        return self.channels

    def get_global_config(self):
        return self.global_config

    """
    Factory method:  create instance of dynamically loaded module
    """
    @staticmethod
    def create(module_name, class_name, parameters):
        my_module = importlib.import_module(module_name)
        clazz = getattr(my_module, class_name)
        instance = clazz(parameters)
        return instance


if __name__ == "__main__":
    c = ConfigManager()
    c.load()
