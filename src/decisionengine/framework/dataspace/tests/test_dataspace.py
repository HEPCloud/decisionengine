import datetime

import pytest

from sqlalchemy.exc import NoResultFound

from decisionengine.framework.dataspace import dataspace as ds
from decisionengine.framework.dataspace.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_PROG,
    DATABASES_TO_TEST,
    load_sample_data_into_datasource,
)
from decisionengine.framework.dataspace.datablock import Header, Metadata


@pytest.fixture(params=DATABASES_TO_TEST)
def dataspace(request):
    """
    This parameterized fixture will mock up various datasources.
    Add datasource objects to DATASOURCES_TO_TEST once they've got
    our basic schema loaded.  And adjust our `if` statements here
    until we are SQLAlchemy only.
    Pytest should take it from there and automatically run it
    through all the below tests
    """
    conn_fixture = request.getfixturevalue(request.param)

    db_info = {}
    try:
        # SQL Alchemy
        db_info["url"] = conn_fixture["url"]
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

    config = {}
    config["dataspace"] = {}
    config["dataspace"]["datasource"] = {}
    config["dataspace"]["datasource"]["config"] = db_info

    if request.param == "PG_DE_DB_WITH_SCHEMA":
        config["dataspace"]["datasource"][
            "module"
        ] = "decisionengine.framework.dataspace.datasources.postgresql"
        config["dataspace"]["datasource"]["name"] = "Postgresql"

    my_ds = ds.DataSpace(config)
    load_sample_data_into_datasource(my_ds)
    return my_ds


def test_dataspace_config_finds_bad():
    with pytest.raises(ds.DataSpaceConfigurationError) as e:
        ds.DataSpace({})
    assert e.match("missing dataspace information")

    with pytest.raises(ds.DataSpaceConfigurationError) as e:
        ds.DataSpace({"dataspace": "asdf"})
    assert e.match("dataspace key must correspond to a dictionary")

    with pytest.raises(ds.DataSpaceConfigurationError) as e:
        ds.DataSpace({"dataspace": {"asdf": "asdf"}})
    assert e.match("Invalid dataspace configuration")


@pytest.mark.usefixtures("dataspace")
def test_get_taskmanager_exists(dataspace):
    """Can I get a taskmanager by name or name and uuid"""
    # should return the 'newest' instance
    result1 = dataspace.get_taskmanager(taskmanager_name="taskmanager1")
    assert result1["name"] == "taskmanager1"
    assert str(result1["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result2 = dataspace.get_taskmanager(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result2["name"] == "taskmanager1"
    assert str(result2["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    assert result1 == result2


@pytest.mark.usefixtures("dataspace")
def test_get_taskmanager_not_exists(dataspace):
    """This should error out"""
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_taskmanager(taskmanager_name="no_such_task_manager")
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_taskmanager(
            taskmanager_name="no_such_task_manager",
            taskmanager_id="11111111-1111-1111-1111-111111111111",
        )


@pytest.mark.usefixtures("dataspace")
def test_get_taskmanagers(dataspace):
    """Can I get multimple task managers"""
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
    two_years_future = str(datetime.datetime.now() + datetime.timedelta(days=730))

    result0 = dataspace.get_taskmanagers()
    assert len(result0) == 2

    result1 = dataspace.get_taskmanagers(taskmanager_name="taskmanager1")
    assert len(result1) == 1
    assert result1[0]["name"] == "taskmanager1"
    assert str(result1[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result2 = dataspace.get_taskmanagers(start_time=yesterday)
    assert len(result2) == 1
    assert result2[0]["name"] == "taskmanager2"
    assert str(result2[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result3 = dataspace.get_taskmanagers(end_time=yesterday)
    assert len(result3) == 1
    assert result3[0]["name"] == "taskmanager1"
    assert str(result3[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result4 = dataspace.get_taskmanagers(
        taskmanager_name="taskmanager1", end_time=yesterday
    )
    assert len(result4) == 1
    assert result4[0]["name"] == "taskmanager1"
    assert str(result4[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result5 = dataspace.get_taskmanagers(
        taskmanager_name="taskmanager2", start_time=yesterday
    )
    assert len(result5) == 1
    assert result5[0]["name"] == "taskmanager2"
    assert str(result5[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result6 = dataspace.get_taskmanagers(
        taskmanager_name="taskmanager2", start_time=yesterday, end_time=two_years_future
    )
    assert len(result6) == 1
    assert result6[0]["name"] == "taskmanager2"
    assert str(result6[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result7 = dataspace.get_taskmanagers(
        start_time=yesterday, end_time=two_years_future
    )
    assert len(result7) == 1
    assert result7[0]["name"] == "taskmanager2"
    assert str(result7[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"


@pytest.mark.usefixtures("dataspace")
def test_get_taskmanagers_not_exist(dataspace):
    """Do I error out when asking for garbage"""
    last_year = str(datetime.datetime.now() - datetime.timedelta(days=365))
    two_years_future = str(datetime.datetime.now() + datetime.timedelta(days=730))

    result = dataspace.get_taskmanagers(taskmanager_name="no_such_task_manager")
    assert result == []

    result = dataspace.get_taskmanagers(start_time=two_years_future)
    assert result == []

    result = dataspace.get_taskmanagers(end_time=last_year, start_time=two_years_future)
    assert result == []


@pytest.mark.usefixtures("dataspace")
def test_store_taskmanager(dataspace):
    """Can we make new entries"""
    primary_key = dataspace.store_taskmanager(
        name="taskmanager3",
        taskmanager_id="00000003-0003-0003-0003-000000000003",
    )
    assert primary_key > 1


@pytest.mark.usefixtures("dataspace")
def test_get_last_generation_id(dataspace):
    """Can we get the last generation id by name or name and uuid"""
    result1 = dataspace.get_last_generation_id(taskmanager_name="taskmanager1")
    assert result1 == 1
    result1 = dataspace.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 1

    result2 = dataspace.get_last_generation_id(
        taskmanager_name="taskmanager2",
        taskmanager_id="22222222-2222-2222-2222-222222222222",
    )
    assert result2 == 2


@pytest.mark.usefixtures("dataspace")
def test_get_last_generation_id_not_exist(dataspace):
    """Does it error out if we ask for a bogus taskmanager?"""
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_last_generation_id(taskmanager_name="no_such_task_manager")
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_last_generation_id(
            taskmanager_name="no_such_task_manager",
            taskmanager_id="11111111-1111-1111-1111-111111111111",
        )


@pytest.mark.usefixtures("dataspace")
def test_get_header(dataspace):
    """Can we fetch a header?"""
    result = dataspace.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result[0] == "11111111-1111-1111-1111-111111111111"
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == "my_test_key"
    assert result[7] == "module"


@pytest.mark.usefixtures("dataspace")
def test_get_header_not_exist(dataspace):
    """Does it error out if we ask for a bogus header?"""
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_header(
            taskmanager_id=100,
            generation_id=1,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_header(
            taskmanager_id=100,
            generation_id=10,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_header(
            taskmanager_id=100,
            generation_id=1,
            key="no_such_key_exists",
        )


@pytest.mark.usefixtures("dataspace")
def test_get_metadata(dataspace):
    """Can we fetch a metadata element?"""
    result = dataspace.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result[0] == "11111111-1111-1111-1111-111111111111"
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == "my_test_key"


@pytest.mark.usefixtures("dataspace")
def test_get_metadata_not_exist(dataspace):
    """Does it error out if we ask for a bogus metadata element?"""
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_metadata(
            taskmanager_id=100,
            generation_id=1,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_metadata(
            taskmanager_id=100,
            generation_id=11111111,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_metadata(
            taskmanager_id=100,
            generation_id=1,
            key="no_such_key_exists",
        )


@pytest.mark.usefixtures("dataspace")
def test_get_dataproducts(dataspace):
    """Can we get the dataproducts by uuid and uuid with key"""
    result1 = dataspace.get_dataproducts(taskmanager_id=1)

    assert len(result1) == 2
    assert result1[0] == {
        "taskmanager_id": 1,
        "generation_id": 1,
        "key": "my_test_key",
        "value": b"my_test_value",
    }
    assert result1[1] == {
        "taskmanager_id": 1,
        "generation_id": 1,
        "key": "a_test_key",
        "value": b"a_test_value",
    }

    result2 = dataspace.get_dataproducts(taskmanager_id="2", key="other_test_key")

    assert result2 == [
        {
            "taskmanager_id": 2,
            "generation_id": 2,
            "key": "other_test_key",
            "value": b"other_test_value",
        },
    ]


@pytest.mark.usefixtures("dataspace")
def test_get_dataproducts_not_exist(dataspace):
    """Does it error out if we ask for bogus information?"""
    result = dataspace.get_dataproducts(taskmanager_id=100)

    assert result == []
    result = dataspace.get_dataproducts(taskmanager_id=2, key="no_such_key")
    assert result == []


@pytest.mark.usefixtures("dataspace")
def test_get_dataproduct(dataspace):
    """Can we get the dataproduct by uuid with key"""
    result2 = dataspace.get_dataproduct(
        taskmanager_id=2,
        generation_id=2,
        key="other_test_key",
    )

    assert result2 == b"other_test_value"


@pytest.mark.usefixtures("dataspace")
def test_get_dataproduct_not_exist(dataspace):
    """Does it error out if we ask for bogus information?"""
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.get_dataproduct(
            taskmanager_id=2,
            generation_id=2,
            key="no_such_key",
        )


@pytest.mark.usefixtures("dataspace")
def test_insert(dataspace):
    """Can we insert new elements"""
    primary_key = dataspace.store_taskmanager(
        "taskmanager3", "33333333-3333-3333-3333-333333333333"
    )
    assert primary_key > 1

    header = Header(primary_key)
    metadata = Metadata(primary_key)
    dataspace.insert(
        primary_key,
        1,
        "sample_test_key",
        "sample_test_value".encode(),
        header,
        metadata,
    )

    result1 = dataspace.get_dataproducts(taskmanager_id=primary_key)

    assert result1 == [
        {
            "key": "sample_test_key",
            "taskmanager_id": primary_key,
            "generation_id": 1,
            "value": b"sample_test_value",
        }
    ]

    result2 = dataspace.get_dataproducts(
        taskmanager_id=primary_key, key="sample_test_key"
    )

    assert result1 == result2


@pytest.mark.usefixtures("dataspace")
def test_update(dataspace):
    """Do updates work as expected"""
    metadata_row = dataspace.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    header_row = dataspace.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    dataspace.update(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
        value=b"I changed IT",
        header=Header(
            header_row[0],
            create_time=header_row[4],
            expiration_time=header_row[5],
            scheduled_create_time=header_row[6],
            creator=header_row[7],
            schema_id=header_row[8],
        ),
        metadata=Metadata(
            metadata_row[0],
            state=metadata_row[4],
            generation_id=metadata_row[2],
            generation_time=metadata_row[5],
            missed_update_count=metadata_row[6],
        ),
    )

    result1 = dataspace.get_dataproduct(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result1 == b"I changed IT"


@pytest.mark.usefixtures("dataspace")
def test_update_bad(dataspace):
    """Do updates fail to work as expected"""
    metadata_row = dataspace.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    header_row = dataspace.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    with pytest.raises((KeyError, NoResultFound)):
        dataspace.update(
            taskmanager_id=100,
            generation_id=1,
            key="my_test_key",
            value=b"I changed IT",
            header=Header(
                header_row[0],
                create_time=header_row[4],
                expiration_time=header_row[5],
                scheduled_create_time=header_row[6],
                creator=header_row[7],
                schema_id=header_row[8],
            ),
            metadata=Metadata(
                metadata_row[0],
                state=metadata_row[4],
                generation_id=metadata_row[2],
                generation_time=metadata_row[5],
                missed_update_count=metadata_row[6],
            ),
        )


@pytest.mark.usefixtures("dataspace")
def test_duplicate_datablock(dataspace):
    """Can we duplicate taskmanager1 and all its entries"""
    result1 = dataspace.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 1

    result1 = dataspace.get_dataproducts(
        taskmanager_id=1,
    )
    assert len(result1) == 2

    dataspace.duplicate_datablock(1, 1, 90)

    result1 = dataspace.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 90
