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
import toposort

from decisionengine.framework.config import ValidConfig
import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.fs as fs

_MANDATORY_CHANNEL_KEYS = {'sources', 'logicengines', 'transforms', 'publishers'}
_ALLOWED_CHANNEL_KEYS = _MANDATORY_CHANNEL_KEYS | {'task_manager'}
_MANDATORY_MODULE_KEYS = {"module", "name", "parameters"}

def _make_de_logger(global_config):
    if 'logger' not in global_config:
        raise RuntimeError("No logger configuration has been specified.")
    try:
        logger_config = global_config['logger']
        de_logger.set_logging(log_level=logger_config.get('log_level', 'INFO'),
                              file_rotate_by=logger_config.get('file_rotate_by', "size"),
                              rotation_time_unit=logger_config.get('rotation_time_unit', 'D'),
                              rotation_interval=logger_config.get('rotation_time_interval', 1),
                              max_backup_count=logger_config.get('max_backup_count', 6),
                              max_file_size=logger_config.get('max_file_size', 1000000),
                              log_file_name=logger_config['log_file'])
        return de_logger.get_logger()
    except Exception as msg:  # pragma: no cover
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

        if not isinstance(conf, dict):
            raise RuntimeError(f"{name} module is not a dictionary: {type(conf)}")

        for module_name, module_conf in conf.items():
            try:
                module_keys = set(module_conf.keys())
            except Exception as msg:
                raise RuntimeError(f"{name} module {module_name} is not a dictionary:\n{msg}")
            diff = _MANDATORY_MODULE_KEYS - module_keys
            if diff:
                missing_keys = str(list(diff))
                raise RuntimeError(f"{name} module {module_name} is missing one or more mandatory keys:\n{missing_keys} ")

def _modules_from(channel, key):
    result = {}
    for name, config in channel.get(key).items():
        result[name] = importlib.import_module(config.get('module'))
    return result

def _produced_products(channel, key):
    result = {}
    for name, mod in _modules_from(channel, key).items():
        try:
            produces = getattr(mod, 'PRODUCES')
            result.update(dict.fromkeys(produces, name))
        except AttributeError:
            raise RuntimeError(f"module {name} does not have a PRODUCES list")
    return result

def _consumed_products(channel, key):
    result = {}
    for name, mod in _modules_from(channel, key).items():
        try:
            result[name] = set(getattr(mod, 'CONSUMES'))
        except AttributeError:
            raise RuntimeError(f"module {name} does not have a CONSUMES list")
    return result

def _validate(channel):
    """
    Validate channels
    :type channel: :obj:`dict`
    """
    _check_keys(channel)


    produced_products = _produced_products(channel, 'sources')
    produced_products.update(_produced_products(channel, 'transforms'))

    consumed_products = _consumed_products(channel, 'transforms')
    consumed_products.update(_consumed_products(channel, 'publishers'))

    # Check that products to be consumed are actually produced
    all_consumes = set()
    all_consumes.update(*consumed_products.values())
    all_produces = set(produced_products.keys())
    if not all_consumes.issubset(all_produces):
        extra_keys = list(all_consumes - all_produces)
        raise RuntimeError(f"consumes are not a subset of produce, extra keys {extra_keys}")

    graph = {}
    for consumer, products in consumed_products.items():
        graph[consumer] = set(map(lambda p: produced_products.get(p), products))

    # Do the check
    try:
        toposort.toposort_flatten(graph)  # Flatten will trigger any potential circularity errors
    except Exception as e:
        raise RuntimeError(f"A produces/consumes circularity exists in the configuration:\n{e}")


class ChannelConfigHandler():

    def __init__(self, global_config, channel_config_dir):
        self.channel_config_dir = channel_config_dir
        self.channels = {}
        self.logger = _make_de_logger(global_config)

    def get_produces(self, channel_config):
        produces = {}
        for key in ('sources', 'transforms'):
            for name, mod in _modules_from(channel_config, key).items():
                produces.setdefault(name, []).extend(getattr(mod, 'PRODUCES'))
        return produces

    def get_channels(self):
        return self.channels

    def print_channel_config(self, channel):
        return self.channels[channel].dump()

    def _load_channel(self, channel_name, path):
        channel_config = None
        self.logger.debug("Loading channel %s from %s.", channel_name, path)
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
        self.logger.debug("Channel %s config is valid.", channel_name)

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
                self.logger.info(f"Already loaded a channel called '{channel_name}', skipping {full_path}")
                continue

            success, result = self._load_channel(channel_name, full_path)
            if not success:
                self.logger.error(result)
