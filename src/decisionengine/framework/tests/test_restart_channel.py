import os
import pathlib
import re

import pytest

from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block  # noqa: F401
from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager
from decisionengine.framework.engine.DecisionEngine import _create_de_server
from decisionengine.framework.engine.DecisionEngine import parse_program_options
from decisionengine.framework.taskmanager.TaskManager import State
from decisionengine.framework.util.sockets import get_random_port

_this_dir = pathlib.Path(__file__).parent.resolve()
_CONFIG_PATH = os.path.join(_this_dir, "etc/decisionengine")
_CHANNEL_CONFIG_PATH = os.path.join(_CONFIG_PATH, 'config.d')

_port = get_random_port()


@pytest.fixture
def deserver_mock_data_block(mock_data_block):  # noqa: F811
    global_config, channel_config_handler = _get_de_conf_manager(_CONFIG_PATH,
                                                                 _CHANNEL_CONFIG_PATH,
                                                                 parse_program_options([f'--port={_port}']))
    server = _create_de_server(global_config, channel_config_handler)
    server.start_channels()
    server.block_while(State.BOOT)
    yield server
    server.stop_channels()


# Because pytest will reorder the tests based on the method name,
# we implement the whole 'workflow' as one unit test.
def test_restart_channel(deserver_mock_data_block):
    # Verify that nothing is active
    output = deserver_mock_data_block.rpc_status()
    assert re.search('test_channel.*state = STEADY', output)

    # Take channel offline
    output = deserver_mock_data_block.rpc_stop_channel('test_channel')
    assert output == 'Channel test_channel stopped cleanly.'

    # Verify no channels are active
    output = deserver_mock_data_block.rpc_status()
    assert "No channels are currently active" in output

    # Take channel offline
    output = deserver_mock_data_block.rpc_start_channel('test_channel')
    assert output == 'OK'
