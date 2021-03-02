'''Fixture based DE Server tests of the server without channels, then with them'''
# pylint: disable=redefined-outer-name

import os
import re

import pytest

from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block  # noqa: F401
from decisionengine.framework.tests.fixtures import DE_DB, DEServer, PG_PROG, TEST_CONFIG_PATH  # noqa: F401

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, 'test-failing-source-proxy')  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_stop_failing_source_proxy(deserver):
    # The following 'block-while' call be unnecessary once the
    # deserver fixture can reliably block when no workers have yet
    # been constructed.
    deserver.de_client_run_cli("--block-while", "BOOT")
    output = deserver.de_client_run_cli('--status')
    assert re.search("test_source_proxy.*state = OFFLINE", output, re.DOTALL)
    deserver.de_client_run_cli('--stop-channel', 'test_source_proxy')
    output = deserver.de_client_run_cli('--status')
    assert re.search("test_source_proxy", output, re.DOTALL) is None
