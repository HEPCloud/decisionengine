# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# pylint: disable=redefined-outer-name,wrong-import-order,unused-import
"""
This test plan covers a generic dataspace object via
pytest parameters.
"""
import datetime

import pytest

from sqlalchemy.exc import NoResultFound

from decisionengine.framework.dataspace.datablock import Header, Metadata
from decisionengine.framework.dataspace.datasources.tests.fixtures import (  # noqa: F401
    DATABASES_TO_TEST,
    datasource,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)


def test_create_tables(datasource):  # noqa: F811
    """create_tables() should be safe to call multiple times"""
    datasource.create_tables()


def test_reset_connections(datasource):  # noqa: F811
    """reset_connections() should be safe to call any time"""
    datasource.reset_connections()


def test_has_config(datasource):  # noqa: F811
    """This should have a `config` dict we can pass to jsonnet"""
    assert isinstance(datasource.config, dict)


def test_get_taskmanager_exists(datasource):  # noqa: F811
    """Can I get a taskmanager by name or name and uuid"""
    # should return the 'newest' instance
    result1 = datasource.get_taskmanager(taskmanager_name="taskmanager1")
    assert result1["name"] == "taskmanager1"
    assert str(result1["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result2 = datasource.get_taskmanager(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result2["name"] == "taskmanager1"
    assert str(result2["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    assert result1 == result2


def test_get_taskmanager_not_exists(datasource):  # noqa: F811
    """This should error out"""
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_taskmanager(taskmanager_name="no_such_task_manager")
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_taskmanager(
            taskmanager_name="no_such_task_manager",
            taskmanager_id="11111111-1111-1111-1111-111111111111",
        )


def test_get_taskmanagers(datasource):  # noqa: F811
    """Can I get multimple task managers"""
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))
    two_years_future = str(datetime.datetime.now() + datetime.timedelta(days=730))

    result0 = datasource.get_taskmanagers()
    assert len(result0) == 2

    result1 = datasource.get_taskmanagers(taskmanager_name="taskmanager1")
    assert len(result1) == 1
    assert result1[0]["name"] == "taskmanager1"
    assert str(result1[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result2 = datasource.get_taskmanagers(start_time=yesterday)
    assert len(result2) == 1
    assert result2[0]["name"] == "taskmanager2"
    assert str(result2[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result3 = datasource.get_taskmanagers(end_time=yesterday)
    assert len(result3) == 1
    assert result3[0]["name"] == "taskmanager1"
    assert str(result3[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result4 = datasource.get_taskmanagers(taskmanager_name="taskmanager1", end_time=yesterday)
    assert len(result4) == 1
    assert result4[0]["name"] == "taskmanager1"
    assert str(result4[0]["taskmanager_id"]) == "11111111-1111-1111-1111-111111111111"

    result5 = datasource.get_taskmanagers(taskmanager_name="taskmanager2", start_time=yesterday)
    assert len(result5) == 1
    assert result5[0]["name"] == "taskmanager2"
    assert str(result5[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result6 = datasource.get_taskmanagers(
        taskmanager_name="taskmanager2", start_time=yesterday, end_time=two_years_future
    )
    assert len(result6) == 1
    assert result6[0]["name"] == "taskmanager2"
    assert str(result6[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"

    result7 = datasource.get_taskmanagers(start_time=yesterday, end_time=two_years_future)
    assert len(result7) == 1
    assert result7[0]["name"] == "taskmanager2"
    assert str(result7[0]["taskmanager_id"]) == "22222222-2222-2222-2222-222222222222"


def test_get_taskmanagers_not_exist(datasource):  # noqa: F811
    """Do I error out when asking for garbage"""
    last_year = str(datetime.datetime.now() - datetime.timedelta(days=365))
    two_years_future = str(datetime.datetime.now() + datetime.timedelta(days=730))

    result = datasource.get_taskmanagers(taskmanager_name="no_such_task_manager")
    assert result == []

    result = datasource.get_taskmanagers(start_time=two_years_future)
    assert result == []

    result = datasource.get_taskmanagers(end_time=last_year, start_time=two_years_future)
    assert result == []


def test_store_taskmanager(datasource):  # noqa: F811
    """Can we make new entries"""
    primary_key = datasource.store_taskmanager(
        name="taskmanager3",
        taskmanager_id="00000003-0003-0003-0003-000000000003",
    )
    assert primary_key > 1


def test_get_last_generation_id(datasource):  # noqa: F811
    """Can we get the last generation id by name or name and uuid"""
    result1 = datasource.get_last_generation_id(taskmanager_name="taskmanager1")
    assert result1 == 1
    result1 = datasource.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 1

    result2 = datasource.get_last_generation_id(
        taskmanager_name="taskmanager2",
        taskmanager_id="22222222-2222-2222-2222-222222222222",
    )
    assert result2 == 2


def test_get_last_generation_id_not_exist(datasource):  # noqa: F811
    """Does it error out if we ask for a bogus taskmanager?"""
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_last_generation_id(taskmanager_name="no_such_task_manager")
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_last_generation_id(
            taskmanager_name="no_such_task_manager",
            taskmanager_id="11111111-1111-1111-1111-111111111111",
        )


def test_get_header(datasource):  # noqa: F811
    """Can we fetch a header?"""
    result = datasource.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result[0] == "11111111-1111-1111-1111-111111111111"
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == "my_test_key"
    assert result[7] == "module"


def test_get_header_not_exist(datasource):  # noqa: F811
    """Does it error out if we ask for a bogus header?"""
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_header(
            taskmanager_id=100,
            generation_id=1,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_header(
            taskmanager_id=100,
            generation_id=10,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_header(
            taskmanager_id=100,
            generation_id=1,
            key="no_such_key_exists",
        )


def test_get_metadata(datasource):  # noqa: F811
    """Can we fetch a metadata element?"""
    result = datasource.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result[0] == "11111111-1111-1111-1111-111111111111"
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == "my_test_key"


def test_get_metadata_not_exist(datasource):  # noqa: F811
    """Does it error out if we ask for a bogus metadata element?"""
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_metadata(
            taskmanager_id=100,
            generation_id=1,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_metadata(
            taskmanager_id=100,
            generation_id=11111111,
            key="my_test_key",
        )

    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_metadata(
            taskmanager_id=100,
            generation_id=1,
            key="no_such_key_exists",
        )


def test_get_dataproducts(datasource):  # noqa: F811
    """Can we get the dataproducts by uuid and uuid with key"""
    result1 = datasource.get_dataproducts(taskmanager_id=1)

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

    result2 = datasource.get_dataproducts(taskmanager_id="2", key="other_test_key")

    assert result2 == [
        {
            "taskmanager_id": 2,
            "generation_id": 2,
            "key": "other_test_key",
            "value": b"other_test_value",
        },
    ]


def test_get_dataproducts_not_exist(datasource):  # noqa: F811
    """Does it error out if we ask for bogus information?"""
    result = datasource.get_dataproducts(taskmanager_id=100)

    assert result == []
    result = datasource.get_dataproducts(taskmanager_id=2, key="no_such_key")
    assert result == []


def test_get_dataproduct(datasource):  # noqa: F811
    """Can we get the dataproduct by uuid with key"""
    result2 = datasource.get_dataproduct(
        taskmanager_id=2,
        generation_id=2,
        key="other_test_key",
    )

    assert result2 == b"other_test_value"


def test_get_dataproduct_not_exist(datasource):  # noqa: F811
    """Does it error out if we ask for bogus information?"""
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_dataproduct(
            taskmanager_id=2,
            generation_id=2,
            key="no_such_key",
        )


def test_insert(datasource):  # noqa: F811
    """Can we insert new elements"""
    primary_key = datasource.store_taskmanager("taskmanager3", "33333333-3333-3333-3333-333333333333")
    assert primary_key > 1

    header = Header(primary_key)
    metadata = Metadata(primary_key)
    datasource.insert(
        primary_key,
        1,
        "sample_test_key",
        b"sample_test_value",
        header,
        metadata,
    )

    result1 = datasource.get_dataproducts(taskmanager_id=primary_key)

    assert result1 == [
        {
            "key": "sample_test_key",
            "taskmanager_id": primary_key,
            "generation_id": 1,
            "value": b"sample_test_value",
        }
    ]

    result2 = datasource.get_dataproducts(taskmanager_id=primary_key, key="sample_test_key")

    assert result1 == result2


def test_update(datasource):  # noqa: F811
    """Do updates work as expected"""
    metadata_row = datasource.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    header_row = datasource.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    datasource.update(
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

    result1 = datasource.get_dataproduct(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )

    assert result1 == b"I changed IT"


def test_update_bad(datasource):  # noqa: F811
    """Do updates fail to work on bogus taskmanager as expected"""
    metadata_row = datasource.get_metadata(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    header_row = datasource.get_header(
        taskmanager_id=1,
        generation_id=1,
        key="my_test_key",
    )
    with pytest.raises(Exception):
        datasource.update(
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


def test_delete_data_older_than_arg(datasource):  # noqa: F811
    """Can we delete old entries"""
    with pytest.raises((ValueError, NoResultFound), match="Argument has to be positive, non zero integer"):
        datasource.delete_data_older_than(0)
    with pytest.raises((ValueError, NoResultFound), match="Argument has to be positive, non zero integer"):
        datasource.delete_data_older_than(-5)

    # verify our old record is loaded
    result1 = datasource.get_taskmanager(taskmanager_name="taskmanager1")
    assert result1["name"] == "taskmanager1"

    # should test it deletes the old one
    datasource.delete_data_older_than(10)
    with pytest.raises((KeyError, NoResultFound)):
        datasource.get_taskmanager(taskmanager_name="taskmanager1")


def test_get_datablock(datasource):  # noqa: F811
    tm = datasource.get_taskmanager(taskmanager_name="taskmanager1")
    gen_id = datasource.get_last_generation_id(taskmanager_name="taskmanager1")
    result1 = datasource.get_datablock(tm["sequence_id"], gen_id)

    assert result1 == {"my_test_key": b"my_test_value", "a_test_key": b"a_test_value"}


def test_duplicate_datablock(datasource):  # noqa: F811
    """Can we duplicate taskmanager1 and all its entries"""
    result1 = datasource.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 1

    result1 = datasource.get_dataproducts(
        taskmanager_id=1,
    )
    assert len(result1) == 2

    datasource.duplicate_datablock(1, 1, 90)

    result1 = datasource.get_last_generation_id(
        taskmanager_name="taskmanager1",
        taskmanager_id="11111111-1111-1111-1111-111111111111",
    )
    assert result1 == 90
