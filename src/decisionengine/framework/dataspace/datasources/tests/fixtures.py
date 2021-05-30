"""pytest fixtures/constants"""
import datetime
import os
import threading
from collections import UserDict

import mock
import pytest

from pytest_postgresql import factories

from decisionengine.framework.dataspace.datablock import Header, Metadata

__all__ = [
    "DATABASES_TO_TEST",
    "PG_PROG",
    "PG_DE_DB_WITH_SCHEMA",
    "mock_data_block",
]

# DE_DB_PORT assigned at random
PG_PROG = factories.postgresql_proc(
    user="postgres", password=None, host="127.0.0.1", port=None
)
PG_DE_DB_WITH_SCHEMA = factories.postgresql(
    "PG_PROG",
    dbname="decisionengine",
    load=[
        os.path.dirname(os.path.abspath(__file__)) + "/../postgresql.sql",
    ],
)

DATABASES_TO_TEST = ("PG_DE_DB_WITH_SCHEMA",)


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
        """Just a fake datablock"""

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
            """Simple behavior"""
            return MockDataBlock(self.data)

        def put(self, key, product, header, metadata=None):  # pylint: disable=unused-argument
            """Simple behavior"""
            self.data[key] = product

    with mock.patch("decisionengine.framework.dataspace.datablock.DataBlock") as my_mock_data_block:
        my_mock_data_block.return_value = MockDataBlock()
        yield


def load_sample_data_into_datasource(schema_only_db):
    """
    load our sample test data into a dataspace
    This is a function not a fixture so you can
    run it on any datasource providing the right API.
    """
    _pk = schema_only_db.store_taskmanager(
        "taskmanager1",
        "11111111-1111-1111-1111-111111111111",
        datetime.datetime(2016, 3, 14),
    )  # _pk=1 probably
    header = Header(_pk)
    metadata = Metadata(_pk)
    schema_only_db.insert(
        _pk, 1, "my_test_key", "my_test_value".encode(), header, metadata
    )
    schema_only_db.insert(
        _pk, 1, "a_test_key", "a_test_value".encode(), header, metadata
    )

    _pk = schema_only_db.store_taskmanager(
        "taskmanager2", "22222222-2222-2222-2222-222222222222"
    )  # _pk=2 probably
    header = Header(_pk)
    metadata = Metadata(_pk)
    schema_only_db.insert(
        _pk, 2, "other_test_key", "other_test_value".encode(), header, metadata
    )

    # return the connection now that it isn't just the schema
    return schema_only_db
