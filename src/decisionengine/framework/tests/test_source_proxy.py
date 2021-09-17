"""Fixture based tests of the SourceProxy module."""
# pylint: disable=redefined-outer-name

import os
import re

import pytest

from decisionengine.framework.dataspace.datasources.tests.fixtures import mock_data_block  # noqa: F401
from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-source-proxy")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_working_source_proxy(deserver):
    # The following 'block-while' call be unnecessary once the
    # deserver fixture can reliably block when no workers have yet
    # been constructed.
    deserver.de_client_run_cli("--block-while", "BOOT")
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_source_proxy.*state = STEADY", output, re.DOTALL)
    deserver.de_client_run_cli("--stop-channel", "test_source_proxy")
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_source_proxy", output, re.DOTALL) is None


_fail_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-failing-source-proxy")  # noqa: F405
deserver_fail = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_fail_channel_config_dir
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver_fail")
def test_stop_failing_source_proxy(deserver_fail):
    # The following 'block-while' call be unnecessary once the
    # deserver fixture can reliably block when no workers have yet
    # been constructed.
    deserver_fail.de_client_run_cli("--block-while", "BOOT")
    output = deserver_fail.de_client_run_cli("--status")
    assert re.search("test_source_proxy.*state = OFFLINE", output, re.DOTALL)
    deserver_fail.de_client_run_cli("--stop-channel", "test_source_proxy")
    output = deserver_fail.de_client_run_cli("--status")
    assert re.search("test_source_proxy", output, re.DOTALL) is None
