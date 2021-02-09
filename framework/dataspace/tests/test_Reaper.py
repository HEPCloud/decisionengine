import mock
import time
import unittest

import decisionengine.framework.dataspace.dataspace as dataspace

GLOBAL_CONFIG = {
    "dataspace": {
        "datasource": {
            "module": "decisionengine.framework.dataspace.datasources.postgresql",
            "name": "Postgresql",
            "config": {
                "user": "decisionengine",
                "blocking": True,
                "host": "decisionengine",
                "port": 5435,
                "database": "decisionengine",
                "maxconnections": 100,
                "maxcached": 10,
            },
        },
    },
}


class MockSource(object):

    def delete_data_older_than(self, day):
        pass


class TestReaper(unittest.TestCase):

    def setUp(self):
        with mock.patch.object(dataspace.DataSourceLoader, "create_datasource") as source:
            source.return_value = MockSource()
            GLOBAL_CONFIG["dataspace"]["retention_interval_in_days"] = 365
            self.reaper = dataspace.Reaper(GLOBAL_CONFIG)

    def tearDown(self):
        '''
            Make sure we don't leave any dangling reapers around
        '''
        try:
            self.reaper.stop()
        except Exception:
            pass

    def test_reap(self):
        self.assertEqual(self.reaper.get_state(),
                         dataspace.State.IDLE)
        self.reaper.reap()

    def test_start_stop(self):
        self.reaper.start()
        time.sleep(0.5)  # make sure scheduler has time to set state
        self.assertTrue(self.reaper.get_state() in (dataspace.State.RUNNING, dataspace.State.SLEEPING))
        self.reaper.stop()
        time.sleep(0.5)  # make sure scheduler has time to set state
        self.assertEqual(self.reaper.get_state(), dataspace.State.STOPPED)

    def test_start_stop_delay(self):
        self.reaper.start(delay=90)
        time.sleep(0.5)  # make sure scheduler has time to set state
        self.assertEqual(self.reaper.get_state(), dataspace.State.STARTING)
        self.reaper.stop()
        time.sleep(0.5)  # make sure scheduler has time to set state
        self.assertEqual(self.reaper.get_state(), dataspace.State.STOPPED)

    def test_loop(self):
        for _ in range(3):
            self.reaper.start()
            time.sleep(0.5)  # make sure scheduler has time to set state
            self.assertTrue(self.reaper.get_state() in (dataspace.State.RUNNING, dataspace.State.SLEEPING))
            self.reaper.stop()
            time.sleep(0.5)  # make sure scheduler has time to set state
            self.assertEqual(self.reaper.get_state(), dataspace.State.STOPPED)

    def test_fail_missing_config_key(self):
        with self.assertRaises(dataspace.DataSpaceConfigurationError):
            with mock.patch.object(dataspace.DataSourceLoader, "create_datasource") as source:
                source.return_value = MockSource()
                del GLOBAL_CONFIG["dataspace"]["retention_interval_in_days"]
                dataspace.Reaper(GLOBAL_CONFIG)

    def test_fail_wrong_config_key(self):
        with self.assertRaises(ValueError):
            with mock.patch.object(dataspace.DataSourceLoader, "create_datasource") as source:
                source.return_value = MockSource()
                GLOBAL_CONFIG["dataspace"]["retention_interval_in_days"] = "abc"
                dataspace.Reaper(GLOBAL_CONFIG)

    def test_source_fail(self):
        with mock.patch.object(MockSource, "delete_data_older_than") as function:
            function.side_effect = KeyError
            self.reaper.start()
            time.sleep(1)  # make sure stack trace bubbles up before checking state
            self.assertEqual(self.reaper.get_state(), dataspace.State.ERROR)
            self.reaper.stop()
            time.sleep(0.5)  # make sure scheduler has time to set state
            self.assertEqual(self.reaper.get_state(), dataspace.State.ERROR)

            function.side_effect = None
            self.reaper.start()
            time.sleep(0.5)  # make sure scheduler has time to set state
            self.assertTrue(self.reaper.get_state() in (dataspace.State.RUNNING, dataspace.State.SLEEPING))
            self.reaper.stop()
            time.sleep(0.5)  # make sure scheduler has time to set state
            self.assertEqual(self.reaper.get_state(), dataspace.State.STOPPED)


if __name__ == '__main__':
    unittest.main()
