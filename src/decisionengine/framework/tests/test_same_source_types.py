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

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-same-source-types-separate-channels")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


def test_same_source_types_separate_channels(deserver):
    # Channels A and B both have sources of type IntSource, which
    # creates a product with the name "int_value".  This test verifies
    # that the publisher in channel A (B) reads the product produced by
    # channel A (B).
    output = deserver.de_client_run_cli("--status")
    assert re.search("channel: A.*state = STEADY", output, re.DOTALL)
    assert re.search("channel: B.*state = STEADY", output, re.DOTALL)
