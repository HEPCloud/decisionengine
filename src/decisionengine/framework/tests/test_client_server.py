# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server for the de-client tests"""
# pylint: disable=redefined-outer-name

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


def test_client_status_msg_to_logger(deserver, caplog):
    """Make sure the actual client console call goes to a logging destination"""
    import decisionengine.framework.engine.de_client as de_client

    de_client.console_scripts_main(
        ["--host", deserver.server_address[0], "--port", str(deserver.server_address[1]), "--status"]
    )
    assert any(filter(lambda r: r.msg.startswith("channel: test_channel") and r.name == "de_client", caplog.records))


def test_client_set_loglevel(deserver):
    # these shouldn't error out even if the channels are dead
    # they should report the channel is dead, if it did die.
    assert "DEBUG" in deserver.de_client_run_cli("--print-engine-loglevel")

    # channel logger tests
    deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "DEBUG")
    output = deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "DEBUG")
    assert output == "Nothing to do. Current log level is : DEBUG"
    assert "ERROR" in deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "ERROR")
    output = deserver.de_client_run_cli("--set-channel-loglevel", "bad_channel", "DEBUG")
    assert output == "No channel found with the name bad_channel."

    # source logger tests
    deserver.de_client_run_cli("--set-source-loglevel", "source1", "DEBUG")
    output = deserver.de_client_run_cli("--set-source-loglevel", "source1", "DEBUG")
    assert output == "Nothing to do. Current log level is : DEBUG"
    assert "ERROR" in deserver.de_client_run_cli("--set-source-loglevel", "source1", "ERROR")
    output = deserver.de_client_run_cli("--set-source-loglevel", "bad_source", "DEBUG")
    assert output == "No source found with the name bad_source."


def test_client_get_loglevel(deserver):
    output = deserver.de_client_run_cli("--get-channel-loglevel", "bad_channel")
    assert output == "No channel found with the name bad_channel."

    output = deserver.de_client_run_cli("--get-source-loglevel", "bad_source")
    assert output == "No source found with the name bad_source."


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
        deserver.de_server.rpc_print_product(None, 123)
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(None, b"123")
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(None, pytest)
    with pytest.raises(ValueError, match=r"Requested product should be a string.*"):
        deserver.de_server.rpc_print_product(None, {"a": "b"})

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
