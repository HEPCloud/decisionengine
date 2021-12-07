# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""defaults for pytest"""
import os

# load DE Server fixtures
# even though we are only using DEServer
# we need to import all of these to instantiate the other fixtures
# so that DEServer gets setup correctly
from decisionengine.framework.engine.tests.fixtures import (
    DEServer,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)

# set path to test config
TEST_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etc/decisionengine")
TEST_CHANNEL_CONFIG_PATH = os.path.join(TEST_CONFIG_PATH, "config.d")

__all__ = [
    "PG_DE_DB_WITHOUT_SCHEMA",
    "PG_PROG",
    "SQLALCHEMY_PG_WITH_SCHEMA",
    "SQLALCHEMY_TEMPFILE_SQLITE",
    "DEServer",
    "TEST_CONFIG_PATH",
    "TEST_CHANNEL_CONFIG_PATH",
]
