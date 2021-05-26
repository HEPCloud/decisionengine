'''Fixture based DE Server for the de-query-tool tests'''
# pylint: disable=redefined-outer-name

import pytest
import re

from datetime import datetime

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_PROG,
    DEServer,
    TEST_CONFIG_PATH,
    TEST_CHANNEL_CONFIG_PATH,
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
    "|  6 | value1 | 0.1    | test_channel |                1 |               3 |\n"
    "|  7 | value2 | 2      | test_channel |                1 |               3 |\n"
    "|  8 | value3 | Test   | test_channel |                1 |               3 |\n"
    "+----+--------+--------+--------------+------------------+-----------------+\n"
)

@pytest.mark.usefixtures("deserver")
def test_query_tool_default(deserver):
    # Test default output
    output = deserver.de_query_tool_run_cli('foo')
    assert output == DEFAULT_OUTPUT

@pytest.mark.usefixtures("deserver")
def test_query_tool_csv(deserver):
    # Test csv output
    output = deserver.de_query_tool_run_cli('foo', '--format=csv')
    assert output == (
        "Product foo:  Found in channel test_channel\n"
        ",key1,key2,channel,taskmanager_id,generation_id\n"
        "0,value1,0.1,test_channel,1,1\n"
        "1,value2,2,test_channel,1,1\n"
        "2,value3,Test,test_channel,1,1\n"
        "3,value1,0.1,test_channel,1,2\n"
        "4,value2,2,test_channel,1,2\n"
        "5,value3,Test,test_channel,1,2\n"
        "6,value1,0.1,test_channel,1,3\n"
        "7,value2,2,test_channel,1,3\n"
        "8,value3,Test,test_channel,1,3\n"
        "\n"
    )

@pytest.mark.usefixtures("deserver")
def test_query_tool_json(deserver):
    # Test json output
    output = deserver.de_query_tool_run_cli('foo', '--format=json')
    assert re.match(
        r'Product foo:  Found in channel test_channel\n'
        r'{\n'
        r'\s*"key1":\s*{\n'
        r'\s*"0":\s*"value1",\n\s*"1":\s*"value2",\n\s*"2":\s*"value3",\n'
        r'\s*"3":\s*"value1",\n\s*"4":\s*"value2",\n\s*"5":\s*"value3",\n'
        r'\s*"6":\s*"value1",\n\s*"7":\s*"value2",\n\s*"8":\s*"value3"\n'
        r'\s*},\n'
        r'\s*"key2":\s*{\n'
        r'\s*"0":\s*0.1,\n\s*"1":\s*2,\n\s*"2":\s*"Test",\n'
        r'\s*"3":\s*0.1,\n\s*"4":\s*2,\n\s*"5":\s*"Test",\n'
        r'\s*"6":\s*0.1,\n\s*"7":\s*2,\n\s*"8":\s*"Test"\n'
        r'\s*},\n'
        r'\s*"channel":\s*{\n'
        r'\s*"0":\s*"test_channel",\n\s*"1":\s*"test_channel",\n\s*"2":\s*"test_channel",\n'
        r'\s*"3":\s*"test_channel",\n\s*"4":\s*"test_channel",\n\s*"5":\s*"test_channel",\n'
        r'\s*"6":\s*"test_channel",\n\s*"7":\s*"test_channel",\n\s*"8":\s*"test_channel"\n'
        r'\s*},\n'
        r'\s*"taskmanager_id":\s*{\n'
        r'\s*"0":\s*1,\n\s*"1":\s*1,\n\s*"2":\s*1,\n'
        r'\s*"3":\s*1,\n\s*"4":\s*1,\n\s*"5":\s*1,\n'
        r'\s*"6":\s*1,\n\s*"7":\s*1,\n\s*"8":\s*1\n'
        r'\s*},\n'
        r'\s*"generation_id":\s*{\n'
        r'\s*"0":\s*1,\n\s*"1":\s*1,\n\s*"2":\s*1,\n'
        r'\s*"3":\s*2,\n\s*"4":\s*2,\n\s*"5":\s*2,\n'
        r'\s*"6":\s*3,\n\s*"7":\s*3,\n\s*"8":\s*3\n'
        r'\s*}\n'
        r'}\n',
        output
    )

@pytest.mark.usefixtures("deserver")
def test_query_tool_since(deserver):
    # Test taskmanager start time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = deserver.de_query_tool_run_cli('foo', f'--since="{current_time}"')
    assert output == DEFAULT_OUTPUT

@pytest.mark.usefixtures("deserver")
def test_query_tool_invalid_product(deserver):
    # Test invalid product output
    output = deserver.de_query_tool_run_cli('not_foo')
    assert output == "Product not_foo: Not produced by any module\n"
