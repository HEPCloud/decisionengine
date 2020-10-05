'''pytest fixtures/constants'''
import mock
import pytest
from pytest_postgresql import factories

from collections import UserDict
import os
import threading

DE_DB_HOST = '127.0.0.1'
DE_DB_USER = 'postgres'
DE_DB_PASS = None
DE_DB_NAME = 'decisionengine'
DE_SCHEMA = [os.path.dirname(os.path.abspath(__file__)) + "/../postgresql.sql", ]

# DE_DB_PORT assigned at random
PG_PROG = factories.postgresql_proc(user=DE_DB_USER, password=DE_DB_PASS,
                                    host=DE_DB_HOST, port=None)
DE_DB = factories.postgresql('PG_PROG', db_name=DE_DB_NAME, load=DE_SCHEMA)


@pytest.fixture
def mock_data_block():
    class MockDataBlock(UserDict):
        def __init__(self, products={}):
            self.lock = threading.Lock()
            self.taskmanager_id = None
            self.generation_id = 1
            self.data = products

        def duplicate(self):
            return MockDataBlock(self.data)

        def put(self, key, product, header, metadata=None):
            self.data[key] = product

    with mock.patch('decisionengine.framework.dataspace.datablock.DataBlock') as mock_data_block:
        mock_data_block.return_value = MockDataBlock()
        yield
