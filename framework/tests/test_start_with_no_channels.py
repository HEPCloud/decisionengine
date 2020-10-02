'''Fixture based DE Server tests of the server without channels, then with them'''
# pylint: disable=redefined-outer-name

import os
import re
import shutil
import tempfile
import time

import pytest

from decisionengine.framework.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA
from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH

EMPTY_DIR = tempfile.TemporaryDirectory()

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=EMPTY_DIR.name) # pylint: disable=invalid-name

@pytest.fixture(autouse=True)
def cleanup_tmpdir():
    # Code to run before each test
    if os.path.isdir(EMPTY_DIR.name):
        shutil.rmtree(EMPTY_DIR.name)
        os.mkdir(EMPTY_DIR.name)

    # test runs under 'yield' here
    yield

    # Code to run after each test
    #pass

@pytest.mark.usefixtures("deserver")
def test_start_from_nothing(deserver):
    # Because pytest will reorder the tests based on the method name,
    # we implement the whole 'workflow' as one unit test.

    # Verify that nothing is active
    output = deserver.de_client_run_cli("--status")
    assert "No channels are currently active" in output

    output = deserver.de_client_run_cli("--print-products")
    assert "No channels are currently active" in output

    # Add channel config to directory
    channel_config = os.path.join(TEST_CHANNEL_CONFIG_PATH, 'test_channel.jsonnet') # noqa: F405
    new_config_path = shutil.copy(channel_config, EMPTY_DIR.name)
    assert os.path.exists(new_config_path)

    # Activate channel and check for steady state
    output = deserver.de_client_run_cli('--start-channel', 'test_channel')
    assert output == 'OK'
    time.sleep(5)
    output = deserver.de_client_run_cli('--status')
    assert re.search('test_channel.*state = STEADY', output)

    # Take channel offline
    output = deserver.de_client_run_cli('--stop-channel', 'test_channel')
    assert output == 'OK'

    # Verify no channels are active
    output = deserver.de_client_run_cli("--status")
    assert "No channels are currently active" in output

    # Verify that the relevant configuration file still exists.
    assert os.path.exists(new_config_path)
