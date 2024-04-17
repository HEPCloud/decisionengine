# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest
import redis


def _redis_server_running() -> bool:
    r = redis.Redis("127.0.0.1", socket_timeout=0.1)
    try:
        r.ping()
        return True
    except Exception:
        return False


def pytest_runtest_call(item):
    if item.get_closest_marker("redis") is not None:
        if not _redis_server_running():
            pytest.skip("No redis server running at default broker url")
