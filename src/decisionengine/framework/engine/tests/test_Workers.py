# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

import pytest

import decisionengine.framework.config.policies as policies

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.engine.Workers import Worker
from decisionengine.framework.taskmanager.TaskManager import TaskManager
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

channel = "test_channel"


def get_channel_config(name):
    return ValidConfig(os.path.join(_CHANNEL_CONFIG_DIR, name + ".jsonnet"))


@pytest.fixture()
@pytest.mark.usefixtures("dataspace")
def global_config(dataspace):  # noqa: F811
    conf = ValidConfig(policies.global_config_file(_CONFIG_PATH))
    conf["dataspace"] = dataspace.config["dataspace"]
    yield conf


@pytest.fixture()
@pytest.mark.usefixtures("global_config")
def task_manager(global_config):
    task_manager = TaskManager(channel, get_channel_config(channel), global_config)
    yield task_manager

    gc.collect()


@pytest.mark.usefixtures("task_manager", "global_config")
def test_worker_name(task_manager, global_config):
    worker = Worker(task_manager, global_config["logger"])

    assert worker.name == f"DEWorker-{task_manager.name}"


@pytest.mark.usefixtures("task_manager", "global_config")
def test_worker_logger_sized_rotation(task_manager, global_config):
    worker = Worker(task_manager, global_config["logger"])
    worker.setup_logger()

    assert "RotatingFileHandler" in str(worker.logger.handlers)


@pytest.mark.usefixtures("task_manager", "global_config")
def test_worker_logger_timed_rotation(task_manager, global_config):
    global_config["logger"]["file_rotate_by"] = "time"
    worker = Worker(task_manager, global_config["logger"])
    worker.setup_logger()

    assert "TimedRotatingFileHandler" in str(worker.logger.handlers)
