'''Fixture based DE Server tests of invalid channel configs'''
# pylint: disable=redefined-outer-name

import os
import pytest
import re
from logging import ERROR

from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH  # noqa: F401

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, 'test-bad-channel')  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


def _missing_produces(name):
    return f"The following modules are missing '@produces' declarations:\n\n - {name}\n"

def _missing_consumes(name):
    return f"The following modules are missing '@consumes' declarations:\n\n - {name}\n"

def _consumes_not_subset(test_str):
    return "The following products are required but not produced:\n['B']" in test_str

def _expected_circularity(test_str):
    return re.search("Circular dependencies exist among these items: "
                     "{'a_uses_b':{'b_uses_a'}, 'b_uses_a':{'a_uses_b'}}",
                     test_str,
                     re.DOTALL)

@pytest.mark.usefixtures("deserver")
def test_client_can_get_products_no_channels(deserver, caplog):
    '''Verify client can get channel products even when none are run'''
    deserver.de_client_run_cli('--block-while', 'BOOT'),
    output = deserver.de_client_run_cli('--print-products')
    assert 'No channels are currently active.' in output

    error_msgs = [entry.message for entry in caplog.records if entry.levelno == ERROR]
    assert len(error_msgs) == 5

    # Find missing product erro
    consumes_not_subset = next(filter(_consumes_not_subset, error_msgs))
    assert consumes_not_subset
    error_msgs.remove(consumes_not_subset)
    assert len(error_msgs) == 4

    # Find circularity error
    circularity_msg = next(filter(_expected_circularity, error_msgs))
    assert circularity_msg
    error_msgs.remove(circularity_msg)
    assert len(error_msgs) == 3

    # Test missing-list messages
    expected = {'test_bad_publisher': _missing_consumes('publisher1'),
                'test_bad_source': _missing_produces('source1'),
                'test_bad_transform': _missing_produces('transform1') + '\n' + _missing_consumes('transform1')}

    for err_msg in error_msgs:
        channel_name = re.search(r"^Channel (\w+).*", err_msg).groups()[0]
        assert expected[channel_name] in err_msg
