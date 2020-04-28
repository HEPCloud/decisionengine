import os
import pytest
import psycopg2

from pytest_postgresql import factories
from decisionengine.framework.dataspace.datasources.postgresql import *

pg_ctl = "/usr/pgsql-11/bin/pg_ctl"
if "PG_CTL" in os.environ:
    pg_ctl = os.environ["PG_CTL"]

postgresql_server = factories.postgresql_proc(pg_ctl)

@pytest.fixture(scope="session")
def postgresql(postgresql_server):
    dsn = {
        "user": postgresql_server.user,
        "port": postgresql_server.port,
        "host": postgresql_server.unixsocketdir
    }
    # Load decision engine schema
    with psycopg2.connect(**dsn) as connection:
        with connection.cursor() as cursor:
            cwd = os.path.split(os.path.abspath(__file__))[0]
            cursor.execute(open(cwd + "/../postgresql.sql", "r").read())
        connection.commit()

    return Postgresql(dsn)

@pytest.fixture(scope="session")
def taskmanager():
    return {
        "name": "test",
        "taskmanager_id": "12321"
    }

def test_py_psql(postgresql):
    print(postgresql)

def test_generate_insert_query():
    table_name = "header"
    keys = ["generation_id", "create_time", "creator"]
    expected_query = "INSERT INTO header (generation_id,create_time,creator) VALUES (%s,%s,%s)"

    result_query = generate_insert_query(table_name, keys).strip()

    assert result_query == expected_query

def test_create_tables(postgresql):
    assert postgresql.create_tables()

def test_store_taskmanager(postgresql, taskmanager):
    result = postgresql.store_taskmanager(taskmanager["name"], taskmanager["taskmanager_id"])
    assert result == 1

def test_get_taskmanager(postgresql, taskmanager):
    result = postgresql.get_taskmanager(taskmanager["name"], taskmanager["taskmanager_id"])
    pass
