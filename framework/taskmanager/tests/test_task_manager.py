import os
import multiprocessing
import time

from decisionengine.framework.config.ValidConfig import ValidConfig
import decisionengine.framework.config.policies as policies
from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block # noqa: F401
from decisionengine.framework.taskmanager.TaskManager import TaskManager, State

_CWD = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_CWD, "../../tests/etc/decisionengine")
_CHANNEL_CONFIG_DIR = os.path.join(_CWD, 'channels')

_global_config = ValidConfig(policies.global_config_file(_CONFIG_PATH))


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


def test_task_manager_construction(mock_data_block): # noqa: F811
    task_manager = task_manager_for('test_channel')
    assert task_manager.get_state() == State.BOOT

def test_take_task_manager_offline(mock_data_block): # noqa: F811
    with RunChannel('test_channel') as task_manager:
        time.sleep(2)
        assert task_manager.get_state() == State.STEADY
        task_manager._take_offline(None)
        assert task_manager.get_state() == State.OFFLINE

def test_failing_publisher(mock_data_block): # noqa: F811
    with RunChannel('failing_publisher') as task_manager:
        time.sleep(2)
        assert task_manager.get_state() == State.OFFLINE
