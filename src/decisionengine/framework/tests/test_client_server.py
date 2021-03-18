'''Fixture based DE Server for the de-client tests'''
# pylint: disable=redefined-outer-name

import io
import sys

import pytest

from decisionengine.framework.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA # noqa: F401
from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH # noqa: F401

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH) # pylint: disable=invalid-name

@pytest.mark.usefixtures("deserver")
def test_client_status_msg_to_stdout(deserver):
    """Make sure the actuall client console call goes to stdout"""
    import decisionengine.framework.engine.de_client as de_client

    myoutput = io.StringIO()
    sys.stdout = myoutput
    de_client.console_scripts_main(['--host', deserver.server_address[0],
                                    '--port', str(deserver.server_address[1]),
                                    '--status'])
    sys.stdout = sys.__stdout__
    assert 'channel: test_channel' in myoutput.getvalue()

@pytest.mark.usefixtures("deserver")
def test_client_print_product(deserver):
    # Test default options
    output = deserver.de_client_run_cli('--print-product', 'foo')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+--------+\n" \
        "|    | key1   | key2   |\n" \
        "|----+--------+--------|\n" \
        "|  0 | value1 | 0.1    |\n" \
        "|  1 | value2 | 2      |\n" \
        "|  2 | value3 | Test   |\n" \
        "+----+--------+--------+"
    output = deserver.de_client_run_cli('--print-product', 'NO_SUCH_PRODUCT')
    assert output == "Product NO_SUCH_PRODUCT: Not produced by any module"

    # Test --types
    output = deserver.de_client_run_cli('--print-product', 'foo', '--types')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+-------------+--------+-------------+\n" \
        "|    | key1   | key1.type   | key2   | key2.type   |\n" \
        "|----+--------+-------------+--------+-------------|\n" \
        "|  0 | value1 | str         | 0.1    | float       |\n" \
        "|  1 | value2 | str         | 2      | int         |\n" \
        "|  2 | value3 | str         | Test   | str         |\n" \
        "+----+--------+-------------+--------+-------------+"

    # Test specific columns only
    output = deserver.de_client_run_cli('--print-product', 'foo', '--columns', 'key1')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+\n" \
        "|    | key1   |\n" \
        "|----+--------|\n" \
        "|  0 | value1 |\n" \
        "|  1 | value2 |\n" \
        "|  2 | value3 |\n" \
        "+----+--------+"

    output = deserver.de_client_run_cli('--print-product', 'foo', '--columns', 'key1,key2')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+--------+\n" \
        "|    | key1   | key2   |\n" \
        "|----+--------+--------|\n" \
        "|  0 | value1 | 0.1    |\n" \
        "|  1 | value2 | 2      |\n" \
        "|  2 | value3 | Test   |\n" \
        "+----+--------+--------+"

    # Test query
    output = deserver.de_client_run_cli('--print-product', 'foo', '--query', 'key2 == 2')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+--------+\n" \
        "|    | key1   |   key2 |\n" \
        "|----+--------+--------|\n" \
        "|  1 | value2 |      2 |\n" \
        "+----+--------+--------+"

    # Test query and column names
    output = deserver.de_client_run_cli('--print-product', 'foo', '--query', 'key2 == 2', '--columns', 'key2')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+\n" \
        "|    |   key2 |\n" \
        "|----+--------|\n" \
        "|  1 |      2 |\n" \
        "+----+--------+"

    output = deserver.de_client_run_cli('--print-product', 'foo', '--query', 'key2 == 2', '--columns', 'key1,key2')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+----+--------+--------+\n" \
        "|    | key1   |   key2 |\n" \
        "|----+--------+--------|\n" \
        "|  1 | value2 |      2 |\n" \
        "+----+--------+--------+"


    # Test --format vertical
    output = deserver.de_client_run_cli('--print-product', 'foo', '--format', 'vertical')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "Row 0\n" \
        "+------+--------+\n" \
        "| key1 | value1 |\n" \
        "| key2 | 0.1    |\n" \
        "+------+--------+\n" \
        "Row 1\n" \
        "+------+--------+\n" \
        "| key1 | value2 |\n" \
        "| key2 | 2      |\n" \
        "+------+--------+\n" \
        "Row 2\n" \
        "+------+--------+\n" \
        "| key1 | value3 |\n" \
        "| key2 | Test   |\n" \
        "+------+--------+"

    # Test --format column-names
    output = deserver.de_client_run_cli('--print-product', 'foo', '--format', 'column-names')
    assert output == \
        "Product foo:  Found in channel test_channel\n" \
        "+-----------+\n" \
        "| columns   |\n" \
        "|-----------|\n" \
        "| key1      |\n" \
        "| key2      |\n" \
        "+-----------+"

# Test --format json
    output = deserver.de_client_run_cli('--print-product', 'foo', '--format', 'json')
    assert output == \
        'Product foo:  Found in channel test_channel\n' \
        '{\n' \
        '    "key1": {\n' \
        '        "0": "value1",\n' \
        '        "1": "value2",\n' \
        '        "2": "value3"\n' \
        '    },\n' \
        '    "key2": {\n' \
        '        "0": 0.1,\n' \
        '        "1": 2,\n' \
        '        "2": "Test"\n' \
        '    }\n' \
        '}'
