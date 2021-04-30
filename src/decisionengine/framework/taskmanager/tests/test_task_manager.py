import threading
import os

import pytest

import decisionengine.framework.config.policies as policies
from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block  # noqa: F401
from decisionengine.framework.taskmanager.TaskManager import State
from decisionengine.framework.taskmanager.TaskManager import TaskManager

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
        self._thread = threading.Thread(name=name, target=self._tm.run)

    def __enter__(self):
        self._thread.start()
        return self._tm

    def __exit__(self, type, value, traceback):
        if type:
            return False
        self._thread.join()


@pytest.mark.usefixtures("mock_data_block")
def test_task_manager_construction(mock_data_block):  # noqa: F811
    task_manager = task_manager_for('test_channel')
    assert task_manager.state.has_value(State.BOOT)


@pytest.mark.usefixtures("mock_data_block")
def test_take_task_manager_offline(mock_data_block):  # noqa: F811
    with RunChannel('test_channel') as task_manager:
        task_manager.state.wait_until(State.STEADY)
        task_manager.take_offline(None)
        assert task_manager.state.has_value(State.OFFLINE)
        assert task_manager.get_state_value() == State.OFFLINE.value


@pytest.mark.usefixtures("mock_data_block")
def test_failing_publisher(mock_data_block):  # noqa: F811
    task_manager = task_manager_for('failing_publisher')
    task_manager.run()
    assert task_manager.state.has_value(State.OFFLINE)


@pytest.mark.usefixtures("mock_data_block")
def test_bad_datablock(mock_data_block, caplog):  # noqa: F811
    with RunChannel('test_channel') as task_manager:
        task_manager.state.wait_until(State.STEADY)
        task_manager.data_block_put('bad_string', 'header', mock_data_block)
        task_manager.take_offline(None)
        assert "data_block put expecting" in caplog.text


@pytest.mark.usefixtures("mock_data_block")
def test_no_data_to_transform(mock_data_block):  # noqa: F811
    with RunChannel('test_channel') as task_manager:
        task_manager.state.wait_until(State.STEADY)
        task_manager.run_transforms()
        task_manager.run_publishers('action', 'facts')
        task_manager.run_logic_engine()
        task_manager.take_offline(None)
