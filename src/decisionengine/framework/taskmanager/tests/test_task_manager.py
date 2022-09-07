# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import random
import string

import kombu
import pytest
import redis

import decisionengine.framework.config.policies as policies

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.dataspace import datablock
from decisionengine.framework.dataspace.dataspace import DataSpace
from decisionengine.framework.engine.ChannelWorkers import ChannelWorker
from decisionengine.framework.engine.SourceWorkers import SourceWorkers
from decisionengine.framework.taskmanager.module_graph import source_products, validated_workflow
from decisionengine.framework.taskmanager.TaskManager import State, TaskManager
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
_CHANNEL_CONFIG_DIR = os.path.join(_CWD, "channels")

_BROKER_URL = "redis://localhost:6379/14"  # Use 14 to avoid collisions with other tests
_EXCHANGE = kombu.Exchange("test_topic_exchange", "topic")


def random_suffix():
    return "".join(random.choice(string.ascii_letters) for _ in range(8))


def channel_config(channel_name):
    return ValidConfig(os.path.join(_CHANNEL_CONFIG_DIR, channel_name + ".jsonnet"))


def source_workers(channel_name, source_configs, logger_config):
    src_workers = SourceWorkers(_EXCHANGE, _BROKER_URL)
    return src_workers, src_workers.update(channel_name, source_configs, logger_config)


def task_manager_for(global_config, channel_name, ch_config=None, src_workers=None):
    if ch_config is None:
        ch_config = channel_config(channel_name)
    # If the channel name is not specified in the configuration, we
    # add a random string onto the end so that we can inspect log
    # files from tests that all use "test_channel.jsonnet"--the suffix
    # ensures that we avoid file collisions.
    channel_name = ch_config.get("channel_name", channel_name + "-" + random_suffix())
    if src_workers is None:
        _, src_workers = source_workers(channel_name, ch_config["sources"], global_config["logger"])
    keys = [worker.key for worker in src_workers.values()]
    module_workers = validated_workflow(channel_name, src_workers, ch_config)
    return TaskManager(
        channel_name,
        module_workers,
        DataSpace(global_config),
        source_products(module_workers["sources"]),
        exchange=_EXCHANGE,
        broker_url=_BROKER_URL,
        routing_keys=keys,
    )


class RunChannel:
    def __init__(self, global_config, channel):
        ch_config = channel_config(channel)
        src_workers, workers_to_start = source_workers(channel, ch_config["sources"], global_config["logger"])
        self._source_workers = src_workers
        self._workers_to_start = workers_to_start
        self._tm = task_manager_for(global_config, channel, ch_config, self._workers_to_start)
        self._channel_worker = ChannelWorker(self._tm, global_config["logger"])

    def __enter__(self):
        self._channel_worker.start()
        self._tm.state.wait_while(State.BOOT)

        # Start any sources that are not yet alive.
        for key, src_worker in self._workers_to_start.items():
            if src_worker.is_alive():
                continue

            src_worker.start()

        self._tm.state.wait_while(State.ACTIVE)
        return self._tm

    def __exit__(self, type, value, traceback):
        if type:
            return False
        self._channel_worker.join()
        self._source_workers.remove_all(None)


@pytest.fixture(scope="module")
def cleanup_redis():
    # Do not cleanup database until everyone is done using it.
    yield
    redis.Redis.from_url(_BROKER_URL).flushdb()


@pytest.fixture()
def global_config(dataspace, cleanup_redis):  # noqa: F811
    conf = ValidConfig(policies.global_config_file(_CONFIG_PATH))
    conf["dataspace"] = dataspace.config["dataspace"]
    yield conf


def test_taskmanager_init(global_config):
    task_manager = task_manager_for(global_config, "test_channel")
    assert task_manager.state.has_value(State.BOOT)


def test_taskmanager_channel_name_in_config(global_config):
    task_manager = task_manager_for(global_config, "test_channel2")
    assert task_manager.name == "name_in_config"


def test_shutdown_method_called(global_config, caplog):
    with RunChannel(global_config, "test_channel") as task_manager:
        task_manager.take_offline()
        task_manager.state.wait_while(State.SHUTTINGDOWN)
    assert task_manager.state.has_value(State.OFFLINE)

    logfile_basename = task_manager.name + ".log"
    logfile = os.path.join(os.path.dirname(global_config["logger"]["log_file"]), logfile_basename)
    shutdown_called = False
    with open(logfile) as f:
        for line in f.readlines():
            if "Will call shutdown on all publishers" in line:
                shutdown_called = True
                break
    assert shutdown_called


def test_take_task_manager_offline(global_config):
    with RunChannel(global_config, "test_channel") as task_manager:
        task_manager.take_offline()
    assert task_manager.state.has_value(State.OFFLINE)
    assert task_manager.get_state_value() == State.OFFLINE.value


def test_erring_publisher(global_config):
    with RunChannel(global_config, "erring_publisher") as task_manager:
        task_manager.state.wait_while(State.ACTIVE)  # While launching sources
        task_manager.state.wait_while(State.SHUTTINGDOWN)  # Never gets into steady state due to producer failure
    assert task_manager.state.has_value(State.OFFLINE)


def test_bad_datablock(global_config, dataspace, caplog):  # noqa: F811
    with RunChannel(global_config, "test_channel") as task_manager:
        task_manager.state.wait_while(State.ACTIVE)
        dblock = datablock.DataBlock(dataspace, task_manager.name)
        task_manager.data_block_put("bad_string", "header", dblock)
        task_manager.take_offline()
        assert "data_block put expecting" in caplog.text


def test_no_data_to_transform(global_config):
    with RunChannel(global_config, "test_channel") as task_manager:
        task_manager.run_transforms()
        with pytest.raises(RuntimeError, match="Cannot run logic engine on data block that is 'None'."):
            task_manager.run_logic_engine(None)
        task_manager.take_offline()


def test_run_source_only_once(global_config):
    with RunChannel(global_config, "run_source_once") as task_manager:
        task_manager.take_offline()


def test_multiple_logic_engines_not_supported(global_config):
    with pytest.raises(RuntimeError, match="Cannot support more than one logic engine per channel."):
        task_manager_for(global_config, "multiple_logic_engines")
