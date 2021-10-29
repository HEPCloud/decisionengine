"""Fixture based tests of the SourceProxy module (tests three generations of source-proxies)."""
# pylint: disable=redefined-outer-name

import os
import re

import pytest

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)
from decisionengine.framework.tests.WriteToDisk import wait_for_n_writes

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-source-proxy-3g")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_many_source_proxies(deserver):
    output = deserver.de_client_run_cli("--status")
    assert re.search("last.*state = STEADY", output, re.DOTALL)

    wait_for_n_writes(deserver.stdout_at_setup, 2)

    deserver.de_client_run_cli("--stop-channel", "last")
    output = deserver.de_client_run_cli("--status")
    assert re.search("last", output, re.DOTALL) is None


_combined_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-combined-channels-3g")  # noqa: F405
deserver_combined = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_combined_channel_config_dir
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver_combined")
def test_combined_channels_3g(deserver_combined):
    # Mimics the 'test_many_source_proxies' workflow but using a
    # combined-configuration approach.
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("last.*state = STEADY", output, re.DOTALL)

    wait_for_n_writes(deserver_combined.stdout_at_setup, 2)

    deserver_combined.de_client_run_cli("--stop-channel", "last")
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("last", output, re.DOTALL) is None
