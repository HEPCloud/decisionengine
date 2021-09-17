import os

import pytest

import decisionengine.framework.config.ValidConfig as ValidConfig

_this_dir = os.path.dirname(os.path.abspath(__file__))
_global_config_dir = os.path.join(_this_dir, "de")


def _global_config_file(relative_filename):
    return os.path.join(_global_config_dir, relative_filename)


def test_no_such_file():
    with pytest.raises(RuntimeError):
        ValidConfig._convert_to_json("/this/file/really/shouldnt/exist")


def test_empty_config():
    with pytest.raises(RuntimeError):
        ValidConfig._convert_to_json(_global_config_file("empty.conf"))


def test_invalid_config():
    with pytest.raises(RuntimeError):
        ValidConfig._convert_to_json(_global_config_file("invalid.jsonnet"))


def test_wrong_type_config():
    with pytest.raises(RuntimeError):
        ValidConfig._convert_to_json(_global_config_file("wrong_type.conf"))
