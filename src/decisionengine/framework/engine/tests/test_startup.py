# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import tempfile

import pytest

from decisionengine.framework.engine.DecisionEngine import _check_metrics_env, _get_global_config, parse_program_options

# Because we just want to ensure correct behavior of program options
# overriding a configuration, it is not necessary to have a valid DE
# server configuration.  We therefore produce a small, temporary file
# with the valid Jsonnet configuration '{}'.

# TODO: need method to clean up file eventually
global_config_file = tempfile.NamedTemporaryFile()
global_config_file.write(b"{}")
global_config_file.flush()

# For some of the metrics environment tests, we need to set up the environment


@pytest.fixture()
def metrics_env_setup(tmp_path, monkeypatch):
    """Make sure we have a directory set for PROMETHEUS_MULTIPROC_DIR so that
    metric instantiation gives us multiprocess metrics"""
    # Get a fixed dir
    d = tmp_path
    monkeypatch.setenv("PROMETHEUS_MULTIPROC_DIR", str(d))
    yield
    monkeypatch.delenv("PROMETHEUS_MULTIPROC_DIR")


# We do not call the DE's _get_de_conf_manager as that assumes the
# presence of configuration directories, which are unnecessary for
# this test.


def _check_override(arguments):
    options = parse_program_options(arguments)
    return _get_global_config(global_config_file.name, options)


def test_default_config():
    arguments = []
    assert _check_override(arguments) == {"server_address": ["localhost", 8888]}


def test_change_port():
    arguments = ["--port=54321"]
    assert _check_override(arguments) == {"server_address": ["localhost", 54321]}


def test_check_metrics_env_no_webserver():
    arguments = ["--no-webserver"]
    options = parse_program_options(arguments)
    try:
        _check_metrics_env(options)
    except Exception as e:
        pytest.fail(f"--no-webserver should have skipped the metrics env check, but instead we got an exception {e}")


@pytest.mark.usefixtures("metrics_env_setup")
def test_check_metrics_env_var_set():
    arguments = []
    options = parse_program_options(arguments)
    try:
        _check_metrics_env(options)
    except Exception as e:
        pytest.fail(
            f"PROMETHEUS_MULTIPROC_DIR should be set, so check_metrics_env should have passed but instead we got an exception {e}"
        )


def test_check_metrics_env_var_unset():
    arguments = []
    options = parse_program_options(arguments)
    with pytest.raises(EnvironmentError) as excinfo:
        _check_metrics_env(options)
    assert "PROMETHEUS_MULTIPROC_DIR must be set" in str(excinfo.value)
