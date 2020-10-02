'''Fixture based DE Server tests of the defaults'''
# pylint: disable=redefined-outer-name

import time

import pytest

from decisionengine.framework.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA
from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH) # pylint: disable=invalid-name

@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_status(deserver):
    '''Verify channel enters stable state'''
    # wait for a few seconds for the channels to finish starting
    time.sleep(1)
    output = deserver.de_client_run_cli('--status')
    for _ in range(6): # pylint: disable=unused-variable
        if 'BOOT' in output:
            time.sleep(1)
            output = deserver.de_client_run_cli('--status')

    assert 'state = STEADY' in output

@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_show_config(deserver):
    '''Verify config has expected items'''
    output = deserver.de_client_run_cli('--show-config')
    assert 'decisionengine.framework.tests.SourceNOP' in output
    assert 'decisionengine.framework.tests.TransformNOP' in output

@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_show_logger_level(deserver):
    '''Verify can fetch log level'''
    output = deserver.de_client_run_cli('--print-engine-loglevel')
    assert output in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
