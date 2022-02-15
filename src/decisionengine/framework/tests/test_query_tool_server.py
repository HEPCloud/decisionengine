# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server for the de-query-tool tests"""
# pylint: disable=redefined-outer-name

import datetime
import json

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CHANNEL_CONFIG_PATH,
    TEST_CONFIG_PATH,
)

deserver = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH
)  # pylint: disable=invalid-name

DEFAULT_OUTPUT = (
    "Product foo:  Found in channel test_channel\n"
    "+----+--------+--------+--------------+------------------+-----------------+\n"
    "|    | key1   | key2   | channel      |   taskmanager_id |   generation_id |\n"
    "|----+--------+--------+--------------+------------------+-----------------|\n"
    "|  0 | value1 | 0.1    | test_channel |                1 |               1 |\n"
    "|  1 | value2 | 2      | test_channel |                1 |               1 |\n"
    "|  2 | value3 | Test   | test_channel |                1 |               1 |\n"
    "|  3 | value1 | 0.1    | test_channel |                1 |               2 |\n"
    "|  4 | value2 | 2      | test_channel |                1 |               2 |\n"
    "|  5 | value3 | Test   | test_channel |                1 |               2 |\n"
)


def test_query_tool(deserver):
    # Test default output
    output = deserver.de_query_tool_run_cli("foo")
    assert output.startswith(DEFAULT_OUTPUT)

    # Test csv output
    output = deserver.de_query_tool_run_cli("foo", "--format=csv")
    assert output.startswith(
        "Product foo:  Found in channel test_channel\n"
        ",key1,key2,channel,taskmanager_id,generation_id\n"
        "0,value1,0.1,test_channel,1,1\n"
        "1,value2,2,test_channel,1,1\n"
        "2,value3,Test,test_channel,1,1\n"
        "3,value1,0.1,test_channel,1,2\n"
        "4,value2,2,test_channel,1,2\n"
        "5,value3,Test,test_channel,1,2\n"
    )

    # Test json output
    output = deserver.de_query_tool_run_cli("foo", "--format=json")
    assert output.startswith("Product foo:  Found in channel test_channel\n")

    as_json = json.loads(output.replace("Product foo:  Found in channel test_channel\n", ""))
    elements = list(as_json.keys())
    elements.sort()

    assert elements == ["channel", "generation_id", "key1", "key2", "taskmanager_id"]
    for element in elements:
        assert isinstance(as_json[element], dict)

    assert as_json["channel"]["0"] == "test_channel"
    assert as_json["channel"]["1"] == "test_channel"
    assert as_json["generation_id"]["0"] == 1
    assert as_json["generation_id"]["1"] == 1
    assert as_json["generation_id"]["2"] == 1
    assert as_json["generation_id"]["3"] == 2
    assert as_json["taskmanager_id"]["0"] == 1
    assert as_json["taskmanager_id"]["1"] == 1
    assert as_json["key1"]["0"] == "value1"
    assert as_json["key2"]["0"] == 0.1
    assert as_json["key1"]["1"] == "value2"
    assert as_json["key2"]["1"] == 2
    assert as_json["key1"]["2"] == "value3"
    assert as_json["key2"]["2"] == "Test"
    assert as_json["key1"]["3"] == "value1"
    assert as_json["key2"]["3"] == 0.1

    # Query tool since
    recently = datetime.datetime.now() - datetime.timedelta(minutes=3)
    output = deserver.de_query_tool_run_cli("foo", f'--since="{recently.strftime("%Y-%m-%d %H:%M:%S")}"')
    assert output.startswith(DEFAULT_OUTPUT)

    # Test invalid product output
    output = deserver.de_query_tool_run_cli("not_foo")
    assert output == "Product not_foo: Not produced by any module\n"
