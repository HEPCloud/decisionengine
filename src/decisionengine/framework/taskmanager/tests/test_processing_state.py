# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import multiprocessing
import time

import pytest

from decisionengine.framework.taskmanager.ProcessingState import (
    INACTIVE_CONDITIONS,
    ProcessingState,
    RUNNING_CONDITIONS,
    State,
    STOPPING_CONDITIONS,
)


class Worker(multiprocessing.Process):
    def __init__(self, state):
        super().__init__(name="TestWorker")
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
    with pytest.raises(Exception, match="1\\.3 is not a valid State"):
        ProcessingState(1.3)


def test_has_lock_and_can_context():
    state = ProcessingState()
    with state.lock:
        return True


def test_cannot_redefine_lock():
    state = ProcessingState()
    with pytest.raises(ValueError):
        state.lock = "bad_string"


def test_wrong_value_on_assignment():
    state = ProcessingState()
    with pytest.raises(Exception, match="Supplied value is not a State variable"):
        state.set(1.3)


def test_wrong_value_has_value():
    state = ProcessingState()
    with pytest.raises(RuntimeError):
        state.has_value("asdf")


def test_wrong_value_has_value_list():
    state = ProcessingState()
    with pytest.raises(RuntimeError):
        state.has_value((State.STEADY, "jkl"))


def test_wait_until():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_until(State.STEADY)
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_until_list():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_until((State.STEADY, State.IDLE))
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_until_has_timeout():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_until(State.STEADY, 4)
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_while():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_while(State.BOOT)
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_while_list():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_while((State.BOOT, State.IDLE))
    assert state.has_value(State.STEADY)
    worker.join()


def test_wait_while_has_timeout():
    state = ProcessingState()
    worker = Worker(state)
    worker.start()
    state.wait_while(State.BOOT, 4)
    assert state.has_value(State.STEADY)
    worker.join()


def test_probably_running():
    state = ProcessingState()
    for set_to in RUNNING_CONDITIONS:
        state.set(set_to)
        assert state.probably_running()


def test_should_stop():
    state = ProcessingState()
    for set_to in STOPPING_CONDITIONS:
        state.set(set_to)
        assert state.should_stop()


def test_inactive():
    state = ProcessingState()
    for set_to in INACTIVE_CONDITIONS:
        state.set(set_to)
        assert state.inactive()
