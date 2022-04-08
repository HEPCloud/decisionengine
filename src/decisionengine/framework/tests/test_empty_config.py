# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server tests of adding a channel later on"""
# pylint: disable=redefined-outer-name
import os
import shutil

import pytest

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
    conf_path=TEST_CONFIG_PATH,
    channel_conf_path=None,
    make_conf_dirs_if_missing=True,
)  # pylint: disable=invalid-name


@pytest.mark.timeout(35)
def test_client_can_start_one_channel_added_after_startup(deserver):
    """Verify client can start a single channel"""
    output = deserver.de_client_run_cli("--ping")
    assert "pong" in output
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." in output
    output = deserver.de_client_run_cli("--show-channel-config", "test_channel")
    assert "There is no active channel named test_channel." in output
    output = deserver.de_client_run_cli("--block-while", "BOOT")
    assert "No active channels." in output
    output = deserver.de_client_run_cli("--product-dependencies")
    assert "No sources or channels are currently active." in output

    channel_config = os.path.join(TEST_CHANNEL_CONFIG_PATH, "test_channel.jsonnet")  # noqa: F405
    new_config_path = shutil.copy(channel_config, deserver.channel_conf_path)
    assert os.path.exists(new_config_path)

    # start channel
    output = deserver.de_client_run_cli("--start-channel", "test_channel")
    assert "OK" in output
    output = deserver.de_client_run_cli("--status")
    assert "No sources or channels are currently active." not in output
    assert "test_channel" in output
    assert "state = STEADY" in output
