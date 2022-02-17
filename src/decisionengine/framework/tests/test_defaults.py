# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server tests of the sample config"""
# pylint: disable=redefined-outer-name

import json

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


def test_defaults(deserver):
    # Verify unknown channel has NOTSET
    output = deserver.de_client_run_cli("--get-channel-loglevel=UNITTEST")
    assert output == "NOTSET"

    # Verify global_channel_log_level setting exists
    output = deserver.de_client_run_cli("--show-de-config")
    assert "global_channel_log_level" in output

    # Verify config is JSON-formatted
    assert json.loads(output)
