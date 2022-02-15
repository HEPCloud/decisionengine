# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import ast

import pytest

from decisionengine.framework.dataspace import datablock
from decisionengine.framework.dataspace.tests.fixtures import (  # noqa: F401
    DATABASES_TO_TEST,
    dataspace,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)


def test_DataBlock_constructor(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples

    dblock = datablock.DataBlock(dataspace, my_tm["name"])
    assert dblock.generation_id == 1

    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])
    assert dblock.generation_id == 1

    dblock = datablock.DataBlock(dataspace, my_tm["name"], generation_id=1)
    assert dblock.generation_id == 1

    dblock = datablock.DataBlock(dataspace, my_tm["name"], sequence_id=1)
    assert dblock.generation_id == 1


def test_DataBlock_to_str(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples

    expected = {
        "taskmanager_id": my_tm["taskmanager_id"],
        "generation_id": dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"]),
        "sequence_id": len(dataspace.get_dataproducts(my_tm["sequence_id"])) + 1,
        "keys": ("example_test_key",),
        "dataproducts": {"example_test_key": "example_test_value"},
    }

    header = datablock.Header(my_tm["taskmanager_id"])

    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])
    dblock.put("example_test_key", "example_test_value", header)

    result = ast.literal_eval(str(dblock))
    assert result == expected


def test_DataBlock_key_management(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    metadata = datablock.Metadata(
        my_tm["taskmanager_id"],
        generation_id=dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"]),
    )
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    # test with automatic metadata and string value
    dblock.put("example_test_key", "example_test_value", header)

    # verify __contains__ matches .keys()
    assert "example_test_key" in dblock.keys()  # noqa: SIM118
    assert "example_test_key" in dblock

    assert dblock.get("example_test_key") == "example_test_value"

    # Test product-retriever interface
    retriever = datablock.ProductRetriever("example_test_key", None, None)
    assert retriever(dblock) == "example_test_value"
    assert str(retriever) == r"Product retriever for {'name': 'example_test_key', 'type': None, 'creator': None}"

    # test new key with manual metadata and dict value
    newDict = {"subKey": "newValue"}
    dblock.put("new_example_test_key", newDict, header, metadata)
    assert dblock["new_example_test_key"] == newDict


def test_DataBlock_key_management_change_name(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    # FIXME: The following behavior should be disallowed for data-integrity reasons!
    #        i.e. replacing a product name from datablock.ProductRetriever with a
    #             different value.
    newDict = {"subKey": "newValue"}
    dblock.put("example_test_key", newDict, header)
    assert dblock["example_test_key"] == newDict


def test_DataBlock_no_key_by_name(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    with pytest.raises(KeyError):
        dblock["no_such_key_exists"]


def test_DataBlock_get_header(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    assert header == dblock.get_header("example_test_key")


def test_DataBlock_get_metadata(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    metadata = datablock.Metadata(
        my_tm["taskmanager_id"],
        generation_id=dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"]),
    )
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header, metadata)

    assert metadata == dblock.get_metadata("example_test_key")


def test_DataBlock_get_taskmanager(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    assert dblock.get_taskmanager(my_tm["name"])["taskmanager_id"] == my_tm["taskmanager_id"]


def test_DataBlock_is_expired(dataspace):  # noqa: F811
    """This test just validates the method/function exists.
    The stub within our default code should be replaced
    by a class inheriting from it.
    That class should have more rational return types.
    """
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    assert dblock.is_expired() is None


def test_DataBlock_is_expired_with_key(dataspace):  # noqa: F811
    """This test just validates the method/function exists.
    The stub within our default code should be replaced
    by a class inheriting from it.
    That class should have more rational return types.
    """
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    assert dblock.is_expired(key="example_test_key") is None


def test_DataBlock_mark_expired(dataspace):  # noqa: F811
    # mark_expired is just a stub in this case
    # failure in a real implementation should raise an exception
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    assert dblock.mark_expired(1) is None


def test_DataBlock_get_dataproducts(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    products = dblock.get_dataproducts()
    assert len(products) == 1
    assert products[0]["key"] == "example_test_key"
    assert products[0]["value"] == "example_test_value"


def test_DataBlock_duplicate(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])
    dblock = datablock.DataBlock(dataspace, my_tm["name"], my_tm["taskmanager_id"])

    dblock.put("example_test_key", "example_test_value", header)

    dblock_2 = dblock.duplicate()

    assert dblock.taskmanager_id == dblock_2.taskmanager_id
    assert dblock.generation_id == dblock_2.generation_id + 1
    assert dblock.sequence_id == dblock_2.sequence_id
    assert dblock.keys() == dblock_2.keys()

    for key in dblock.keys():
        assert dblock[key] == dblock_2[key]


def test_Metadata_constructor(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    metadata = datablock.Metadata(my_tm["taskmanager_id"])

    assert metadata.data["taskmanager_id"] == my_tm["taskmanager_id"]

    genTime = 1.0
    missCount = 3
    state = "START_BACKUP"

    metadata = datablock.Metadata(
        my_tm["taskmanager_id"],
        state=state,
        generation_id=dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"]),
        generation_time=genTime,
        missed_update_count=missCount,
    )

    assert metadata.data["taskmanager_id"] == my_tm["taskmanager_id"]
    assert metadata.data["state"] == state
    assert metadata.data["generation_id"] == dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"])
    assert metadata.data["generation_time"] == genTime
    assert metadata.data["missed_update_count"] == missCount

    with pytest.raises(datablock.InvalidMetadataError):
        metadata = datablock.Metadata(
            my_tm["taskmanager_id"],
            state="NO SUCH STATE EXISTS",
            generation_id=dataspace.get_last_generation_id(my_tm["name"], my_tm["taskmanager_id"]),
            generation_time=genTime,
            missed_update_count=missCount,
        )


def test_Metadata_set_state(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    metadata = datablock.Metadata(my_tm["taskmanager_id"])

    state = "START_BACKUP"
    metadata.set_state(state)

    assert metadata.data["state"] == state

    with pytest.raises(datablock.InvalidMetadataError):
        metadata.set_state("INVALID_STATE")


def test_Header_constructor(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])

    assert header.data["taskmanager_id"] == my_tm["taskmanager_id"]

    createTime = 1.0
    expirationTime = 3.0
    scheduleTime = 5.0
    creator = "creator"
    schema = 1
    header = datablock.Header(
        my_tm["taskmanager_id"],
        create_time=createTime,
        expiration_time=expirationTime,
        scheduled_create_time=scheduleTime,
        creator=creator,
        schema_id=schema,
    )
    assert header.data["taskmanager_id"] == my_tm["taskmanager_id"]
    assert header.data["create_time"] == createTime
    assert header.data["expiration_time"] == expirationTime
    assert header.data["scheduled_create_time"] == scheduleTime
    assert header.data["creator"] == creator
    assert header.data["schema_id"] == schema


def test_Header_is_valid(dataspace):  # noqa: F811
    my_tm = dataspace.get_taskmanagers()[0]  # fetch one of our loaded examples
    header = datablock.Header(my_tm["taskmanager_id"])

    assert header.is_valid() is True
