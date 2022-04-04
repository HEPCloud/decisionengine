# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import re
import time

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


def test_error_on_acquire(deserver):
    deserver.de_client_run_cli("--block-while", "SHUTTINGDOWN")
    time.sleep(5)  # Should be enough time for source2 to come offline.
    output = deserver.de_client_run_cli("--status")
    assert re.search(r"source1.*ERROR.*source2.*(STEADY|OFFLINE).*error_on_acquire.*OFFLINE", output, re.DOTALL)
    output = deserver.de_client_run_cli("--stop-channel", "error_on_acquire")
    assert output == "Channel error_on_acquire stopped cleanly."
