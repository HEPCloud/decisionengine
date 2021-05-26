"""Fixture based DE Server tests of the sample config"""
# pylint: disable=redefined-outer-name

import json

import pytest

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_PROG,
    DEServer,
    TEST_CONFIG_PATH,
    TEST_CHANNEL_CONFIG_PATH,
)

deserver = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_show_channel_logger_level(deserver):
    """Verify unknown channel has NOTSET"""
    output = deserver.de_client_run_cli("--get-channel-loglevel=UNITTEST")
    assert output == "NOTSET"


@pytest.mark.usefixtures("deserver")
def test_global_channel_log_level_in_config(deserver):
    """Verify global_channel_log_level setting exists"""
    output = deserver.de_client_run_cli("--show-de-config")
    assert "global_channel_log_level" in output


@pytest.mark.usefixtures("deserver")
def test_client_de_config_is_json(deserver):
    """Verify config can be fetched in json format"""
    output = deserver.de_client_run_cli("--show-de-config")
    assert json.loads(output)
