'''
Manager of channel configurations.

The ChannelConfigHandler manages only channel configurations and not
the global decision-engine configuration.  It is responsible for
loading channel configuration files and validating that the channels
have the correct configuration artifacts and inter-module product
dependencies.
'''

import importlib
import os

from decisionengine.framework.config import ValidConfig
import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.fs as fs
import decisionengine.framework.util.tsort as tsort

_MANDATORY_CHANNEL_KEYS = {'sources', 'logicengines', 'transforms', 'publishers'}
_ALLOWED_CHANNEL_KEYS = _MANDATORY_CHANNEL_KEYS | {'task_manager'}
_MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}

def _make_logger(global_config):
    if 'logger' not in global_config:
        raise RuntimeError("No logger configuration has been specified.")
    try:
        logger_config = global_config['logger']
        de_logger.set_logging(log_level=logger_config.get('log_level', 'INFO'),
                              file_rotate_by=logger_config.get('file_rotate_by', "size"),
                              rotation_time_unit=logger_config.get('rotation_time_unit', 'D'),
                              rotation_interval=logger_config.get('rotation_time_interval', 1),
                              max_backup_count=logger_config.get('max_backup_count', 6),
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

def _validate(channel):
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


class ChannelConfigHandler():

    def __init__(self, global_config, channel_config_dir):
        self.channel_config_dir = channel_config_dir
        self.channels = {}
        self.logger = _make_logger(global_config)

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

    def get_channels(self):
        return self.channels

    def print_channel_config(self, channel):
        return self.channels[channel].dump()

    def _load_channel(self, channel_name, path):
        channel_config = None
        try:
            channel_config = ValidConfig.ValidConfig(path)
        except Exception as msg:
            return (False,
                    f"Failed to open channel configuration file {path} "
                    f"contains error\n-> {msg}\nSKIPPING channel")

        try:
            _validate(channel_config)
        except Exception as msg:
            return (False,
                    f"The channel configuration file {path} contains a "
                    f"validation error\n{msg}\nSKIPPING channel")

        self.channels[channel_name] = channel_config
        return (True, channel_config)

    def load_channel(self, channel_name):
        '''
        Load a single configuration for a channel with the supplied name.

        The behavior is to read a configuration file whose path is:

          <cached channel config. dir>/{channel_name}.jsonnet

        where the cached channel-configuration directory was stored whenever the
        ChannelConfigHandler object was created, and {channel_name} is the value
        of the supplied method argument.
        '''
        path = os.path.join(self.channel_config_dir, channel_name) + '.jsonnet'
        return self._load_channel(channel_name, path)

    def load_all_channels(self):
        '''
        Load all channel configurations inside the stored channel-configuration directory.

        Any cached configurations will be dropped prior to reloading.
        '''
        if self.channels:
            self.channels = {}
            self.logger.info("All channel configurations have been removed and are being reloaded.")

        files = fs.files_with_extensions(self.channel_config_dir, '.conf', '.jsonnet')
        for channel_name, full_path in files:
            # Load only the channels that are not already in memory
            if channel_name in self.channels:
                continue

            success, result = self._load_channel(channel_name, full_path)
            if not success:
                self.logger.error(result)
