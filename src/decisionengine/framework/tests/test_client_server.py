# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server for the de-client tests"""
# pylint: disable=redefined-outer-name

import io
import sys

import pytest

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


def test_client_status_msg_to_stdout(deserver):
    """Make sure the actual client console call goes to stdout"""
    import decisionengine.framework.engine.de_client as de_client

    myoutput = io.StringIO()
    sys.stdout = myoutput
    de_client.console_scripts_main(
        ["--host", deserver.server_address[0], "--port", str(deserver.server_address[1]), "--status"]
    )
    sys.stdout = sys.__stdout__
    assert "channel: test_channel" in myoutput.getvalue()


def test_client_set_loglevel(deserver):
    # these shouldn't error out even if the channels are dead
    # they should report the channel is dead, if it did die.
    assert "DEBUG" in deserver.de_client_run_cli("--print-engine-loglevel")
    deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "DEBUG")
    assert "ERROR" in deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "ERROR")


def test_client_print_product(deserver):
    # Test default options
    output = deserver.de_client_run_cli("--print-product", "foo", "--verbose")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+--------+\n"
        "|    | key1   | key2   |\n"
        "|----+--------+--------|\n"
        "|  0 | value1 | 0.1    |\n"
        "|  1 | value2 | 2      |\n"
        "|  2 | value3 | Test   |\n"
        "+----+--------+--------+"
    )

    # Test non-existent product
    output = deserver.de_client_run_cli("--print-product", "NO_SUCH_PRODUCT")
    assert output == "Product NO_SUCH_PRODUCT: Not produced by any module"

    # Test against bad values
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(123)
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(b"123")
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(pytest)
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product({"a": "b"})

    # Test --types
    output = deserver.de_client_run_cli("--print-product", "foo", "--types")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+-------------+--------+-------------+\n"
        "|    | key1   | key1.type   | key2   | key2.type   |\n"
        "|----+--------+-------------+--------+-------------|\n"
        "|  0 | value1 | str         | 0.1    | float       |\n"
        "|  1 | value2 | str         | 2      | int         |\n"
        "|  2 | value3 | str         | Test   | str         |\n"
        "+----+--------+-------------+--------+-------------+"
    )

    # Test specific columns only
    output = deserver.de_client_run_cli("--print-product", "foo", "--columns", "key1")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+\n"
        "|    | key1   |\n"
        "|----+--------|\n"
        "|  0 | value1 |\n"
        "|  1 | value2 |\n"
        "|  2 | value3 |\n"
        "+----+--------+"
    )

    output = deserver.de_client_run_cli("--print-product", "foo", "--columns", "key1,key2")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+--------+\n"
        "|    | key1   | key2   |\n"
        "|----+--------+--------|\n"
        "|  0 | value1 | 0.1    |\n"
        "|  1 | value2 | 2      |\n"
        "|  2 | value3 | Test   |\n"
        "+----+--------+--------+"
    )

    # Test specific columns only
    # Test query
    output = deserver.de_client_run_cli("--print-product", "foo", "--query", "key2 == 2")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+--------+\n"
        "|    | key1   |   key2 |\n"
        "|----+--------+--------|\n"
        "|  1 | value2 |      2 |\n"
        "+----+--------+--------+"
    )

    # Test query and column names
    output = deserver.de_client_run_cli("--print-product", "foo", "--query", "key2 == 2", "--columns", "key2")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+\n"
        "|    |   key2 |\n"
        "|----+--------|\n"
        "|  1 |      2 |\n"
        "+----+--------+"
    )

    output = deserver.de_client_run_cli("--print-product", "foo", "--query", "key2 == 2", "--columns", "key1,key2")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+----+--------+--------+\n"
        "|    | key1   |   key2 |\n"
        "|----+--------+--------|\n"
        "|  1 | value2 |      2 |\n"
        "+----+--------+--------+"
    )

    # Test --format vertical
    output = deserver.de_client_run_cli("--print-product", "foo", "--format", "vertical")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "Row 0\n"
        "+------+--------+\n"
        "| key1 | value1 |\n"
        "| key2 | 0.1    |\n"
        "+------+--------+\n"
        "Row 1\n"
        "+------+--------+\n"
        "| key1 | value2 |\n"
        "| key2 | 2      |\n"
        "+------+--------+\n"
        "Row 2\n"
        "+------+--------+\n"
        "| key1 | value3 |\n"
        "| key2 | Test   |\n"
        "+------+--------+"
    )

    # Test --format column-names
    output = deserver.de_client_run_cli("--print-product", "foo", "--format", "column-names")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "+-----------+\n"
        "| columns   |\n"
        "|-----------|\n"
        "| key1      |\n"
        "| key2      |\n"
        "+-----------+"
    )

    # Test --format json
    output = deserver.de_client_run_cli("--print-product", "foo", "--format", "json")
    assert (
        output == "Product foo:  Found in channel test_channel\n"
        "{\n"
        '    "key1": {\n'
        '        "0": "value1",\n'
        '        "1": "value2",\n'
        '        "2": "value3"\n'
        "    },\n"
        '    "key2": {\n'
        '        "0": 0.1,\n'
        '        "1": 2,\n'
        '        "2": "Test"\n'
        "    }\n"
        "}"
    )
