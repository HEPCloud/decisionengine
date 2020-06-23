import os
import pytest

from decisionengine.framework.configmanager import ConfigManager

@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    monkeypatch.setenv('CONFIG_PATH',
                       os.path.join(this_dir, 'de'))

def load(filename):
    manager = ConfigManager.ConfigManager(filename)
    manager.load()

def test_empty_config():
    with pytest.raises(RuntimeError) as e:
        load('empty.conf')
    assert e.match('Empty configuration file .*/empty\\.conf')

def test_wrong_type():
    with pytest.raises(RuntimeError) as e:
        load('wrong_type.conf')
    assert e.match('The configuration file must be a Python dictionary')

def test_empty_dict():
    with pytest.raises(RuntimeError) as e:
        load('empty_dict.conf')
    assert e.match('No logger configuration has been specified')

def test_empty_dict_with_leading_comment():
    with pytest.raises(RuntimeError) as e:
        load('empty_dict_with_leading_comment.conf')
    assert e.match('No logger configuration has been specified')
