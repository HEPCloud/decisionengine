import mock
import os
import pytest
import unittest

import decisionengine.framework.dataspace.datasource as datasource
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

    def delete_old_data(self, interval):
        pass


class TestReaper(unittest.TestCase):

    def setUp(self):
        self.reaper = dataspace.Reaper(GLOBAL_CONFIG)

    def tearDown(self):
        pass

    def test_reaper(self):
        with mock.patch.object(dataspace.DataSourceLoader, "create_datasource") as source:
            source.return_value = MockSource()
        self.reaper.reap()

if __name__ == '__main__':
    unittest.main()
