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
from decisionengine.framework.tests.WriteToDisk import wait_for_n_writes

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-combined-channels")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


def test_combined_channels(deserver):
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_combined_channels.*state = STEADY", output)

    wait_for_n_writes(deserver.stdout_at_setup, 2)

    output = deserver.de_client_run_cli("--queue-status")
    assert re.search(r"source1\s+source1.*\s+None", output)

    deserver.de_client_run_cli("--stop-channel", "test_combined_channels")
    output = deserver.de_client_run_cli("--status")
    assert re.search("test_combined_channels", output) is None


_combined_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-combined-channels-3g")  # noqa: F405
deserver_combined = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_combined_channel_config_dir
)  # pylint: disable=invalid-name


def test_combined_channels_3g(deserver_combined):
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("last.*state = STEADY", output)

    wait_for_n_writes(deserver_combined.stdout_at_setup, 2)

    output = deserver_combined.de_client_run_cli("--queue-status")
    ref_pattern = r"""
Source name      Queue name\s+      Unconsumed messages
---------------  ------------------------------------------------.*  ---------------------
                 client\.requests\s+      None
                 client\.requests\.listener\.de_client\s+ None
first_source     first_source.*          None
first_source     first_source\.last.*    None
last_source_A    last_source_A.*         None
last_source_A    last_source_A\.last.*   None
last_source_B    last_source_B.*         None
last_source_B    last_source_B\.last.*   None
second_source_A  second_source_A.*       None
second_source_A  second_source_A\.last.* None
second_source_B  second_source_B.*       None
second_source_B  second_source_B\.last.* None
second_source_C  second_source_C.*       None
second_source_C  second_source_C\.last.* None"""
    assert re.search(ref_pattern, output)

    output = deserver_combined.de_client_run_cli("--product-dependencies", "-v")
    ref_pattern = (
        r"sources\s+first_source:\s+produces:.*_a.*"
        + r"transforms:\s+first_transform\s+consumes:.*_a.*produces.*a.*"
        + r"publishers:\s+last_publisher\s+consumes:.*tA"
    )
    assert re.search(ref_pattern, output, re.DOTALL)

    deserver_combined.de_client_run_cli("--stop-channel", "last")
    output = deserver_combined.de_client_run_cli("--status")
    assert re.search("last", output) is None
