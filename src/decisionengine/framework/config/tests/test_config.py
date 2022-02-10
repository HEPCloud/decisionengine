# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import re

import pytest

from decisionengine.framework.config.ChannelConfigHandler import ChannelConfigHandler
from decisionengine.framework.config.ValidConfig import ValidConfig

_this_dir = os.path.dirname(os.path.abspath(__file__))
_global_config_dir = os.path.join(_this_dir, "de")


def _global_config_file(relative_filename):
    return os.path.join(_global_config_dir, relative_filename)


def _channel_config_dir(relative_dir):
    return os.path.join(_this_dir, relative_dir)


@pytest.fixture()
def load():
    def _call(relative_filename, relative_channel_config_dir=None):
        channel_config_dir = None
        if relative_channel_config_dir is None:
            channel_config_dir = _channel_config_dir("channels/no_config_files")
        else:
            channel_config_dir = _channel_config_dir(relative_channel_config_dir)

        filename = _global_config_file(relative_filename)
        global_config = ValidConfig(filename)
        handler = ChannelConfigHandler(global_config, channel_config_dir)
        handler.load_all_channels()
        return handler

    yield _call

    # Cleanup code on this is tricky as the unit tests either share
    # a static directory to store their logfiles across multiple
    # fixtures or use random tempfile names.


# --------------------------------------------------------------------


def test_empty_config(load):
    with pytest.raises(RuntimeError, match="Empty configuration file .*/empty\\.jsonnet"):
        load("empty.jsonnet")


def test_syntax_error_in_config_names_bad_file(load):
    with pytest.raises(Exception, match="invalid.jsonnet"):
        load("invalid.jsonnet")


def test_valid_but_empty_config(load):
    # This tests a valid Jsonnet structure; however, the configuration
    # is missing a logger configuration, which is the next failure
    # mode after reading the configuration file.
    with pytest.raises(RuntimeError, match="No logger configuration has been specified"):
        load("valid_but_empty.jsonnet")


def test_minimal_jsonnet_wrong_extension(load, capsys):
    load("minimal.conf")
    stdout, stderr = capsys.readouterr()
    assert not stdout
    expected = r"Please rename '.*/minimal\.conf' to '.*/minimal\.jsonnet'"
    assert re.match(expected, stderr)


def test_minimal_jsonnet_right_extension(load, capsys):
    load("minimal.jsonnet")
    stdout, stderr = capsys.readouterr()
    assert not stdout
    assert not stderr


def test_channel_no_config_files(load):
    load("minimal.jsonnet", relative_channel_config_dir="channels/no_config_files")


def test_channel_empty_config(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/empty_config")
    assert re.search("Empty configuration file .*\\.jsonnet", caplog.text)


def test_channel_empty_dictionary(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/empty_dictionary")
    assert re.search("channel is missing one or more mandatory keys", caplog.text)


def test_channel_no_modules(load):
    load("minimal.jsonnet", relative_channel_config_dir="channels/no_modules")


def test_channel_invalid_modules_string(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/invalid_modules_string")
    assert re.search("is not a dictionary:", caplog.text)


def test_channel_invalid_modules_list(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/invalid_modules_list")
    assert re.search("is not a dictionary:", caplog.text)


def test_channel_invalid_modules_no_keys(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/invalid_modules_no_keys")
    assert re.search("is not a dictionary:", caplog.text)


def test_channel_module_missing_all(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/module_missing_all")
    assert re.search("is missing one or more mandatory keys", caplog.text)


def test_channel_module_missing_module(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/module_missing_module")
    assert re.search("is missing one or more mandatory keys", caplog.text)


def test_channel_module_missing_parameters(load, caplog):
    load("minimal.jsonnet", relative_channel_config_dir="channels/module_missing_parameters")
    assert re.search("is missing one or more mandatory keys", caplog.text)


# --------------------------------------------------------------------
# Test channel names based on channel configuration file names
def test_channel_names(load):
    handler = load("minimal.jsonnet", relative_channel_config_dir="channels/no_modules")
    assert list(handler.get_channels().keys()) == ["no_modules"]
    handler.print_channel_config("no_modules")


# --------------------------------------------------------------------
def test_channel_loading(caplog):
    filename = _global_config_file("minimal.jsonnet")
    global_config = ValidConfig(filename)
    channel_config_dir = _channel_config_dir("channels/no_modules")
    handler = ChannelConfigHandler(global_config, channel_config_dir)

    success, result = handler.load_channel("no_modules")
    assert success
    assert isinstance(result, ValidConfig)
    success, result = handler.load_channel("non_existent")
    assert not success
    assert isinstance(result, str)

    assert len(handler.get_channels()) == 1
    handler.load_all_channels()
    assert "All channel configurations have been removed and are being reloaded." in caplog.text
