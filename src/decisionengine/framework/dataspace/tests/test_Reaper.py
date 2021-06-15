import logging
import time

import mock
import pytest
import unittest

import decisionengine.framework.dataspace.dataspace as dataspace
from decisionengine.framework.dataspace.maintain import Reaper
from decisionengine.framework.taskmanager.ProcessingState import State
from decisionengine.framework.dataspace.datasources.null import NullDataSource


class TestReaper(unittest.TestCase):
    logger = logging.getLogger()

    def setUp(self):
        # use the null datasource so we don't have to patch out the behavior
        self.config = {
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
        self.reaper = Reaper(self.config)

    def tearDown(self):
        # Make sure there are no dangling reapers
        try:
            if self.reaper.thread.is_alive() or not self.reaper.state.should_stop():
                self.reaper.state.set(State.OFFLINE)
                time.sleep(0.5)
        except Exception:
            pass

    def test_reap_default_state(self):
        self.assertEqual(self.reaper.state.get(), State.BOOT)

    def test_reaper_can_reap(self):
        self.reaper.reap()

    def test_just_stop_no_error(self):
        self.reaper.stop()

    def test_start_stop(self):
        self.reaper.start()
        self.assertIn(self.reaper.state.get(), (State.IDLE, State.ACTIVE, State.STEADY))

        self.reaper.stop()
        self.assertIn(self.reaper.state.get(), (State.SHUTTINGDOWN, State.SHUTDOWN))

    def test_start_stop_stop(self):
        self.reaper.start()
        self.assertIn(self.reaper.state.get(), (State.IDLE, State.ACTIVE, State.STEADY))

        self.reaper.stop()
        self.assertIn(self.reaper.state.get(), (State.SHUTTINGDOWN, State.SHUTDOWN))

        self.logger.debug("running second stop")
        self.reaper.stop()
        self.assertIn(self.reaper.state.get(), (State.SHUTTINGDOWN, State.SHUTDOWN))

    def test_state_can_be_active(self):
        def sleepnow(arg1=None, arg2=None):
            time.sleep(3)

        with mock.patch.object(NullDataSource, "delete_data_older_than", new=sleepnow):
            self.reaper.start()
            time.sleep(0.5)  # make sure reaper has a chance to get the lock
            self.assertEqual(self.reaper.state.get(), State.ACTIVE)

    @pytest.mark.timeout(20)
    def test_state_sets_timer_and_uses_it(self):
        def sleepnow(arg1=None, arg2=None):
            time.sleep(3)

        with mock.patch.object(NullDataSource, "delete_data_older_than", new=sleepnow):
            self.reaper.MIN_SECONDS_BETWEEN_RUNS = 1
            self.reaper.seconds_between_runs = 1
            self.reaper.start(delay=2)
            self.assertEqual(self.reaper.seconds_between_runs, 1)
            self.reaper.state.wait_while(State.IDLE)  # Make sure the reaper started
            self.assertEqual(self.reaper.state.get(), State.ACTIVE)
            self.reaper.state.wait_while(State.ACTIVE)  # let the reaper finish its scan
            self.reaper.state.wait_while(State.IDLE)    # Make sure the reaper started a second time
            self.reaper.state.wait_while(State.ACTIVE)  # let the reaper finish its scan

    def test_start_delay(self):
        self.reaper.start(delay=90)
        self.assertEqual(self.reaper.state.get(), State.IDLE)

    @pytest.mark.timeout(20)
    def test_loop_of_start_stop_in_clumps(self):
        for _ in range(3):
            self.logger.debug(f"run {_} of rapid start/stop")
            self.reaper.start()
            self.assertIn(self.reaper.state.get(), (State.IDLE, State.ACTIVE, State.STEADY))
            self.reaper.stop()
            self.assertIn(self.reaper.state.get(), (State.SHUTTINGDOWN, State.SHUTDOWN))

    def test_fail_small_retain(self):
        with self.assertRaises(ValueError):
            self.reaper.retention_interval = 1

    def test_fail_small_run_interval(self):
        with self.assertRaises(ValueError):
            self.reaper.seconds_between_runs = 1

    def test_fail_start_two_reapers(self):
        self.reaper.start()
        self.assertIn(self.reaper.state.get(), (State.IDLE, State.ACTIVE, State.STEADY))
        with self.assertRaises(RuntimeError):
            self.logger.debug("running second start")
            self.reaper.start()

    def test_fail_missing_config(self):
        with self.assertRaises(dataspace.DataSpaceConfigurationError):
            test_config = self.config.copy()
            del test_config["dataspace"]
            Reaper(test_config)

    def test_fail_bad_config(self):
        with self.assertRaises(dataspace.DataSpaceConfigurationError):
            test_config = self.config.copy()
            test_config["dataspace"] = "somestring"
            Reaper(test_config)

    def test_fail_missing_config_key(self):
        with self.assertRaises(dataspace.DataSpaceConfigurationError):
            test_config = self.config.copy()
            del test_config["dataspace"]["retention_interval_in_days"]
            Reaper(test_config)

    def test_fail_wrong_config_key(self):
        with self.assertRaises(ValueError):
            test_config = self.config.copy()
            test_config["dataspace"]["retention_interval_in_days"] = "abc"
            Reaper(test_config)

    @pytest.mark.timeout(20)
    def test_source_fail_can_be_fixed(self):
        with mock.patch.object(NullDataSource, "delete_data_older_than") as function:
            function.side_effect = KeyError
            self.reaper.start()
            time.sleep(1)  # make sure stack trace bubbles up before checking state
            self.assertEqual(self.reaper.state.get(), State.ERROR)

            self.reaper.stop()
            self.assertEqual(self.reaper.state.get(), State.ERROR)

            function.side_effect = None
            self.reaper.start(delay=30)
            self.assertEqual(self.reaper.state.get(), State.IDLE)

            self.reaper.stop()
            self.assertEqual(self.reaper.state.get(), State.SHUTDOWN)
