# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server for the reaper tests"""
# pylint: disable=redefined-outer-name

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


def test_client_can_get_de_server_reaper_status(deserver):
    """Verify reaper status"""
    output = deserver.de_client_run_cli("--reaper-status")

    # find reaper section
    assert "reaper:" in output

    # find reaper state section
    assert "state:" in output

    # find reaper interval
    assert "retention_interval:" in output

    # Verify reaper can stop
    output = deserver.de_client_run_cli("--reaper-stop")
    assert output == "OK"

    # get status to be sure
    output = deserver.de_client_run_cli("--reaper-status")

    # find reaper section
    assert "reaper:" in output

    # find reaper state section
    assert "state:" in output

    # find reaper state value
    assert "State.SHUTDOWN" in output

    # Verify reaper can start with delay
    output = deserver.de_client_run_cli("--reaper-start", "--reaper-start-delay-secs=90")
    assert output == "OK"

    # get status to be sure
    output = deserver.de_client_run_cli("--reaper-status")

    # find reaper section
    assert "reaper:" in output

    # find reaper state section
    assert "state:" in output

    # find reaper state value
    assert "State.IDLE" in output
