'''Fixture based DE Server tests of the defaults'''
# pylint: disable=redefined-outer-name

import pytest

from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH  # noqa: F401

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_status(deserver):
    '''Verify channel enters stable state'''
    deserver.de_client_run_cli('--block-while', 'BOOT'),
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
