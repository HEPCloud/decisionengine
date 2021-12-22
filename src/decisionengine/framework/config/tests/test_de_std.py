# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

from decisionengine.framework.config.ValidConfig import _config_from_file

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def config(basename, jpathdirs=None):
    return _config_from_file(os.path.join(_THIS_DIR, "libsonnet", basename), jpathdirs)


def test_jpath():
    cfg = config("import_from_jpath.jsonnet", jpathdirs=[os.path.join(_THIS_DIR, "libsonnet", "jpath_test")])
    assert cfg == {}


def test_combine_one_level():
    cfg = config("combine_one_level.jsonnet")
    assert cfg["test"] == cfg["reference"]


def test_combine_one_level_skip_proxies():
    cfg = config("combine_one_level_skip_proxies.jsonnet")
    assert cfg["test"] == cfg["reference"]


def test_allow_duplicate_keys_same_values():
    cfg = config("allow_duplicate_keys_same_values.jsonnet")
    assert cfg["test"] == cfg["reference"]


def test_error_on_duplicate_keys():
    with pytest.raises(RuntimeError, match=".*The following keys have conflicting values.*s1_a1"):
        config("error_on_duplicate_keys.jsonnet")


def test_allow_duplicate_source_proxy_keys():
    cfg = config("allow_duplicate_source_proxy_keys.jsonnet")
    assert cfg["test"] == cfg["reference"]
