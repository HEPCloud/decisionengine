# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import contextlib
import logging
import multiprocessing
import os
import pickle
import time
import uuid

import psutil
import structlog

from kombu import Connection, Queue
from kombu.pools import producers

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.modules.logging_configDict as logconf

from decisionengine.framework.modules import Module
from decisionengine.framework.modules.Source import Source
from decisionengine.framework.taskmanager.module_graph import _create_module_instance
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState, State
from decisionengine.framework.util.countdown import Countdown
from decisionengine.framework.util.metrics import Gauge, Histogram

_DEFAULT_SCHEDULE = 300  # 5 minutes

MB = 1000000

SOURCE_STATUS = Gauge(
    "de_source_status",
    "Status of Source Data",
    [
        "source_name",
    ],
)

SOURCE_ACQUIRE_GAUGE = Gauge(
    "de_source_last_acquire_timestamp_seconds",
    "Last time a source successfully ran its acquire function",
    [
        "source_name",
    ],
)

SOURCE_ACQUIRE_HISTOGRAM = Histogram(
    "de_source_acquire_seconds",
    "How long it took to acquire the source data",
    [
        "source_name",
    ],
)


class SourceWorker(multiprocessing.Process):
    """
    Provides interface to loadable modules an events to synchronize
    execution
    """

    def __init__(self, key, config, logger_config, channel_name, exchange, broker_url):
        """
        :type config: :obj:`dict`
        :arg config: configuration dictionary describing the worker
        """
        super().__init__(name=f"SourceWorker-{key}")
        self.config = config
        self.logger_config = logger_config
        self.channel_name = channel_name
        self.module = self.config["module"]
        self.key = key
        SOURCE_ACQUIRE_GAUGE.labels(self.key)

        self.loglevel = multiprocessing.Value("i", logging.WARNING)
        self.logger = structlog.getLogger(logconf.SOURCELOGGERNAME)
        self.logger.setLevel(logging.DEBUG)

        self.module_instance = _create_module_instance(config, Source, channel_name)
        self.class_name = self.module_instance.__class__.__name__

        logger = structlog.getLogger(logconf.LOGGERNAME)
        logger = logger.bind(module=__name__.split(".")[-1], source=self.key)

        self.exchange = exchange
        self.connection = Connection(broker_url)
        self.connection_channel = self.connection.channel()

        # We use a random name to avoid queue collisions when running tests
        queue_id = self.key + "." + str(uuid.uuid4()).upper()
        logger.debug(f"Creating queue {queue_id} with routing key {self.key}")
        self.queue = Queue(
            queue_id,
            exchange=self.exchange,
            routing_key=self.key,
            channel=self.connection_channel,
            auto_delete=True,
        )
        self.state = ProcessingState()
        self.schedule = config.get("schedule", _DEFAULT_SCHEDULE)

        logger.debug(
            f"Creating worker: module={self.module} name={self.key} class_name={self.class_name} parameters={config['parameters']} schedule={self.schedule}"
        )

    def get_loglevel(self):
        with self.loglevel.get_lock():
            return self.loglevel.value

    def set_loglevel_value(self, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.loglevel.get_lock():
            # Convert from string to int form using technique
            # suggested by logging module
            self.loglevel.value = getattr(logging, log_level)
            self.logger.setLevel(self.loglevel.value)

    # setup the Source specific loggers
    def setup_logger(self):
        myname = self.key
        myfilename = os.path.join(os.path.dirname(self.logger_config["log_file"]), myname + ".log")
        start_q_logger = self.logger_config.get("start_q_logger", "True")

        # self.logger = structlog.getLogger(logconf.SOURCELOGGERNAME)
        # setting a default value here. value from config file is set in call
        # self.worker.set_loglevel_value after logger configuration is completed
        # self.logger.setLevel(logging.DEBUG)

        logger_rotate_by = self.logger_config.get("file_rotate_by", "size")
        if logger_rotate_by == "size":
            handler = logging.handlers.RotatingFileHandler(
                filename=myfilename,
                maxBytes=self.logger_config.get("max_file_size", 200 * MB),
                backupCount=self.logger_config.get("max_backup_count", 6),
            )

        elif logger_rotate_by == "time":
            handler = logging.handlers.TimedRotatingFileHandler(
                filename=myfilename,
                when=self.logger_config.get("rotation_time_unit", "D"),
                interval=self.logger_config.get("rotation_time_interval", 1),
                backupCount=self.logger_config.get("max_backup_count", 6),
            )
        else:
            raise ValueError(f"In SourceWorkers, incorrect 'logger_rotate_by':'{logger_rotate_by}:'")

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(logconf.userformat))

        self.logger.addHandler(handler)

        if start_q_logger == "True":
            self.logger.addHandler(de_logger.get_queue_logger().structlog_q_handler)

        self.logger = self.logger.bind(module=myname, channel=self.channel_name)
        self.logger.setLevel(self.logger_config.get("global_source_log_level", "WARNING"))

    def take_offline(self):
        if self.state.has_value(State.ERROR):
            return
        self.state.set(State.OFFLINE)
        SOURCE_STATUS.labels(self.key).set(State.OFFLINE.value)

    def run(self):
        """
        Get the data from source
        """
        self.state.set(State.ACTIVE)
        SOURCE_STATUS.labels(self.key).set(State.ACTIVE.value)
        self.setup_logger()
        self.logger.info(f"Starting source loop for {self.key}")
        SOURCE_ACQUIRE_GAUGE.labels(self.key)
        with producers[self.connection].acquire(block=True) as producer:
            # If task manager is in offline state, do not keep executing sources.
            while not self.state.should_stop():
                try:
                    self.logger.setLevel(self.loglevel.value)
                    self.logger.info(f"Source {self.key} calling acquire")
                    with SOURCE_ACQUIRE_HISTOGRAM.labels(self.key).time():
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
                    self.queue.purge()  # Once the message has been delivered to the broker, remove from queue.
                    self.logger.info(f"Source {self.key} finished cycle")
                    if not self.state.should_stop() and not self.state.has_value(State.STEADY):
                        self.state.set(State.STEADY)
                        SOURCE_STATUS.labels(self.key).set(State.STEADY.value)
                except Exception:
                    self.logger.exception(f"Exception running source {self.key} ")
                    self.logger.debug(f"Sending shutdown flag to queue {self.queue.name}")
                    self.state.set(State.ERROR)
                    SOURCE_STATUS.labels(self.key).set(State.ERROR.value)
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
    """
    This class manages and provides access to the Source workers.

    The intention is that the decision engine never directly interacts with the
    workers but refers to them via a context manager:

      with workers.access() as ws:
          # Access to ws now protected
          ws['new_source'] = SourceWorker(...)

    In cases where the decision engine's block_while method must be
    called (e.g. during tests), one should use unguarded access:

      ws = workers.get_unguarded()
      # Access to ws is unprotected
      ws['new_source'].wait_while(...)

    Calling a blocking method while using the protected context
    manager (i.e. workers.access()) will likely result in a deadlock.
    """

    def __init__(self, exchange, broker_url, logger=structlog.getLogger(logconf.LOGGERNAME)):
        self._exchange = exchange
        self._broker_url = broker_url
        self._logger = logger
        self._workers = {}
        self._use_count = {}
        self._lock = multiprocessing.Lock()

    class Access:
        def __init__(self, workers, lock):
            self._workers = workers
            self._lock = lock

        def __enter__(self):
            self._lock.acquire()
            return self._workers

        def __exit__(self, error, type, bt):
            self._lock.release()

    def access(self):
        return self.Access(self._workers, self._lock)

    def get_unguarded(self):
        return self._workers

    def update(self, channel_name, source_configs, logger_config):
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
                worker = SourceWorker(key, config, logger_config, channel_name, self._exchange, self._broker_url)
                self._workers[key] = worker
                workers[key] = worker
                self._use_count[key] = {channel_name}

        return workers

    def detach(self, channel_name, source_names):
        with self._lock:
            for source_name in source_names:
                self._use_count[source_name].discard(channel_name)
                if len(self._use_count[source_name]) != 0:
                    continue

                if self._workers[source_name].state.probably_running():
                    self._logger.debug(f"Taking source {source_name} offline")
                    self._workers[source_name].take_offline()

    def prune(self, channel_name, source_names):
        self.detach(channel_name, source_names)
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
                    worker.join(countdown.time_left)
                    if worker.exitcode is None:
                        # When we upgrade to Python 3.7, the following should be replaced with
                        # worker.kill()
                        with contextlib.suppress(psutil.NoSuchProcess):
                            psutil.Process(worker.pid).kill()

            self._workers.clear()
            self._use_count.clear()
