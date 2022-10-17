# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import re
import time

from decisionengine.framework.taskmanager.PublisherStatus import PublisherStatusBoard


def test_publisher_status_board():
    board = PublisherStatusBoard(["a", "b"])
    snapshot = board.snapshot()
    a1_enabled, _, a1_since = snapshot.state("a")
    b1_enabled, _, b1_since = snapshot.state("b")
    assert a1_enabled and b1_enabled

    board.update("a", False)

    a2_enabled, _, a2_since = snapshot.state("a")
    b2_enabled, _, b2_since = snapshot.state("b")
    assert not a2_enabled and b2_enabled
    assert a2_since > a1_since
    assert b2_since == b1_since

    re.search(r"a\s+False.*b\s+True", str(snapshot), re.DOTALL)

    time.sleep(2)
    assert board.snapshot().state("a").duration.seconds >= 2
