# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

import decisionengine.framework.config.policies as policies


def test_valid_dir(tmp_path):
    d = tmp_path
    assert d == policies.valid_dir(d, "Only-for-error-msg")

    f = d / "a.txt"
    f.touch()
    with pytest.raises(RuntimeError) as e:
        policies.valid_dir(f, "Only-for-error-msg")
    e.match("Only-for-error-msg configuration directory.*not found")


def test_global_config_dir(tmp_path, monkeypatch):
    de_config = tmp_path
    monkeypatch.setenv("CONFIG_PATH", str(de_config))
    global_config_dir = policies.global_config_dir()
    assert de_config == global_config_dir


def test_channel_config_dir(tmp_path, monkeypatch):
    channel_cfg_dir = tmp_path / "config.d"
    absolute_parent_path = str(channel_cfg_dir.parent.resolve())
    channel_cfg_dir.mkdir()

    # Explicit parent path
    channel_config_dir = policies.channel_config_dir(absolute_parent_path)
    assert channel_cfg_dir == channel_config_dir

    # Through channel-config environment variable
    with monkeypatch.context() as m:
        m.setenv("CHANNEL_CONFIG_PATH", str(channel_cfg_dir))
        channel_config_dir = policies.channel_config_dir()
        assert channel_cfg_dir == channel_config_dir

    # Through global-config environment variable
    with monkeypatch.context() as m:
        m.setenv("CONFIG_PATH", absolute_parent_path)
        channel_config_dir = policies.channel_config_dir()
        assert channel_cfg_dir == channel_config_dir


def test_global_config_file(tmp_path, monkeypatch):
    cfg_file = tmp_path / policies.GLOBAL_CONFIG_FILENAME
    absolute_parent_path = str(cfg_file.parent.resolve())

    with pytest.raises(RuntimeError) as e:
        policies.global_config_file(absolute_parent_path)
    e.match("Global configuration file.*not found")

    # Create config file
    cfg_file.touch()

    # Explicit parent path
    global_cfg_file = policies.global_config_file(absolute_parent_path)
    assert global_cfg_file == cfg_file

    # Through global-config environment variable
    with monkeypatch.context() as m:
        m.setenv("CONFIG_PATH", absolute_parent_path)
        global_cfg_file = policies.global_config_file()
        assert global_cfg_file == cfg_file
