import os
import pytest
import psycopg2

from pytest_postgresql import factories
from decisionengine.framework.dataspace.datasources.postgresql import *

pg_ctl = "/usr/pgsql-11/bin/pg_ctl"
if "PG_CTL" in os.environ:
    pg_ctl = os.environ["PG_CTL"]

postgresql_server = factories.postgresql_proc(pg_ctl)

@pytest.fixture(scope="function")
def postgresql(postgresql_server, data):
    dsn = {
        "user": postgresql_server.user,
        "port": postgresql_server.port,
        "host": postgresql_server.unixsocketdir
    }

    with psycopg2.connect(**dsn) as connection:
        with connection.cursor() as cursor:
            cwd = os.path.split(os.path.abspath(__file__))[0]
            # Load decision engine schema
            cursor.execute(open(cwd + "/../postgresql.sql", "r").read())
            # Load test data
            for table, rows in data.items():
                for row in rows:
                    keys = ",".join(row.keys())
                    values = ",".join([f"'{value}'" for value in row.values()])
                    cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")
        connection.commit()

    return Postgresql(dsn)

@pytest.fixture(scope="session")
def data():
    return {
        "taskmanager": [
            {
                "name": "taskmanager1",
                "taskmanager_id": "1"
            }
        ]
    }

@pytest.fixture(scope="session")
def taskmanager():
    return {
        "name": "new_taskmanager",
        "taskmanager_id": "123"
    }

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
    assert result > 0

def test_get_taskmanager(postgresql, taskmanager, data):
    # test valid taskmanager
    result = postgresql.get_taskmanager(data["taskmanager"][0]["name"], data["taskmanager"][0]["taskmanager_id"])
    assert result["name"] == data["taskmanager"][0]["name"]
    assert result["taskmanager_id"] == data["taskmanager"][0]["taskmanager_id"]

    result = postgresql.get_taskmanager(data["taskmanager"][0]["name"])
    assert result["name"] == data["taskmanager"][0]["name"]

    # test taskmanager not present in the database
    try:
        result = postgresql.get_taskmanager(taskmanager["name"], taskmanager["taskmanager_id"])
    except Exception as e:
        assert e.__class__ == KeyError
    
    try:
        result = postgresql.get_taskmanager(taskmanager["name"])
    except Exception as e:
        assert e.__class__ == KeyError
