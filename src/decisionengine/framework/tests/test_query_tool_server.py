'''Fixture based DE Server for the de-query-tool tests'''
# pylint: disable=redefined-outer-name

import io
import re
import sys

import pytest

from decisionengine.framework.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA # noqa: F401
from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH # noqa: F401

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH) # pylint: disable=invalid-name

def test_query_tool_default(deserver):
    # Test default output
    output = deserver.de_query_tool_run_cli('foo')
    assert output == (
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

def test_query_tool_default_csv(deserver):
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
