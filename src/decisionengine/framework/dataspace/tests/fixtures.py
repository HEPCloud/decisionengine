# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import gc

import pytest

from decisionengine.framework.dataspace import dataspace as ds
from decisionengine.framework.dataspace.datasources.tests.fixtures import (  # noqa: F401
    DATABASES_TO_TEST,
    datasource,
    load_sample_data_into_datasource,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)

__all__ = [
    "PG_DE_DB_WITHOUT_SCHEMA",
    "PG_PROG",
    "DATABASES_TO_TEST",
    "SQLALCHEMY_PG_WITH_SCHEMA",
    "SQLALCHEMY_TEMPFILE_SQLITE",
    "datasource",
    "dataspace",
    "load_sample_data_into_datasource",
]


@pytest.fixture(params=DATABASES_TO_TEST)
def dataspace(request):
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
        db_info["echo"] = True  # put into extra chatty mode for tests
    except TypeError:
        # psycopg2
        db_info["host"] = conn_fixture.info.host
        db_info["port"] = conn_fixture.info.port
        db_info["user"] = conn_fixture.info.user
        db_info["password"] = conn_fixture.info.password
        db_info["database"] = conn_fixture.info.dbname

    config = {}
    config["dataspace"] = {}
    config["dataspace"]["datasource"] = {}
    config["dataspace"]["datasource"]["config"] = db_info

    config["dataspace"]["datasource"]["module"] = "decisionengine.framework.dataspace.datasources.sqlalchemy_ds"
    config["dataspace"]["datasource"]["name"] = "SQLAlchemyDS"

    my_ds = ds.DataSpace(config)
    load_sample_data_into_datasource(my_ds)

    yield my_ds

    del my_ds
    gc.collect()
