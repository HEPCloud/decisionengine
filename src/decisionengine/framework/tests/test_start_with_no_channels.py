'''Fixture based DE Server tests of the server without channels, then with them'''
# pylint: disable=redefined-outer-name

import os
import re
import shutil
import tempfile
from unittest.mock import patch

import pytest

from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _create_de_server, parse_program_options
from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block  # noqa: F401
from decisionengine.framework.taskmanager.TaskManager import State
from decisionengine.framework.tests.fixtures import TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH
from decisionengine.framework.util.sockets import get_random_port

_port = get_random_port()

EMPTY_DIR = tempfile.TemporaryDirectory()


@pytest.fixture
def deserver_mock_data_block(mock_data_block):  # noqa: F811
    global_config, channel_config_handler = _get_de_conf_manager(TEST_CONFIG_PATH,
                                                                 EMPTY_DIR.name,
                                                                 parse_program_options([f'--port={_port}']))
    server = _create_de_server(global_config, channel_config_handler)
    server.start_channels()
    server.block_while(State.BOOT)
    yield server
    server.stop_channels()


# Because pytest will reorder the tests based on the method name,
# we implement the whole 'workflow' as one unit test.
def test_start_from_nothing(deserver_mock_data_block):
    deserver = deserver_mock_data_block

    # Verify that nothing is active
    output = deserver.rpc_status()
    assert "No channels are currently active" in output

    output = deserver.rpc_print_products()
    assert "No channels are currently active" in output

    # Add channel config to directory
    channel_config = os.path.join(TEST_CHANNEL_CONFIG_PATH, 'test_channel.jsonnet')  # noqa: F405
    new_config_path = shutil.copy(channel_config, EMPTY_DIR.name)
    assert os.path.exists(new_config_path)

    # Activate channel and check for steady state
    deserver.rpc_start_channel('test_channel')
    deserver.block_while(State.BOOT)
    output = deserver.rpc_status()
    assert re.search('test_channel.*state = STEADY', output)

    # Take channel offline.  Make sure Publisher.shutdown method is called and
    # that we stop cleanly.
    # with patch('decisionengine.framework.modules.Publisher.Publisher.shutdown'
    with patch('decisionengine.framework.tests.PublisherNOP.PublisherNOP.shutdown'
        ) as mocked_shutdown:
        output = deserver.rpc_stop_channel('test_channel')
        mocked_shutdown.assert_called()
        print("yay")
        assert output == 'Channel test_channel stopped cleanly.'

    # output = deserver.rpc_stop_channel('test_channel')
    # assert output == 'Channel test_channel stopped cleanly.'

    # Verify no channels are active
    output = deserver.rpc_status()
    assert "No channels are currently active" in output

    # Bring channel back online
    deserver.rpc_start_channel('test_channel')
    deserver.block_while(State.BOOT)
    output = deserver.rpc_status()
    assert re.search('test_channel.*state = STEADY', output)

    # Kill channel
    output = deserver.rpc_kill_channel('test_channel', 0)
    assert output == 'Channel test_channel has been killed.'

    # Verify that the relevant configuration file still exists.
    assert os.path.exists(new_config_path)
