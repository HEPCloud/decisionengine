'''
The ProcessingState class can represent any of the following task-manager states:

  BOOT
  IDLE
  ACTIVE
  STEADY
  OFFLINE
  SHUTTINGDOWN
  SHUTDOWN
  ERROR

In addition, the class supports 'wait_until(state)' and 'wait_while(state)' methods,
which, when called from a different process, block until the state has been entered
or exited, respectively.

The 'RUNNING_CONDITIONS' list is a list of states that a thread may have if it is started/starting.
The 'STOPPING_CONDITIONS' list is a list of states that a thread may have if it is stopped/stopping.
The 'INACTIVE_CONDITIONS' list is a list of states that a thread may have when it is not active
'''

import enum
import multiprocessing
import logging

class State(enum.Enum):
    BOOT = 0
    IDLE = 1
    ACTIVE = 2
    STEADY = 3
    SHUTTINGDOWN = 4
    SHUTDOWN = 5
    OFFLINE = 6
    ERROR = 7


RUNNING_CONDITIONS = (State.BOOT, State.IDLE, State.ACTIVE, State.STEADY)
STOPPING_CONDITIONS = (State.SHUTTINGDOWN, State.SHUTDOWN, State.OFFLINE, State.ERROR)
INACTIVE_CONDITIONS = (State.OFFLINE, State.ERROR)


class ProcessingState:
    """
    This object tracks the state of a process.

    A number of convience wrappers are provided.

    Additionally you may use the `.lock` attribute for `with` block
    to lock the state during specific operations.
    """
    def __init__(self, state=State.BOOT):
        allowed_state = State(state)
        self._cv = multiprocessing.Condition()
        self._lock = multiprocessing.RLock()
        self._state = multiprocessing.Value('i', allowed_state.value)
        self.logger = logging.getLogger()

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, value):
        raise ValueError("You may not redefine the ProcessingState lock")

    def get(self):
        """
        This function is a minimally locking check to fetch the state.
        """
        try:
            value = None
            with self._state.get_lock():
                value = self._state.value
            return State(value)
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def set(self, state):
        """
        This function will lock (and possibly block) to ensure a consistent
        change to the state value.

        This function can be blocked using the `.lock` to force state
        sync between threads if need be.
        """
        try:
            if not isinstance(state, State):
                raise RuntimeError("Supplied value is not a State variable.")
            with self.lock:  # don't hold other locks if we can't get this one
                with self._cv, self._state.get_lock():
                    self._state.value = state.value
                    self._cv.notify()
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def has_value(self, state):
        try:
            if not isinstance(state, State) and not isinstance(state, (list, tuple)):
                raise RuntimeError("Supplied value is not a State variable or list of State values.")
            if isinstance(state, (list, tuple)):
                return True in map(self.has_value, state)
            else:
                return self.get() == state
        except Exception:
            self.logger.exception("Unexpected error!")
            raise

    def wait_until(self, state, timeout=None):
        with self._cv:
            self._cv.wait_for(lambda: self.has_value(state), timeout)

    def wait_while(self, state, timeout=None):
        with self._cv:
            self._cv.wait_for(lambda: not self.has_value(state), timeout)

    def probably_running(self):
        return self.has_value(RUNNING_CONDITIONS)

    def should_stop(self):
        return self.has_value(STOPPING_CONDITIONS)

    def inactive(self):
        return self.has_value(INACTIVE_CONDITIONS)
