import copy
import importlib
import os
import string

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.tsort as tsort

MANDATORY_CHANNEL_KEYS = {"sources", 'logicengines', "transforms", "publishers"}
MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}


CONFIG_FILE_NAME = "decision_engine.conf"


class ConfigManager(object):

    def __init__(self):
        self.config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
        if not os.path.isdir(self.config_dir):
            raise Exception("Config dir '%s' not found" % self.config_dir)
        self.config_file = os.path.join(self.config_dir, CONFIG_FILE_NAME)
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
            raise RuntimeError("channel is missing one or more mandatory keys {} ".
                               format(list(diff)))
        for name in MANDATORY_CHANNEL_KEYS:
            conf = channel_conf_dict[name]
            for module_name, module_conf in conf.items():
                try:
                    module_keys = set(module_conf.keys())
                except Exception as msg:
                    raise RuntimeError("{} module {} is not a dictionary, {}".
                                       format(name, module_name, str(msg)))
                diff = MANDATORY_MODULE_KEYS - module_keys
                if diff:
                    raise RuntimeError("{} module {} is missing one or more mandatory keys {} ".
                                       format(name, module_name, str(list(diff))))

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
            except AttributeError as msg:
                raise RuntimeError("source module {} does not have required PRODUCES list".
                                   format(sname))

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
                raise RuntimeError("transform module {} does not have required lists {}".
                                   format(tname, str(msg)))

        if not all_consumes.issubset(all_produces):
            raise RuntimeError("consumes are not subset of produce, extra keys {}".
                               format(list(all_consumes-all_produces)))

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
            raise RuntimeError("cyclic dependency detected for modules {}".
                               format(list(cyclic_modules)))

    def get_produces(self, channel_config):
        produces = {}
        for i in ('sources', 'transforms'):
            modules = channel_config.get(i, {})
            for name, conf in modules.items():
                my_module = importlib.import_module(conf.get('module'))
                try:
                    produces.setdefault(name, []).extend(getattr(my_module, 'PRODUCES'))
                except:
                    pass
        return produces

    def reload(self):
        old_global_config = copy.deepcopy(self.global_config)
        old_config = copy.deepcopy(self.config)
        try:
            self.load()
        except:
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
                    raise RuntimeError("Configuration file {} contains errors: {}".
                                       format(self.config_file, str(msg)))
            else:
                raise RuntimeError("Empty configuration file {}".format(self.config_file))
        except Exception as msg:
            raise RuntimeError("Failed to read configuration file {} {}".
                               format(self.config_file, str(msg)))

        if not self.logger:
            try:
                de_logger.set_logging(log_file_name=self.global_config['logger']['log_file'],
                                      max_file_size=self.global_config['logger']['max_file_size'],
                                      max_backup_count=self.global_config['logger']['max_backup_count'])
                self.logger = de_logger.get_logger()
            except Exception as msg:
                raise RuntimeError("Failed to create log: {}".format(str(msg)))


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
                        self.logger.error("Channel configuration file {} \
                                           contains error {}, SKIPPING".
                                          format(channel_conf, str(msg)))
                        continue
            except Exception as msg:
                self.logger.error("Failed to open channel configuration file {} \
                                  contains error {}, SKIPPING".
                                  format(channel_conf, str(msg)))

            """
            check that channel configuration contains necessary keys
            if keys are missing channel is removed and error is printed
            """
            try:
                self.validate_channel(self.channels[name])
            except Exception as msg:
                self.logger.error("{} {}, REMOVING the channel".format(name, str(msg)))
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
