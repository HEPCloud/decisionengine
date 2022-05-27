# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

import kombu
import pytest

import decisionengine.framework.config.policies as policies

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.engine.SourceWorkers import SourceWorker
from decisionengine.framework.taskmanager.tests.fixtures import (  # noqa: F401
    DATABASES_TO_TEST,
    dataspace,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)

_CWD = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_CWD, "../../tests/etc/decisionengine")
_CHANNEL_CONFIG_DIR = os.path.join(_CWD, "config")

_KEY = "test_key"
_CHANNEL_NAME = "test_channel"
_SOURCE_NAME = "source1"
_BROKER_URL = "redis://localhost:6379/14"  # Use 14 to avoid collisions with other tests
_EXCHANGE = kombu.Exchange("test_topic_exchange", "topic")


@pytest.fixture()
def global_config(dataspace):  # noqa: F811
    conf = ValidConfig(policies.global_config_file(_CONFIG_PATH))
    conf["dataspace"] = dataspace.config["dataspace"]
    yield conf


def source_config(channel_name, source_name):
    ch_config = ValidConfig(os.path.join(_CHANNEL_CONFIG_DIR, channel_name + ".jsonnet"))
    src_config = ch_config["sources"]
    return src_config[source_name]


def source_worker_for(src_config, global_config):
    return SourceWorker(_KEY, src_config, global_config["logger"], _CHANNEL_NAME, _EXCHANGE, _BROKER_URL)


def test_worker_name(global_config):
    src_config = source_config(_CHANNEL_NAME, _SOURCE_NAME)
    worker = source_worker_for(src_config, global_config)
    assert worker.name == f"SourceWorker-{_KEY}"


def test_worker_logger_sized_rotation(global_config):
    src_config = source_config(_CHANNEL_NAME, _SOURCE_NAME)
    worker = source_worker_for(src_config, global_config)
    worker.setup_logger()

    assert "RotatingFileHandler" in str(worker.logger.handlers)


def test_worker_logger_timed_rotation(global_config):
    global_config["logger"]["file_rotate_by"] = "time"
    src_config = source_config(_CHANNEL_NAME, _SOURCE_NAME)
    worker = source_worker_for(src_config, global_config)
    worker.setup_logger()

    assert "TimedRotatingFileHandler" in str(worker.logger.handlers)


def test_worker_logger_wrong_rotation_method(global_config):
    global_config["logger"]["file_rotate_by"] = "test"
    src_config = source_config(_CHANNEL_NAME, _SOURCE_NAME)
    worker = source_worker_for(src_config, global_config)

    with pytest.raises(ValueError):
        worker.setup_logger()
