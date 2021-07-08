"""pytest fixtures/constants"""
import datetime
import gc
import logging
import os
import threading
from collections import UserDict

from unittest import mock
import pytest

from pytest_postgresql import factories

from decisionengine.framework.dataspace.datablock import Header, Metadata

from decisionengine.framework.dataspace.datasources.postgresql import (
    Postgresql as Postgresql_datasource,
)

__all__ = [
    "DATABASES_TO_TEST",
    "PG_PROG",
    "PG_DE_DB_WITH_SCHEMA",
    "PG_DE_DB_WITHOUT_SCHEMA",
    "SQLALCHEMY_PG_WITH_SCHEMA",
    "SQLALCHEMY_IN_MEMORY_SQLITE",
    "datasource",
    "mock_data_block",
]

# DE_DB_PORT assigned at random
PG_PROG = factories.postgresql_proc(
    user="postgres", password=None, host="127.0.0.1", port=None, postgres_options="-N 1000",
)
PG_DE_DB_WITHOUT_SCHEMA = factories.postgresql(
    "PG_PROG",
    dbname="decisionengine",
)

DATABASES_TO_TEST = ("PG_DE_DB_WITH_SCHEMA",)


@pytest.fixture
@pytest.mark.usefixtures("PG_DE_DB_WITHOUT_SCHEMA")
def PG_DE_DB_WITH_SCHEMA(request):
    """
    Load our PG schema into the database via this fixture
    so pytest knows the limitations on parallel usage of this
    databse scope.
    """
    connection = request.getfixturevalue("PG_DE_DB_WITHOUT_SCHEMA")
    with open(os.path.dirname(os.path.abspath(__file__)) + "/../postgresql.sql", 'r') as _fd:
        with connection.cursor() as cursor:
            cursor.execute(_fd.read())
    connection.commit()
    yield connection

    connection.close()
    del connection

    gc.collect()

@pytest.fixture
def SQLALCHEMY_PG_WITH_SCHEMA(request):
    """
    Get a blank database from pytest_postgresql.
    Then setup the SQLAlchemy style URL with that DB.
    The SQLAlchemyDS will create the schema as needed.
    """
    conn_fixture = request.getfixturevalue("PG_DE_DB_WITHOUT_SCHEMA")

    db_info = {}
    try:
        # psycopg2
        db_info["host"] = conn_fixture.info.host
        db_info["port"] = conn_fixture.info.port
        db_info["user"] = conn_fixture.info.user
        db_info["password"] = conn_fixture.info.password
        db_info["database"] = conn_fixture.info.dbname
    except AttributeError:
        # psycopg2cffi
        for element in conn_fixture.dsn.split():
            (key, value) = element.split("=")
            if value != "''" and value != '""':
                db_info[key] = value
            else:
                db_info[key] = ''

    # echo will log all the sql commands to log.debug
    yield {
        "url": f"postgresql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}",
        "echo": True,
    }


@pytest.fixture
def SQLALCHEMY_IN_MEMORY_SQLITE(request):
    """
    Setup an SQLite database in memory
    Then setup the SQLAlchemy style URL with that DB.
    The SQLAlchemyDS will create the schema as needed.
    """
    yield {"url": "sqlite:///:memory:", "echo": True}

@pytest.fixture(params=DATABASES_TO_TEST)
def datasource(request):
    """
    This parameterized fixture will setup up various datasources.

    Add datasource objects to DATASOURCES_TO_TEST once they've got
    our basic schema loaded.  And adjust our `if` statements here
    until we are SQLAlchemy only.

    Pytest should take it from there and automatically run it
    through all the tests using this fixture.
    """
    conn_fixture = request.getfixturevalue(request.param)

    db_info = {}
    try:
        # SQL Alchemy
        db_info["url"] = conn_fixture["url"]
        db_info["echo"] = True  # put SQLAlchemy into extra chatty mode
    except TypeError:
        try:
            # psycopg2
            db_info["host"] = conn_fixture.info.host
            db_info["port"] = conn_fixture.info.port
            db_info["user"] = conn_fixture.info.user
            db_info["password"] = conn_fixture.info.password
            db_info["database"] = conn_fixture.info.dbname
        except AttributeError:
            # psycopg2cffi
            for element in conn_fixture.dsn.split():
                (key, value) = element.split("=")
                if value != "''" and value != '""':
                    db_info[key] = value

    if request.param == "PG_DE_DB_WITH_SCHEMA":
        my_ds = Postgresql_datasource(db_info)

    load_sample_data_into_datasource(my_ds)

    yield my_ds

    del my_ds
    gc.collect()


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
    logging.getLogger().debug("Loading Sample data for tests")

    _pk = schema_only_db.store_taskmanager(
        "taskmanager1",
        "11111111-1111-1111-1111-111111111111",
        datetime.datetime(2016, 3, 14),
    )  # _pk=1 probably
    header = Header(_pk)
    metadata = Metadata(_pk)
    schema_only_db.insert(
        _pk, 1, "my_test_key", b"my_test_value", header, metadata
    )
    schema_only_db.insert(
        _pk, 1, "a_test_key", b"a_test_value", header, metadata
    )

    _pk = schema_only_db.store_taskmanager(
        "taskmanager2", "22222222-2222-2222-2222-222222222222"
    )  # _pk=2 probably
    header = Header(_pk)
    metadata = Metadata(_pk)
    schema_only_db.insert(
        _pk, 2, "other_test_key", b"other_test_value", header, metadata
    )

    # return the connection now that it isn't just the schema
    return schema_only_db
