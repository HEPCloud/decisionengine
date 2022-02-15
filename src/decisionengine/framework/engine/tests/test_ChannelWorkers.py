# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

import decisionengine.framework.config.policies as policies

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.engine.ChannelWorkers import ChannelWorker
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


class TaskManager:
    name = "test_channel"

    def set_loglevel_value(self, value):
        pass


_TASK_MANAGER = TaskManager()


@pytest.fixture()
def global_config(dataspace):  # noqa: F811
    conf = ValidConfig(policies.global_config_file(_CONFIG_PATH))
    conf["dataspace"] = dataspace.config["dataspace"]
    yield conf


def test_worker_name(global_config):
    worker = ChannelWorker(_TASK_MANAGER, global_config["logger"])

    assert worker.name == f"DEChannelWorker-{_TASK_MANAGER.name}"


def test_worker_logger_sized_rotation(global_config):
    worker = ChannelWorker(_TASK_MANAGER, global_config["logger"])
    worker.setup_logger()

    assert "RotatingFileHandler" in str(worker.logger.handlers)


def test_worker_logger_timed_rotation(global_config):
    global_config["logger"]["file_rotate_by"] = "time"
    worker = ChannelWorker(_TASK_MANAGER, global_config["logger"])
    worker.setup_logger()

    assert "TimedRotatingFileHandler" in str(worker.logger.handlers)
