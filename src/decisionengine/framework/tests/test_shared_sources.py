# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

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

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-shared-sources-conflicting")  # noqa: F405
deserver_conflicting = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir
)  # pylint: disable=invalid-name


def record_that_matches(substring, records):
    return any(substring in r.message for r in records)


def test_conflicting_source_configurations(deserver_conflicting, caplog):
    assert record_that_matches(
        "Mismatched configurations for source with name source", caplog.get_records(when="setup")
    )


_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-shared-sources")  # noqa: F405
deserver_shared = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir
)  # pylint: disable=invalid-name


def test_shared_source(deserver_shared, caplog):
    assert record_that_matches("Using existing source source for channel D", caplog.get_records(when="setup"))
    output = deserver_shared.de_client_run_cli("--status")
    assert re.search("channel: C.*state = STEADY", output, re.DOTALL)
    assert re.search("channel: D.*state = STEADY", output, re.DOTALL)

    # Take channel C offline and test that the shared source continues to execute
    deserver_shared.de_client_run_cli("--stop-channel", "C")
    output = deserver_shared.de_client_run_cli("--status")
    assert not re.search("channel: C", output, re.DOTALL)
    assert re.search("channel: D.*state = STEADY", output, re.DOTALL)
