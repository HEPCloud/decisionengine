# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import time

from decisionengine.framework.util.countdown import Countdown


def test_timeout_of_none():
    countdown = Countdown(wait_up_to=None)
    assert countdown.time_left is None
    for i in range(10):
        with countdown:
            time.sleep(0.1)
    assert countdown.time_left is None


def test_timeout():
    countdown = Countdown(wait_up_to=2)
    with countdown:
        time.sleep(2)
    assert countdown.time_left == 0.0
