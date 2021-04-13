'''Fixture based DE Server tests of invalid channel configs'''
# pylint: disable=redefined-outer-name

import os
import pytest

from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH  # noqa: F401

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, 'test-bad-channel')  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_client_can_get_products_no_channels(deserver, caplog):
    '''Verify client can get channel products even when none are run'''
    deserver.de_client_run_cli('--block-while', 'BOOT'),
    output = deserver.de_client_run_cli('--print-products')
    assert 'No channels are currently active.' in output

    error_logs = []
    for logentry in caplog.records:
        if logentry.levelname == 'ERROR':
            error_logs.append(logentry.message)
    assert len(error_logs) >= 2

    assert 'source module source1 does not have required PRODUCES list' in caplog.text
    assert "has no attribute 'CONSUMES'" in caplog.text
