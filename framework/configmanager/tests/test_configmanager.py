import os
import pytest
import re

from decisionengine.framework.configmanager import ConfigManager

_this_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture()
def load(monkeypatch):
    def _call(filename,
              relative_channel_config_dir=None,
              program_options=None):
        monkeypatch.setenv('CONFIG_PATH', os.path.join(_this_dir, 'de'))
        if relative_channel_config_dir is None:
            monkeypatch.setenv('CHANNEL_CONFIG_PATH',
                               os.path.join(_this_dir, 'channels/no_config_files'))
        else:
            monkeypatch.setenv('CHANNEL_CONFIG_PATH',
                               os.path.join(_this_dir, relative_channel_config_dir))
        manager = ConfigManager.ConfigManager(program_options)
        manager.load(filename)
        return manager.get_global_config()
    return _call


# --------------------------------------------------------------------
# These tests demonstrate failure modes when reading a DE
# applicaation configuration file.
def test_empty_config(load):
    with pytest.raises(RuntimeError) as e:
        load('empty.conf')
    assert e.match('Empty configuration file .*/empty\\.conf')

def test_wrong_type(load):
    with pytest.raises(RuntimeError) as e:
        load('wrong_type.conf')
    assert e.match('The supplied configuration must be a valid Jsonnet/JSON document')

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

# --------------------------------------------------------------------
# These tests verify that program options are correctly included
# as/override part of the final configuration.
def test_program_options_default(load):
    address = ['localhost', 1234]
    config = load('minimal.jsonnet',
                  program_options={'server_address': address})
    assert config.get('server_address') == address

def test_program_options_update(load):
    # Verify non-modified 'server_address' value
    config = load('minimal_with_address.jsonnet')
    assert config.get('server_address') == ['localhost', 0]
    # Override value with program option
    address = ['localhost', 1234]
    config = load('minimal_with_address.jsonnet',
                  program_options={'server_address': address})
    assert config.get('server_address') == address

# --------------------------------------------------------------------
# These tests verify expected behavior for channel (not DE)
# configurations.
def test_channel_no_config_files(load):
    load('minimal_python.conf', 'channels/no_config_files')

def test_channel_empty_config(load, capsys, caplog):
    load('minimal_python.conf', 'channels/empty_config')
    stdout, stderr = capsys.readouterr()
    expected = "The supplied configuration.*has been converted to a valid JSON construct"
    assert re.search(expected, stderr, flags=re.DOTALL)
    assert re.search('Empty configuration file .*\\.jsonnet', caplog.text)

def test_channel_empty_dictionary(load, caplog):
    load('minimal_python.conf', 'channels/empty_dictionary')
    assert re.search("channel is missing one or more mandatory keys", caplog.text)

def test_channel_no_modules(load):
    load('minimal_python.conf', 'channels/no_modules')
