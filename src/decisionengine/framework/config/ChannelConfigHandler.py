# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Manager of channel configurations.

The ChannelConfigHandler manages only channel configurations and not
the global decision-engine configuration.  It is responsible for
loading channel configuration files and validating that the channels
have the correct configuration artifacts.
"""

import os

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.util.fs as fs

from decisionengine.framework.config import ValidConfig
from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME

_MANDATORY_CHANNEL_KEYS = {"sources", "transforms", "publishers"}
_ALLOWED_CHANNEL_KEYS = _MANDATORY_CHANNEL_KEYS | {"logicengines", "task_manager"}
_MANDATORY_MODULE_KEYS = {"module", "parameters"}


def _make_de_logger(global_config):
    if "logger" not in global_config:
        raise RuntimeError("No logger configuration has been specified.")
    try:
        logger_config = global_config["logger"]
        de_logger.configure_logging(
            log_level=logger_config.get("log_level", "INFO"),
            file_rotate_by=logger_config.get("file_rotate_by", "size"),
            rotation_time_unit=logger_config.get("rotation_time_unit", "D"),
            rotation_interval=logger_config.get("rotation_time_interval", 1),
            max_backup_count=logger_config.get("max_backup_count", 6),
            max_file_size=logger_config.get("max_file_size", 1000000),
            log_file_name=logger_config["log_file"],
            start_q_logger=logger_config.get("start_q_logger", "True"),
        )
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
                raise RuntimeError(
                    f"{name} module {module_name} is missing one or more mandatory keys:\n{missing_keys} "
                )


class ChannelConfigHandler:
    def __init__(self, global_config, channel_config_dir):
        self.channel_config_dir = channel_config_dir
        self.channels = {}
        self.logger = _make_de_logger(global_config)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)

    def get_channels(self):
        return self.channels

    def print_channel_config(self, channel):
        return self.channels[channel].dump()

    def _load_channel(self, channel_name, path):
        channel_config = None
        self.logger.debug(f"Loading channel {channel_name} from {path}.")
        try:
            channel_config = ValidConfig.ValidConfig(path)
        except Exception as msg:
            return (
                False,
                f"Failed to open channel configuration file {path} contains error\n-> {msg}\nSKIPPING channel",
            )

        try:
            _check_keys(channel_config)
        except Exception as msg:
            return (
                False,
                f"The channel configuration file {path} contains a validation error\n{msg}\nSKIPPING channel",
            )
        self.logger.debug(f"Channel {channel_name} config is valid.")

        self.channels[channel_name] = channel_config
        return (True, channel_config)

    def load_channel(self, channel_name):
        """
        Load a single configuration for a channel with the supplied name.

        The behavior is to read a configuration file whose path is:

          <cached channel config. dir>/{channel_name}.jsonnet

        where the cached channel-configuration directory was stored whenever the
        ChannelConfigHandler object was created, and {channel_name} is the value
        of the supplied method argument.
        """
        path = os.path.join(self.channel_config_dir, channel_name) + ".jsonnet"
        return self._load_channel(channel_name, path)

    def load_all_channels(self):
        """
        Load all channel configurations inside the stored channel-configuration directory.

        Any cached configurations will be dropped prior to reloading.
        """
        if self.channels:
            self.channels = {}
            self.logger.info("All channel configurations have been removed and are being reloaded.")

        self.logger.info(f"Loading channel configs from:{self.channel_config_dir}")

        files = fs.files_with_extensions(self.channel_config_dir, ".conf", ".jsonnet")
        for channel_name, full_path in files:
            # Load only the channels that are not already in memory
            if channel_name in self.channels:
                self.logger.info(f"Already loaded a channel called '{channel_name}'. Skipping {full_path}")
                continue

            success, result = self._load_channel(channel_name, full_path)
            if not success:
                self.logger.error(f"CHANNEL LOAD FAILURE: {result}")
