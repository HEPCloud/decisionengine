'''Fixture based DE Server tests of invalid channel configs'''
# pylint: disable=redefined-outer-name

import os
import pytest
import re
from logging import ERROR

from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH  # noqa: F401

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, 'test-bad-channel')  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


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
    assert len(error_msgs) == 4

    # Find circularity error
    circularity_msg = next(filter(_expected_circularity, error_msgs))
    assert circularity_msg

    # Remove circularity error now that we have verified it
    error_msgs.remove(circularity_msg)
    assert len(error_msgs) == 3

    # Test missing produces/consumes errors
    expected_missing_lists = {'source1': 'PRODUCES',
                              'transform1': 'PRODUCES',
                              'publisher1': 'CONSUMES'}
    for err_msg in error_msgs:
        match = re.match(r'.*module (\w+) does not have a (\w+) list.*', err_msg, re.DOTALL)
        assert match
        module_name, missing_list = match.groups()
        assert missing_list == expected_missing_lists[module_name]
