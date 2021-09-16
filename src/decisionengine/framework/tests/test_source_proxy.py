"""Fixture based tests of the SourceProxy module."""
# pylint: disable=redefined-outer-name

import os
import re

import pytest

from decisionengine.framework.modules.SourceProxy import SourceProxy
from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)
from decisionengine.framework.tests.WriteToDisk import wait_for_n_writes

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-source-proxy")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


def test_cannot_inherit_from_source_proxy():
    with pytest.raises(RuntimeError, match="Cannot inherit from SourceProxy."):

        class CannotInheritFrom(SourceProxy):
            pass


@pytest.mark.usefixtures("deserver")
def test_single_source_proxy(deserver):
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_source_proxy.*state = STEADY", output, re.DOTALL)

    wait_for_n_writes(deserver.stdout_at_setup, 2)

    deserver.de_client_run_cli("--stop-channel", "test_source_proxy")
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_source_proxy", output, re.DOTALL) is None


_combined_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-combined-channels")  # noqa: F405
deserver_combined = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_combined_channel_config_dir
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver_combined")
def test_combined_channels(deserver_combined):
    # Mimics the 'test_single_source_proxy' workflow but using a
    # combined-configuration approach.
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("test_combined_channels.*state = STEADY", output, re.DOTALL)

    wait_for_n_writes(deserver_combined.stdout_at_setup, 2)

    deserver_combined.de_client_run_cli("--stop-channel", "test_combined_channels")
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("test_combined_channels", output, re.DOTALL) is None


_fail_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-failing-source-proxy")  # noqa: F405
deserver_fail = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_fail_channel_config_dir
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver_fail")
def test_stop_failing_source_proxy(deserver_fail):
    output = deserver_fail.de_client_run_cli("--status")
    assert re.search("test_source_proxy.*state = OFFLINE", output, re.DOTALL)
    deserver_fail.de_client_run_cli("--stop-channel", "test_source_proxy")
    output = deserver_fail.de_client_run_cli("--status")
    assert re.search("test_source_proxy", output, re.DOTALL) is None
