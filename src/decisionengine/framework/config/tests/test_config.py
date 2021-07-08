import os
import pytest
import re

from decisionengine.framework.config.ChannelConfigHandler import ChannelConfigHandler
from decisionengine.framework.config.ValidConfig import ValidConfig

_this_dir = os.path.dirname(os.path.abspath(__file__))
_global_config_dir = os.path.join(_this_dir, 'de')

def _global_config_file(relative_filename):
    return os.path.join(_global_config_dir, relative_filename)

def _channel_config_dir(relative_dir):
    return os.path.join(_this_dir, relative_dir)

@pytest.fixture()
def load():
    def _call(relative_filename,
              relative_channel_config_dir=None):
        channel_config_dir = None
        if relative_channel_config_dir is None:
            channel_config_dir = _channel_config_dir('channels/no_config_files')
        else:
            channel_config_dir = _channel_config_dir(relative_channel_config_dir)

        filename = _global_config_file(relative_filename)
        global_config = ValidConfig(filename)
        handler = ChannelConfigHandler(global_config, channel_config_dir)
        handler.load_all_channels()
        return handler
    yield _call


# --------------------------------------------------------------------
# These tests demonstrate failure modes when reading a DE
# application configuration file.
def test_empty_config(load):
    with pytest.raises(RuntimeError) as e:
        load('empty.conf')
    assert e.match('Empty configuration file .*/empty\\.conf')

def test_wrong_type(load):
    with pytest.raises(RuntimeError) as e:
        load('wrong_type.conf')
    assert e.match('The supplied configuration must be a valid Jsonnet/JSON document')

def test_syntax_error_in_config_names_bad_file(load):
    with pytest.raises(Exception) as e:
        load('invalid.jsonnet')
    assert e.match('invalid.jsonnet')


# --------------------------------------------------------------------
# These tests yield valid DE configuration structures. However, the
# configurations are missing a logger configuration, which is the next
# failure mode after reading the configuration files.
def test_empty_dict(load):
    with pytest.raises(RuntimeError) as e:
        load('empty_dict.conf')
    assert e.match('No logger configuration has been specified')

def test_empty_dict_with_leading_comment(load):
    with pytest.raises(RuntimeError) as e:
        load('empty_dict_with_leading_comment.conf')
    assert e.match('No logger configuration has been specified')

# --------------------------------------------------------------------
# These tests validate well-formed DE configurations, but they also
# check that the appropriate warning messages are emitted regarding
# Python support for a Jsonnet configuration system.
def test_minimal_python(load, capsys):
    load('minimal_python.conf')
    stdout, stderr = capsys.readouterr()
    assert not stdout
    expected = "The supplied configuration.*has been converted to a valid JSON construct"
    assert re.search(expected, stderr, flags=re.DOTALL)

def test_minimal_jsonnet_wrong_extension(load, capsys):
    load('minimal_jsonnet.conf')
    stdout, stderr = capsys.readouterr()
    assert not stdout
    expected = r"Please rename '.*/minimal_jsonnet\.conf' to '.*/minimal_jsonnet\.jsonnet'"
    assert re.match(expected, stderr)

def test_minimal_jsonnet_right_extension(load, capsys):
    load('minimal.jsonnet')
    stdout, stderr = capsys.readouterr()
    assert not stdout
    assert not stderr

# --------------------------------------------------------------------
# These tests verify expected behavior for channel (not DE)
# configurations.
def test_channel_no_config_files(load):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/no_config_files')

def test_channel_empty_config(load, capsys, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/empty_config')
    stdout, stderr = capsys.readouterr()
    expected = "The supplied configuration.*has been converted to a valid JSON construct"
    assert re.search(expected, stderr, flags=re.DOTALL)
    assert re.search('Empty configuration file .*\\.jsonnet', caplog.text)

def test_channel_empty_dictionary(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/empty_dictionary')
    assert re.search("channel is missing one or more mandatory keys", caplog.text)

def test_channel_no_modules(load):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/no_modules')

def test_channel_invalid_modules_string(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/invalid_modules_string')
    assert re.search("is not a dictionary:", caplog.text)

def test_channel_invalid_modules_list(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/invalid_modules_list')
    assert re.search("is not a dictionary:", caplog.text)

def test_channel_invalid_modules_no_keys(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/invalid_modules_no_keys')
    assert re.search("is not a dictionary:", caplog.text)

def test_channel_module_missing_all(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/module_missing_all')
    assert re.search("is missing one or more mandatory keys", caplog.text)

def test_channel_module_missing_module(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/module_missing_module')
    assert re.search("is missing one or more mandatory keys", caplog.text)

def test_channel_module_missing_parameters(load, caplog):
    load('minimal_python.conf',
         relative_channel_config_dir='channels/module_missing_parameters')
    assert re.search("is missing one or more mandatory keys", caplog.text)

# --------------------------------------------------------------------
# Test channel names based on channel configuration file names
def test_channel_names(load):
    handler = load('minimal_python.conf',
                   relative_channel_config_dir='channels/no_modules')
    assert list(handler.get_channels().keys()) == ['no_modules']
    handler.print_channel_config('no_modules')

# --------------------------------------------------------------------
def test_channel_loading(caplog):
    filename = _global_config_file('minimal.jsonnet')
    global_config = ValidConfig(filename)
    channel_config_dir = _channel_config_dir('channels/no_modules')
    handler = ChannelConfigHandler(global_config, channel_config_dir)

    success, result = handler.load_channel('no_modules')
    assert success and isinstance(result, ValidConfig)
    success, result = handler.load_channel('non_existent')
    assert not success and isinstance(result, str)

    assert len(handler.get_channels()) == 1
    handler.load_all_channels()
    assert 'All channel configurations have been removed and are being reloaded.' in caplog.text
