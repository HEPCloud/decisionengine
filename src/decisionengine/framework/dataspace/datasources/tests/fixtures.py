"""pytest fixtures/constants"""
import os
import threading
from collections import UserDict

import mock
import pytest

from pytest_postgresql import factories

DE_DB_HOST = "127.0.0.1"
DE_DB_USER = "postgres"
DE_DB_PASS = None
DE_DB_NAME = "decisionengine"
DE_SCHEMA = [
    os.path.dirname(os.path.abspath(__file__)) + "/../postgresql.sql",
]

# DE_DB_PORT assigned at random
PG_PROG = factories.postgresql_proc(user=DE_DB_USER, password=DE_DB_PASS, host=DE_DB_HOST, port=None)
DE_DB = factories.postgresql("PG_PROG", dbname=DE_DB_NAME, load=DE_SCHEMA)


@pytest.fixture
def mock_data_block():
    """
    This fixture replaces the standard datablock implementation.

    The current DataBlock implementation does not own any data
    products but forwards them immediately to a backend datasource.
    The only implemented datasource requires Postgres, which is
    overkill when needing to test simple data-product communication
    between modules.

    This mock datablock class directly owns the data products, thus
    avoiding the need for a datasource backend.  It is anticipated
    that a future design of the DataBlock will own the data products,
    thus making this mock class unnecessary.
    """

    class MockDataBlock(UserDict):
        def __init__(self, products=None):
            super().__init__()
            self.lock = threading.Lock()
            self.taskmanager_id = None
            self.generation_id = 1
            if products:
                self.data = products
            else:
                self.data = {}

        def duplicate(self):
            return MockDataBlock(self.data)

        def put(self, key, product, header, metadata=None):
            self.data[key] = product

    with mock.patch("decisionengine.framework.dataspace.datablock.DataBlock") as my_mock_data_block:
        my_mock_data_block.return_value = MockDataBlock()
        yield
