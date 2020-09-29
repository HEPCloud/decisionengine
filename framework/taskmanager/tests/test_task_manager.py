from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _start_de_server, parse_program_options
from decisionengine.framework.taskmanager.TaskManager import TaskManager, State
from decisionengine.framework.util.sockets import get_random_port

import os
import pytest
import threading
import time
import uuid

_CWD = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_CWD, "../../tests/etc/decisionengine")
_CHANNEL_CONFIG_DIR = os.path.join(_CONFIG_PATH, 'config.d')

_port = get_random_port()

@pytest.fixture(scope="module")
def config():
    global_config, channel_config_handler = _get_de_conf_manager(_CONFIG_PATH,
                                                                 _CHANNEL_CONFIG_DIR,
                                                                 parse_program_options([f'--port={_port}']))
    channel_config_handler.load_all_channels()
    return (global_config, channel_config_handler.get_channels())

def run(task_manager):
    task_manager.run()

def test_task_manager_construction(config):
    global_config, channel_configs = config
    generation_id = 1
    assert len(channel_configs) == 1
    channel_name = list(channel_configs.keys())[0]
    assert channel_name == 'test_channel'
    task_manager = TaskManager(channel_name,
                               generation_id,
                               channel_configs[channel_name],
                               global_config)
    assert task_manager.get_state() == State.BOOT
    thread = threading.Thread(target=run,
                              args=(task_manager,))
    thread.start()
    time.sleep(3)
    assert task_manager.get_state() == State.STEADY
    task_manager._take_offline(None)
    assert task_manager.get_state() == State.OFFLINE
    thread.join()
