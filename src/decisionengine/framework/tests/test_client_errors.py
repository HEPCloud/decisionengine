# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based DE Server tests of the sample config"""
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


def test_client_cannot_wait_on_bad_state(deserver):
    """Verify wait is for a valid state"""
    output = deserver.de_client_run_cli("--block-while=INVALID_STATE")
    assert output == "INVALID_STATE is not a valid channel state."
