import os
import pytest
import re

from decisionengine.framework.configmanager import ConfigManager

_this_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture()
def load(monkeypatch):
    def _call(filename, relative_channel_config_dir=None):
        monkeypatch.setenv('CONFIG_PATH', os.path.join(_this_dir, 'de'))
        if relative_channel_config_dir is None:
            monkeypatch.setenv('CHANNEL_CONFIG_PATH',
                               os.path.join(_this_dir, 'channels/no_config_files'))
        else:
            monkeypatch.setenv('CHANNEL_CONFIG_PATH',
                               os.path.join(_this_dir, relative_channel_config_dir))
        manager = ConfigManager.ConfigManager()
        manager.load(filename)
    return _call


#-------------------------------------------------
def test_empty_config(load):
    with pytest.raises(RuntimeError) as e:
        load('empty.conf')
    assert e.match('Empty configuration file .*/empty\\.conf')

def test_wrong_type(load):
    with pytest.raises(RuntimeError) as e:
        load('wrong_type.conf')
    assert e.match('The configuration file must be a Python dictionary')

def test_empty_dict(load):
    with pytest.raises(RuntimeError) as e:
        load('empty_dict.conf')
    assert e.match('No logger configuration has been specified')

def test_empty_dict_with_leading_comment(load):
    with pytest.raises(RuntimeError) as e:
        load('empty_dict_with_leading_comment.conf')
    assert e.match('No logger configuration has been specified')

# -------------------------------------------------
def test_minimal_python(load):
    load('minimal_python.conf')

# -------------------------------------------------
def test_channel_no_config_files(load):
    load('minimal_python.conf', 'channels/no_config_files')

def test_channel_empty_config(load):
    with pytest.raises(RuntimeError) as e:
        load('minimal_python.conf', 'channels/empty_config')
    assert e.match('Empty configuration file .*\\.conf')

def test_channel_empty_dictionary(load, caplog):
    load('minimal_python.conf', 'channels/empty_dictionary')
    assert re.search("channel is missing one or more mandatory keys", caplog.text)

def test_channel_no_modules(load):
    load('minimal_python.conf', 'channels/no_modules')
