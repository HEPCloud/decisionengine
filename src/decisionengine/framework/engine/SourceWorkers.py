# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import multiprocessing
import pickle
import threading
import time
import uuid

import structlog

from kombu import Connection, Queue
from kombu.pools import producers

from decisionengine.framework.modules import Module
from decisionengine.framework.modules.logging_configDict import LOGGERNAME
from decisionengine.framework.modules.Source import Source
from decisionengine.framework.taskmanager.module_graph import _create_module_instance
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState, State
from decisionengine.framework.util.countdown import Countdown
from decisionengine.framework.util.metrics import Gauge

_DEFAULT_SCHEDULE = 300  # 5 minutes

SOURCE_ACQUIRE_GAUGE = Gauge(
    "de_source_last_acquire_timestamp_seconds",
    "Last time a source successfully ran its acquire function",
    [
        "source_name",
    ],
)


class SourceWorker(multiprocessing.Process):
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, key, config, channel_name, exchange, broker_url):
        """
        :type config: :obj:`dict`
        :arg config: configuration dictionary describing the worker
        """
        super().__init__(name=f"SourceWorker-{key}")
        self.module_instance = _create_module_instance(config, Source, channel_name)
        self.config = config
        self.module = self.config["module"]
        self.key = key
        self.class_name = self.module_instance.__class__.__name__
        SOURCE_ACQUIRE_GAUGE.labels(self.key)

        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], source=self.key)

        self.exchange = exchange
        self.connection = Connection(broker_url)

        # We use a random name to avoid queue collisions when running tests
        queue_id = self.key + "-" + str(uuid.uuid4()).upper()
        self.logger.debug(f"Creating queue {queue_id} with routing key {self.key}")
        self.queue = Queue(
            queue_id,
            exchange=self.exchange,
            routing_key=self.key,
            auto_delete=True,
        )
        self.state = ProcessingState()
        self.schedule = config.get("schedule", _DEFAULT_SCHEDULE)

        self.logger.debug(
            f"Creating worker: module={self.module} name={self.key} class_name={self.class_name} parameters={config['parameters']} schedule={self.schedule}"
        )

    def take_offline(self):
        if self.state.has_value(State.ERROR):
            return
        self.state.set(State.OFFLINE)

    def run(self):
        """
        Get the data from source
        """
        self.logger.info(f"Starting source loop for {self.key}")
        SOURCE_ACQUIRE_GAUGE.labels(self.key)
        with producers[self.connection].acquire(block=True) as producer:
            # If task manager is in offline state, do not keep executing sources.
            while not self.state.should_stop():
                try:
                    self.logger.info(f"Source {self.key} calling acquire")
                    data = self.module_instance.acquire()
                    Module.verify_products(self.module_instance, data)
                    self.logger.info(f"Source {self.key} acquire returned")
                    SOURCE_ACQUIRE_GAUGE.labels(self.key).set_to_current_time()
                    self.logger.debug(
                        f"Publishing data to queue {self.queue.name} with routing key {self.key}"
                        + f" ({len(pickle.dumps(data))} pickled bytes)"
                    )
                    producer.publish(
                        dict(source_name=self.key, source_module=self.module, data=data),
                        routing_key=self.key,
                        exchange=self.exchange,
                        serializer="pickle",
                        declare=[
                            self.exchange,
                            self.queue,
                        ],
                    )
                    self.logger.info(f"Source {self.key} finished cycle")
                    if not self.state.should_stop() and not self.state.has_value(State.STEADY):
                        self.state.set(State.STEADY)
                except Exception:
                    self.logger.exception(f"Exception running source {self.key} ")
                    self.logger.debug(f"Sending shutdown flag to queue {self.queue.name}")
                    self.state.set(State.ERROR)
                    producer.publish(
                        dict(source_name=self.key, source_module=self.module, data=State.SHUTDOWN),
                        routing_key=self.key,
                        exchange=self.exchange,
                        serializer="pickle",
                        declare=[
                            self.exchange,
                            self.queue,
                        ],
                    )
                    break
                if self.schedule > 0:
                    time.sleep(self.schedule)
                else:
                    self.logger.info(f"Source {self.key} runs only once")
                    break

        self.logger.info(f"Stopped source {self.key} in {self.state.get().name} state")


class SourceWorkers:
    def __init__(self, exchange, broker_url, logger=structlog.getLogger(LOGGERNAME)):
        self._exchange = exchange
        self._broker_url = broker_url
        self._logger = logger
        self._workers = {}
        self._use_count = {}
        self._lock = threading.Lock()

    def unguarded_access(self):
        return self._workers

    def update(self, channel_name, source_configs):
        workers = {}

        # Reuse already existing sources
        with self._lock:
            existing_sources = set(self._workers.keys()).intersection(source_configs.keys())
            for src_name in existing_sources:
                new_src_config = source_configs.pop(src_name)
                src_worker = self._workers[src_name]
                if new_src_config != src_worker.config:
                    err_msg = (
                        f"Channel {channel_name} will not be loaded due to the following error:\n"
                        f"Mismatched configurations for source with name {src_name}\n"
                        f"New configuration\n -> {new_src_config}\n"
                        f"Cached configuration\n -> {src_worker.config}"
                    )
                    raise RuntimeError(err_msg)
                self._logger.info(f"Using existing source {src_name} for channel {channel_name}")
                self._use_count[src_name].add(channel_name)
                workers[src_name] = src_worker

            # The remaining configuration correspond to new sources
            for key, config in source_configs.items():
                self._logger.info(f"Creating source {key} for channel {channel_name}")
                worker = SourceWorker(key, config, channel_name, self._exchange, self._broker_url)
                self._workers[key] = worker
                workers[key] = worker
                self._use_count[key] = {channel_name}

        return workers

    def unique(self, source_name):
        with self._lock:
            return len(self._use_count[source_name]) == 1

    def detach_channel(self, channel_name, source_names):
        with self._lock:
            for source_name in source_names:
                self._use_count[source_name].discard(channel_name)
                if len(self._use_count[source_name]) == 0:
                    self._logger.debug(f"Taking channel {channel_name} offline")
                    self._workers[source_name].take_offline()

    def prune(self, channel_name, source_names):
        self.detach_channel(channel_name, source_names)
        with self._lock:
            for source_name in source_names:
                src_worker = self._workers[source_name]
                if src_worker.state.should_stop():
                    self._logger.debug(f"Removing source {source_name}")
                    src_worker.join()
                    del self._workers[source_name]
                    del self._use_count[source_name]
                    self._logger.debug(f"Removed source {source_name}")

    def remove_all(self, timeout):
        with self._lock:
            countdown = Countdown(wait_up_to=timeout)
            for worker in self._workers.values():
                if not worker.is_alive():
                    continue

                with countdown:
                    worker.take_offline()
                    rc = worker.join(countdown.time_left)
                    if rc is None:
                        worker.terminate()
            self._workers.clear()
            self._use_count.clear()
