# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-error-on-acquire")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


def test_source_only_channel(deserver):
    output = deserver.de_client_run_cli("--stop-channel", "error_on_acquire")
    assert output == "Channel error_on_acquire stopped cleanly."
