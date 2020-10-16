import multiprocessing
import time

import pytest

from decisionengine.framework.taskmanager.ProcessingState import State
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState


class Worker(multiprocessing.Process):
    def __init__(self, state):
        super().__init__()
        self._state = state

    def run(self):
        time.sleep(2)
        self._state.set(State.STEADY)


def test_shared_state_construction():
    state = ProcessingState()
    assert state.has_value(State.BOOT)
    state = ProcessingState(State.STEADY)
    assert state.has_value(State.STEADY)


def test_wrong_value_on_creation():
    with pytest.raises(Exception, match='1\\.3 is not a valid State'):
        ProcessingState(1.3)


def test_wrong_value_on_assignment():
    state = ProcessingState()
    with pytest.raises(Exception, match='Supplied value is not a State variable'):
        state.set(1.3)


def test_wait_until():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_until(State.STEADY)
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_while():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_while(State.BOOT)
    assert state.has_value(State.STEADY)
    worker.join()
