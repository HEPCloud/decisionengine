import os
import pytest
import psycopg2
import pytest_postgresql

from decisionengine.framework.dataspace.datasources.postgresql import Postgresql, generate_insert_query
from decisionengine.framework.dataspace.datablock import Header, Metadata


@pytest.fixture(scope="function")
def datasource(postgresql, data):
    with postgresql.cursor() as cursor:
        cwd = os.path.split(os.path.abspath(__file__))[0]
        # Load decision engine schema
        cursor.execute(open(cwd + "/../postgresql.sql", "r").read())
        # Load test data
        for table, rows in data.items():
            for row in rows:
                keys = ",".join(row.keys())
                values = ",".join([f"'{value}'" for value in row.values()])
                cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")
    postgresql.commit()

    return Postgresql(postgresql.info.dsn_parameters)

@pytest.fixture(scope="session")
def data():
    return {
        "taskmanager": [
            {
                "name": "taskmanager1",
                "taskmanager_id": "1"
            },
            {
                "name": "taskmanager2",
                "taskmanager_id": "2"
            }
        ],
        "dataproduct": [
            {
                "taskmanager_id": "1",
                "generation_id": "1",
                "key": "test_key1",
                "value": "test_value1"
            }
        ]
    }

@pytest.fixture(scope="session")
def taskmanager():
    return {
        "name": "new_taskmanager",
        "taskmanager_id": "123"
    }

@pytest.fixture(scope="session")
def dataproduct():
    return {
        "taskmanager_id": "1",
        "generation_id": "2",
        "key": "new_key",
        "value": "new_value"
    }

@pytest.fixture(scope="session")
def header(data):
    return Header(
        data["taskmanager"][0]["taskmanager_id"]
    )

@pytest.fixture(scope="session")
def metadata(data):
    return Metadata(
        data["taskmanager"][0]["taskmanager_id"]
    )

def test_generate_insert_query():
    table_name = "header"
    keys = ["generation_id", "create_time", "creator"]
    expected_query = "INSERT INTO header (generation_id,create_time,creator) VALUES (%s,%s,%s)"

    result_query = generate_insert_query(table_name, keys).strip()

    assert result_query == expected_query

def test_create_tables(datasource):
    assert datasource.create_tables()

def test_store_taskmanager(datasource, taskmanager):
    result = datasource.store_taskmanager(taskmanager["name"], taskmanager["taskmanager_id"])
    assert result > 0

def test_get_taskmanager(datasource, taskmanager, data):
    # test valid taskmanager
    result = datasource.get_taskmanager(data["taskmanager"][0]["name"], data["taskmanager"][0]["taskmanager_id"])
    assert result["name"] == data["taskmanager"][0]["name"]
    assert result["taskmanager_id"] == data["taskmanager"][0]["taskmanager_id"]

    result = datasource.get_taskmanager(data["taskmanager"][0]["name"])
    assert result["name"] == data["taskmanager"][0]["name"]

    # test taskmanager not present in the database
    try:
        datasource.get_taskmanager(taskmanager["name"], taskmanager["taskmanager_id"])
    except Exception as e:
        assert e.__class__ == KeyError

    try:
        datasource.get_taskmanager(taskmanager["name"])
    except Exception as e:
        assert e.__class__ == KeyError

def test_get_last_generation_id(datasource, taskmanager, data):
    # test valid taskmanager
    result = datasource.get_last_generation_id(data["taskmanager"][0]["name"], data["taskmanager"][0]["taskmanager_id"])
    assert result == int(data["dataproduct"][0]["generation_id"])

    result = datasource.get_last_generation_id(data["taskmanager"][0]["name"])
    assert result == int(data["dataproduct"][0]["generation_id"])

    # test taskmanager not present in the database
    try:
        result = datasource.get_last_generation_id(taskmanager["name"], taskmanager["taskmanager_id"])
    except Exception as e:
        assert e.__class__ == KeyError

    try:
        datasource.get_last_generation_id(taskmanager["name"])
    except Exception as e:
        assert e.__class__ == KeyError

def test_insert(datasource, dataproduct, header, metadata):
    datasource.insert(dataproduct["taskmanager_id"], dataproduct["generation_id"], dataproduct["key"],
                      dataproduct["value"], header, metadata)
