# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server tests of the defaults"""
# pylint: disable=redefined-outer-name

import re

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


def stopped_channel_opts(timeout=1):
    maybe_s = "s" if timeout != 1 else ""
    return [
        "Channel test_channel stopped cleanly.",
        f"Channel test_channel has been killed due to shutdown timeout ({timeout} second{maybe_s}).",
        "Channel test_channel has been killed.",
    ]


def test_client_can_get_de_server_status(deserver):
    # Verify channel enters stable state
    output = deserver.de_client_run_cli("--status")
    assert "state = STEADY" in output

    # Verify present modules
    output = deserver.de_client_run_cli("--show-config")
    assert "decisionengine.framework.tests.SourceNOP" in output
    assert "decisionengine.framework.tests.TransformNOP" in output

    # Verify channel config has expected items
    output = deserver.de_client_run_cli("--show-channel-config", "test_channel")
    assert "test_channel" in output
    assert "decisionengine.framework.tests.SourceNOP" in output
    assert "decisionengine.framework.tests.TransformNOP" in output

    # Verify client can get channel products
    output = deserver.de_client_run_cli("--print-products")
    assert "source1" in output
    assert "transform1" in output

    # make sure this doesn't crash the tests
    deserver.de_client_run_cli("--metrics")

    # Verify timeout works
    output = deserver.de_client_run_cli("--block-while", "STEADY", "--timeout", "3")
    re.search("The following channels are still in STEADY state.*test_channel.", output, re.DOTALL)
    output = deserver.de_client_run_cli("--status")
    assert "state = STEADY" in output

    # Verify client cannot double start channels
    output = deserver.de_client_run_cli("--start-channel", "test_channel")
    assert "test_channel is running" in output

    # Verify de-client can run --stop
    output = deserver.de_client_run_cli("--stop")
    assert "OK" in output


def test_client_can_restart_all_channels(deserver):
    """Verify client can get channel products even when none are run"""
    output = deserver.de_client_run_cli("--stop-channels")
    assert "All channels stopped." in output
    output = deserver.de_client_run_cli("--print-products")
    assert "No channels are currently active." in output
    output = deserver.de_client_run_cli("--start-channels")
    assert "No sources or channels are currently active." not in output


def test_client_can_restart_one_channel(deserver):
    """Verify client can restart a single channel"""
    output = deserver.de_client_run_cli("--stop-channel", "test_channel")
    assert "Channel test_channel stopped cleanly." in output
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." in output
    output = deserver.de_client_run_cli("--start-channel", "test_channel")
    assert "No sources or channels are currently active." not in output


def test_client_can_kill_one_channel(deserver):
    # Verify client can kill a single channel
    output = deserver.de_client_run_cli("--kill-channel", "test_channel")
    assert output in stopped_channel_opts()
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." in output

    # Verify client can kill a single channel with force
    output = deserver.de_client_run_cli("--start-channel", "test_channel")
    assert "OK" in output
    output = deserver.de_client_run_cli("--kill-channel", "test_channel", "--force")
    assert output in stopped_channel_opts()
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." in output

    # Verify client can kill a single channel with timeout
    output = deserver.de_client_run_cli("--start-channel", "test_channel")
    assert "OK" in output
    output = deserver.de_client_run_cli("--kill-channel", "test_channel", "--timeout", "5")
    assert output in stopped_channel_opts(5)
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." in output


def test_client_non_real_channel(deserver):
    # Verify correct handling of config for missing channel
    output = deserver.de_client_run_cli("--show-channel-config", "ISNT_REAL")
    assert "There is no active channel named ISNT_REAL." in output

    # Verify start for missing channel does what it should
    output = deserver.de_client_run_cli("--start-channel", "ISNT_REAL")
    assert "Failed to open channel configuration file" in output

    # Verify stop for missing channel does what it should
    output = deserver.de_client_run_cli("--stop-channel", "ISNT_REAL")
    assert "No channel found with the name ISNT_REAL." in output

    # Verify graceful fail on bogus channel
    output = deserver.de_client_run_cli("--get-channel-loglevel", "ISNT_REAL")
    assert output == "No channel found with the name ISNT_REAL."

    output = deserver.de_client_run_cli("--set-channel-loglevel", "ISNT_REAL", "DEBUG")
    assert output == "No channel found with the name ISNT_REAL."


def test_client_logger_level(deserver):
    # Verify can fetch log level
    output = deserver.de_client_run_cli("--print-engine-loglevel")
    assert output in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    # Verify can fetch log level for a channel
    output = deserver.de_client_run_cli("--get-channel-loglevel", "test_channel")
    assert output in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    # Verify can fetch log level for a source
    output = deserver.de_client_run_cli("--get-source-loglevel", "source1")
    assert output in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    # Verify set log level for a channel
    output = deserver.de_client_run_cli("--set-channel-loglevel", "test_channel", "DEBUG")
    output = deserver.de_client_run_cli("--get-channel-loglevel", "test_channel")
    assert output == "DEBUG"

    # Verify set log level for a source
    output = deserver.de_client_run_cli("--set-source-loglevel", "source1", "DEBUG")
    output = deserver.de_client_run_cli("--get-source-loglevel", "source1")
    assert output == "DEBUG"
