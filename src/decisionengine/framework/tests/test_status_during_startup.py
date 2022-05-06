# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# pylint: disable=redefined-outer-name

import os
import re

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-combined-channels")  # noqa: F405
deserver_no_wait = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir, block_until_startup_complete=False
)


def test_status_during_startup(deserver_no_wait):
    output = deserver_no_wait.de_client_run_cli("--status")
    ref_pattern_none = r"""No sources or channels are currently active.

reaper: state = IDLE"""

    ref_pattern_launched = r"""
source: source1, queue id = source1.*, state = (BOOT|ACTIVE|STEADY)

channel: test_combined_channels, id = .*, state = (BOOT|ACTIVE|STEADY)

reaper: state = IDLE"""
    assert re.search(ref_pattern_none, output, re.DOTALL) or re.search(ref_pattern_launched, output, re.DOTALL)
