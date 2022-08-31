# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import time


class Countdown:
    """
    Countdown is a context manager that keeps track of elapsed time.

    It is designed to be used for cases where a sequence of operations
    should not take longer than a specified period of time.  This is done
    by occasionally querying the 'time_left' attribute (e.g.):

    .. code-block:: python

        countdown = Countdown(wait_up_to=10)
        for p in processes:
            with countdown:
                rc = p.join(countdown.time_left)
                if rc is None:
                    p.terminate()

    In the above example, the time it takes to shutdown all processes
    should not exceed 10 seconds.  Upon entering the countdown
    context, a timer starts.  Once that context is exited, the timer
    stops and the elapsed time is subtracted from the initial
    'wait_up_to' value.  If it takes 10 seconds for the first process
    to join, then the 'time_left' value will be 0 when joining all
    subsequent processes.  In this way, the entire sequence of
    operations is constrained to occur in roughly 10 seconds.
    """

    def __init__(self, wait_up_to):
        """
        :type wait_up_to: float or None
        :param wait_up_to: Countdown start time in seconds.  If None
                           is specified, no countdown occurs and the ~time_left
                           variable remains `None` (useful when needing to
                           call a blocking join on a process/thread).
        """
        self.time_left = wait_up_to
        self._elapsed_time = None

    def __enter__(self):
        if self.time_left is not None:
            self._elapsed_time = time.monotonic()
        return self

    def __exit__(self, type, value, traceback):
        if self.time_left is None:
            return

        self._elapsed_time = time.monotonic() - self._elapsed_time
        self.time_left = max(0, self.time_left - self._elapsed_time)
