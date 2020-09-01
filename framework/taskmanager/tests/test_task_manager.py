from collections import UserDict
import mock
import os
import multiprocessing
import pytest
import threading
import time

from decisionengine.framework.config.ValidConfig import ValidConfig
import decisionengine.framework.config.policies as policies
from decisionengine.framework.taskmanager.TaskManager import TaskManager, State
import decisionengine.framework.dataspace.datablock

_CWD = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_CWD, "../../tests/etc/decisionengine")
_CHANNEL_CONFIG_DIR = os.path.join(_CWD, 'channels')

_global_config = ValidConfig(policies.global_config_file(_CONFIG_PATH))

class MockDataBlock(UserDict):
    def __init__(self, products={}):
        self.lock = threading.Lock()
        self.taskmanager_id = None
        self.generation_id = 1
        self.data = products

    def duplicate(self):
        return MockDataBlock(self.data)

    def put(self, key, product, header, metadata=None):
        self.data[key] = product

@pytest.fixture
def mock_data_block():
    with mock.patch('decisionengine.framework.dataspace.datablock.DataBlock') as mock_data_block:
        mock_data_block.return_value = MockDataBlock()
        yield


def channel_config(name):
    return ValidConfig(os.path.join(_CHANNEL_CONFIG_DIR, name + '.jsonnet'))

def task_manager_for(name):
    return TaskManager(name, 1, channel_config(name), _global_config)

class RunChannel:
    def __init__(self, name):
        self._tm = task_manager_for(name)
        self._process = multiprocessing.Process(target=self._tm.run)

    def __enter__(self):
        self._process.start()
        return self._tm

    def __exit__(self, type, value, traceback):
        self._process.join()
        if type:
            return False

def test_task_manager_construction(mock_data_block):
    task_manager = task_manager_for('test_channel')
    assert task_manager.get_state() == State.BOOT

def test_take_task_manager_offline(mock_data_block):
    with RunChannel('test_channel') as task_manager:
        time.sleep(2)
        assert task_manager.get_state() == State.STEADY
        task_manager._take_offline(None)
        assert task_manager.get_state() == State.OFFLINE

def test_failing_publisher(mock_data_block):
    with RunChannel('failing_publisher') as task_manager:
        time.sleep(2)
        assert task_manager.get_state() == State.OFFLINE
