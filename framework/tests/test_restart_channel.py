import multiprocessing
import pathlib
import os
import re
import time

import pytest

import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _start_de_server, parse_program_options
from decisionengine.framework.util.sockets import get_random_port
from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block # noqa: F401

_this_dir = pathlib.Path(__file__).parent.resolve()
_CONFIG_PATH = os.path.join(_this_dir, "etc/decisionengine")
_CHANNEL_CONFIG_PATH = os.path.join(_CONFIG_PATH, 'config.d')

_port = get_random_port()

def run_server():
    global_config, channel_config_handler = _get_de_conf_manager(_CONFIG_PATH,
                                                                 _CHANNEL_CONFIG_PATH,
                                                                 parse_program_options([f'--port={_port}']))
    _start_de_server(global_config, channel_config_handler)

def de_client_request(*args):
    return de_client.main([f"--port={_port}", *args])

@pytest.fixture
def deserver_mock_data_block(mock_data_block): # noqa: F811
    worker = multiprocessing.Process(target=run_server)
    worker.start()
    time.sleep(2) # Make sure channels have enough time to start
    yield
    de_client_request("--stop")
    worker.terminate()

# Because pytest will reorder the tests based on the method name,
# we implement the whole 'workflow' as one unit test.
def test_restart_channel(deserver_mock_data_block):
    # Verify that nothing is active
    output = de_client_request("--status")
    assert re.search('test_channel.*state = STEADY', output)

    # Take channel offline
    output = de_client_request('--stop-channel', 'test_channel')
    assert output == 'OK'

    # Verify no channels are active
    output = de_client_request("--status")
    assert "No channels are currently active" in output

    # Take channel offline
    output = de_client_request('--start-channel', 'test_channel')
    assert output == 'OK'
