# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import contextlib
import gc
import logging
import time

from unittest import mock

import pytest

import decisionengine.framework.dataspace.dataspace as dataspace

from decisionengine.framework.dataspace.datasources.null import NullDataSource
from decisionengine.framework.dataspace.maintain import Reaper
from decisionengine.framework.taskmanager.ProcessingState import State

logger = logging.getLogger()


@pytest.fixture()
def config():

    yield {
        "dataspace": {
            "retention_interval_in_days": 365,
            "datasource": {
                "module": "decisionengine.framework.dataspace.datasources.null",
                "name": "NullDataSource",
                "config": {
                    "key": "value",
                },
            },
        },
    }


@pytest.fixture()
def reaper(request):
    config_fixture = request.getfixturevalue("config")
    reaper = Reaper(config_fixture)

    yield reaper

    with contextlib.suppress(Exception):
        if reaper.thread.is_alive() or not reaper.state.should_stop():
            reaper.state.set(State.OFFLINE)
            reaper.thread.join(timeout=1)

    del reaper
    gc.collect()


def test_reap_default_state(reaper):
    assert reaper.state.get() == State.BOOT


def test_reaper_can_reap(reaper):
    reaper.reap()


def test_just_stop_no_error(reaper):
    reaper.stop()


def test_start_stop(reaper):
    reaper.start()
    assert reaper.state.get() in (State.IDLE, State.ACTIVE, State.STEADY)

    reaper.stop()
    assert reaper.state.get() in (State.SHUTTINGDOWN, State.SHUTDOWN)


def test_start_stop_stop(reaper):
    reaper.start()
    assert reaper.state.get() in (State.IDLE, State.ACTIVE, State.STEADY)

    reaper.stop()
    assert reaper.state.get() in (State.SHUTTINGDOWN, State.SHUTDOWN)

    logger.debug("running second stop")
    reaper.stop()
    assert reaper.state.get() in (State.SHUTTINGDOWN, State.SHUTDOWN)


def test_state_can_be_active(reaper):
    def sleepnow(arg1=None, arg2=None):
        time.sleep(3)

    with mock.patch.object(NullDataSource, "delete_data_older_than", new=sleepnow):
        reaper.start()
        time.sleep(0.5)  # make sure reaper has a chance to get the lock
        assert reaper.state.get() == State.ACTIVE


@pytest.mark.timeout(20)
def test_state_sets_timer_and_uses_it(reaper):
    def sleepnow(arg1=None, arg2=None):
        time.sleep(3)

    with mock.patch.object(NullDataSource, "delete_data_older_than", new=sleepnow):
        reaper.MIN_SECONDS_BETWEEN_RUNS = 1
        reaper.seconds_between_runs = 1
        reaper.start(delay=2)
        assert reaper.seconds_between_runs == 1
        reaper.state.wait_while(State.IDLE)  # Make sure the reaper started
        assert reaper.state.get() == State.ACTIVE
        reaper.state.wait_while(State.ACTIVE)  # let the reaper finish its scan
        reaper.state.wait_while(State.IDLE)  # Make sure the reaper started a second time
        reaper.state.wait_while(State.ACTIVE)  # let the reaper finish its scan


def test_start_delay(reaper):
    reaper.start(delay=90)
    assert reaper.state.get() == State.IDLE


@pytest.mark.timeout(20)
def test_loop_of_start_stop_in_clumps(reaper):
    for _ in range(3):
        logger.debug(f"run {_} of rapid start/stop")
        reaper.start()
        assert reaper.state.get() in (State.IDLE, State.ACTIVE, State.STEADY)
        reaper.stop()
        assert reaper.state.get() in (State.SHUTTINGDOWN, State.SHUTDOWN)


def test_fail_small_retain(reaper):
    with pytest.raises(ValueError):
        reaper.retention_interval = 1


def test_fail_small_run_interval(reaper):
    with pytest.raises(ValueError):
        reaper.seconds_between_runs = 1


def test_fail_start_two_reapers(reaper):
    reaper.start()
    assert reaper.state.get() in (State.IDLE, State.ACTIVE, State.STEADY)
    logger.debug("running second start")
    with pytest.raises(RuntimeError):
        reaper.start()


def test_fail_missing_config(reaper, config):
    del config["dataspace"]
    with pytest.raises(dataspace.DataSpaceConfigurationError):
        Reaper(config)


def test_fail_bad_config(reaper, config):
    config["dataspace"] = "somestring"
    with pytest.raises(dataspace.DataSpaceConfigurationError):
        Reaper(config)


def test_fail_missing_config_key(reaper, config):
    del config["dataspace"]["retention_interval_in_days"]
    with pytest.raises(dataspace.DataSpaceConfigurationError):
        Reaper(config)


def test_fail_wrong_config_key(reaper, config):
    config["dataspace"]["retention_interval_in_days"] = "abc"
    with pytest.raises(ValueError):
        Reaper(config)


@pytest.mark.timeout(20)
def test_source_fail_can_be_fixed(reaper):
    with mock.patch.object(NullDataSource, "delete_data_older_than") as function:
        function.side_effect = KeyError
        reaper.start()
        time.sleep(1)  # make sure stack trace bubbles up before checking state
        assert reaper.state.get() == State.ERROR

        reaper.stop()
        assert reaper.state.get() == State.ERROR

        function.side_effect = None
        reaper.start(delay=30)
        assert reaper.state.get() == State.IDLE

        reaper.stop()
        assert reaper.state.get() == State.SHUTDOWN
