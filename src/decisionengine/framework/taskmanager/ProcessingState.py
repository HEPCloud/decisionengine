'''
The ProcessingState class can represent any of the following task-manager states:

  BOOT
  STEADY
  OFFLINE
  SHUTTINGDOWN
  SHUTDOWN
  ERROR

In addition, the class supports 'wait_until(state)' and 'wait_while(state)' methods,
which, when called from a different process, block until the state has been entered
or exited, respectively.
'''

import enum
import multiprocessing
import logging

class State(enum.Enum):
    BOOT = 0
    STEADY = 1
    SHUTTINGDOWN = 2
    SHUTDOWN = 3
    OFFLINE = 4
    ERROR = 5


class ProcessingState:
    def __init__(self, state=State.BOOT):
        allowed_state = State(state)
        self._cv = multiprocessing.Condition()
        self._state = multiprocessing.Value('i', allowed_state.value)
        self.logger = logging.getLogger()

    def get(self):
        try:
            value = None
            with self._state.get_lock():
                value = self._state.value
            return State(value)
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def set(self, state):
        try:
            if not isinstance(state, State):
                raise RuntimeError("Supplied value is not a State variable.")
            with self._cv, self._state.get_lock():
                self._state.value = state.value
                self._cv.notify()
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def has_value(self, state):
        try:
            if not isinstance(state, State):
                raise RuntimeError("Supplied value is not a State variable.")
            return self.get() == state
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def wait_until(self, state):
        with self._cv:
            self._cv.wait_for(lambda: self.has_value(state))

    def wait_while(self, state):
        with self._cv:
            self._cv.wait_for(lambda: not self.has_value(state))

    def should_stop(self):
        return self.get().value > State.STEADY.value

    def inactive(self):
        return self.get().value > State.SHUTTINGDOWN.value
