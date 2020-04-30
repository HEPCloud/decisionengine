import os
import pytest
import psycopg2
import pytest_postgresql
from decisionengine.framework.dataspace.datasources.postgresql import Postgresql, generate_insert_query


@pytest.fixture(scope="function")
def postgresql(postgresql_proc, data):
    dsn = {
        "user": postgresql_proc.user,
        "port": postgresql_proc.port,
        "host": postgresql_proc.unixsocketdir
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

def test_get_last_generation_id(postgresql, data):
    postgresql.get_last_generation_id(data["taskmanager"][0]["name"], data["taskmanager"][0]["taskmanager_id"])
    assert True
