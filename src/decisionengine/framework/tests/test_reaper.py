'''Fixture based DE Server for the reaper tests'''
# pylint: disable=redefined-outer-name

import pytest

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    DEServer,
    TEST_CONFIG_PATH,
    TEST_CHANNEL_CONFIG_PATH,
)

deserver = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_reaper_status(deserver):
    '''Verify reaper status'''
    output = deserver.de_client_run_cli('--reaper-status')

    # find reaper section
    assert 'reaper:' in output

    # find reaper state section
    assert 'state:' in output

    # find reaper interval
    assert 'retention_interval:' in output

@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_reaper_stop(deserver):
    '''Verify reaper can stop'''
    output = deserver.de_client_run_cli('--reaper-stop')
    assert output == 'OK'

    # get status to be sure
    output = deserver.de_client_run_cli('--reaper-status')

    # find reaper section
    assert 'reaper:' in output

    # find reaper state section
    assert 'state:' in output

    # find reaper state value
    assert 'State.SHUTDOWN' in output

@pytest.mark.usefixtures("deserver")
def test_client_can_get_de_server_reaper_start_delay(deserver):
    '''Verify reaper can start with delay'''
    # make sure the reaper is stopped first
    deserver.de_client_run_cli('--reaper-stop')

    output = deserver.de_client_run_cli('--reaper-start', '--reaper-start-delay-secs=90')
    assert output == 'OK'

    # get status to be sure
    output = deserver.de_client_run_cli('--reaper-status')

    # find reaper section
    assert 'reaper:' in output

    # find reaper state section
    assert 'state:' in output

    # find reaper state value
    assert 'State.IDLE' in output
