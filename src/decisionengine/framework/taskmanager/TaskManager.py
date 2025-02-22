# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Task manager
"""
import logging
import multiprocessing
import time
import uuid

import structlog

from kombu import Queue

from decisionengine.framework.dataspace import datablock
from decisionengine.framework.modules.logging_configDict import CHANNELLOGGERNAME
from decisionengine.framework.taskmanager.LatestMessages import LatestMessages
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState, State
from decisionengine.framework.taskmanager.PublisherStatus import PublisherStatusBoard
from decisionengine.framework.taskmanager.SourceProductCache import SourceProductCache
from decisionengine.framework.util.metrics import Gauge, Histogram

# Metrics for monitoring TaskManager
CHANNEL_STATE_GAUGE = Gauge(
    "de_channel_state",
    "Channel state",
    [
        "channel_name",
    ],
)

LOGICENGINE_RUN_GAUGE = Gauge(
    "de_logicengine_last_run_timestamp_seconds",
    "Last time a logicengine successfully ran",
    [
        "channel_name",
        "logicengine_name",
    ],
)

TRANSFORM_RUN_GAUGE = Gauge(
    "de_transform_last_run_timestamp_seconds",
    "Last time a transform successfully ran",
    [
        "channel_name",
        "transform_name",
    ],
)

PUBLISHER_RUN_GAUGE = Gauge(
    "de_publisher_last_run_timestamp_seconds",
    "Last time a publisher successfully ran",
    [
        "channel_name",
        "publisher_name",
    ],
)

LOGICENGINE_RUN_HISTOGRAM = Histogram(
    "de_logicengine_run_seconds",
    "Time spent running logicengine",
    [
        "channel_name",
        "logicengine_name",
    ],
)

TRANSFORM_RUN_HISTOGRAM = Histogram(
    "de_transform_run_seconds",
    "Time spent running transform",
    [
        "channel_name",
        "transform_name",
    ],
)

PUBLISHER_RUN_HISTOGRAM = Histogram(
    "de_publisher_run_seconds",
    "Time spent running publisher",
    [
        "channel_name",
        "publisher_name",
    ],
)


class TaskManager:
    """
    Task manager
    """

    def __init__(self, name, workers, dataspace, expected_products, exchange, broker_url, routing_keys):
        """
        :type name: :obj:`str`
        :arg name: Name of channel corresponding to this task manager
        :type generation_id: :obj:`int`
        :arg generation_id: Task manager generation id provided by caller
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        :type global_config: :obj:`dict`
        :arg global_config: global configuration
        """
        self.name = name
        self.state = ProcessingState()
        self.loglevel = multiprocessing.Value("i", logging.WARNING)

        self.id = str(uuid.uuid4()).upper()
        self.data_block_t0 = datablock.DataBlock(dataspace, name, self.id, 1)  # my current data block
        self.logger = structlog.getLogger(CHANNELLOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=self.name)

        # The DE owns the sources
        self.source_workers = workers["sources"]
        self.transform_workers = workers["transforms"]
        self.logic_engine = workers["logic_engine"]
        self.publisher_workers = workers["publishers"]
        self.publisher_status_board = PublisherStatusBoard(self.publisher_workers.keys())

        self.exchange = exchange
        self.broker_url = broker_url

        self.source_product_cache = SourceProductCache(expected_products, self.logger)
        self.routing_keys = routing_keys

    def get_state_value(self):
        return self.state.get_state_value()

    def get_state(self):
        return self.state.get()

    def get_state_name(self):
        return self.get_state().name

    def set_loglevel_value(self, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.loglevel.get_lock():
            # Convert from string to int form using technique
            # suggested by logging module
            self.loglevel.value = getattr(logging, log_level)

    def get_loglevel(self):
        with self.loglevel.get_lock():
            return self.loglevel.value

    def take_offline(self):
        """
        Adjust status to stop the decision cycles and bring the task manager offline
        """
        self.state.set(State.SHUTTINGDOWN)

    def run_cycle(self, messages):
        for name, msg_body in messages.items():
            source_name = msg_body["source_name"]
            module_spec = msg_body["source_module"]
            data = msg_body["data"]
            assert data
            if data is State.SHUTDOWN:
                self.logger.info(
                    f"Channel {self.name} has received shutdown flag from source {source_name} (module {module_spec})"
                )
                self.take_offline()
                return

            assert isinstance(data, dict)
            self.logger.debug(f"Data received from {source_name}: {data}")

            data_to_process = self.source_product_cache.update(data)
            if data_to_process is None:
                return

            header = datablock.Header(self.data_block_t0.taskmanager_id, create_time=time.time(), creator=module_spec)
            self.logger.info(f"Source {source_name} header done")

            try:
                self.data_block_put(data_to_process, header, self.data_block_t0)
            except Exception:  # pragma: no cover
                self.logger.exception("Exception inserting data into the data block.")
                self.logger.error(f"Could not insert data from the following message\n{msg_body}")
                self.state.set(State.ERROR)
                return

            self.logger.info(f"Source {source_name} data block put done")

        try:
            self.data_block_put(
                {"publisher_status": self.publisher_status_board.snapshot()}, header, self.data_block_t0
            )
            self.decision_cycle()
            with self.state.lock:
                if not self.state.should_stop() and not self.state.has_value(State.STEADY):
                    # If we are signaled to stop, don't override that state
                    # otherwise the last decision_cycle completed without error
                    self.state.set(State.STEADY)
                    CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())
        except Exception:  # pragma: no cover
            self.logger.exception("Exception in the task manager main loop")
            self.logger.error("Error occurred. Task manager %s exits with state %s", self.id, self.get_state_name())

    def run_cycles(self):
        """
        Task manager main loop
        """
        self.logger.setLevel(self.loglevel.value)
        self.logger.info(f"Starting task manager {self.id}")

        queues = []
        for key in self.routing_keys:
            queue_name = f"{key}.{self.name}.{self.id}"
            self.logger.debug(f"Creating queue {queue_name} with routing key {key}")
            queues.append(
                Queue(
                    queue_name,
                    exchange=self.exchange,
                    routing_key=key,
                    auto_delete=True,
                )
            )

        with LatestMessages(queues, self.broker_url) as messages:
            self.state.set(State.ACTIVE)
            self.logger.debug(f"Channel {self.name} is listening for events")
            while not self.state.should_stop():
                self.logger.setLevel(self.loglevel.value)
                msgs = messages.consume()
                if msgs:
                    self.run_cycle(msgs)
            self.logger.info(f"Task manager {self.id} received stop signal and is shutting down")

        self.state.set(State.SHUTTINGDOWN)
        CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())
        self.logger.debug("Shutting down. Will call shutdown on all publishers")
        for worker in self.publisher_workers.values():
            worker.module_instance.shutdown()
        self.state.set(State.OFFLINE)
        self.logger.info(f"Channel {self.name} is offline.")
        CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())

    def get_produces(self):
        # FIXME: What happens if a transform and source have the same name?
        produces = {}
        for name, worker in self.source_workers.items():
            produces[name] = list(worker.module_instance._produces.keys())
        for name, worker in self.transform_workers.items():
            produces[name] = list(worker.module_instance._produces.keys())
        return produces

    def get_consumes(self):
        # FIXME: What happens if a transform and publisher have the same name?
        consumes = {}
        for name, worker in self.transform_workers.items():
            consumes[name] = list(worker.module_instance._consumes.keys())
        for name, worker in self.publisher_workers.items():
            consumes[name] = list(worker.module_instance._consumes.keys())
        return consumes

    def data_block_put(self, data, header, data_block):
        """
        Put data into data block

        :type data: :obj:`dict`
        :arg data: key, value pairs
        :type header: :obj:`~datablock.Header`
        :arg header: data header
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        if not isinstance(data, dict):
            self.logger.error(f"data_block put expecting {dict} type, got {type(data)}")
            return
        self.logger.debug(f"data_block_put {data}")
        with data_block.lock:
            metadata = datablock.Metadata(
                data_block.taskmanager_id, state="END_CYCLE", generation_id=data_block.generation_id
            )
            for key, product in data.items():
                data_block.put(key, product, header, metadata=metadata)

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.data_block_t0.duplicate()
        self.logger.debug(f"Duplicated block {self.data_block_t0}")

        try:
            self.run_transforms(data_block_t1)
        except Exception:  # pragma: no cover
            self.logger.exception("Error in decision cycle(transforms) ")
            # We do not call 'take_offline' here because it has
            # already been called during run_transform.

        actions = None
        try:
            actions = self.run_logic_engine(data_block_t1)
            self.logger.info("ran all logic engines")
        except Exception:  # pragma: no cover
            self.logger.exception("Error in decision cycle(logic engine) ")
            self.take_offline()

        if actions is None:
            return

        try:
            self.run_publishers(actions, data_block_t1)
        except Exception:  # pragma: no cover
            self.logger.exception("Error in decision cycle(publishers) ")
            self.take_offline()

    def run_transforms(self, data_block=None):
        """
        Run transforms.
        So far in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        self.logger.info("run_transforms")
        self.logger.debug(f"run_transforms: data block {data_block}")
        if not data_block:
            return

        for key, worker in self.transform_workers.items():
            self.logger.info(f"starting transform {key}")
            self.run_transform(worker, data_block)
        self.logger.info("all transforms finished")

    def run_transform(self, worker, data_block):
        """
        Run a transform

        :type worker: :obj:`~Worker`
        :arg worker: Transform worker
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        consume_keys = list(worker.module_instance._consumes.keys())

        self.logger.info(
            "transform: %s expected keys: %s provided keys: %s", worker.name, consume_keys, list(data_block.keys())
        )
        self.logger.info("Run transform %s", worker.name)
        try:
            with TRANSFORM_RUN_HISTOGRAM.labels(self.name, worker.name).time():
                data = worker.module_instance.transform(data_block)
                self.logger.debug(f"transform returned {data}")
                header = datablock.Header(data_block.taskmanager_id, create_time=time.time(), creator=worker.name)
                self.data_block_put(data, header, data_block)
                self.logger.info("transform put data")
                TRANSFORM_RUN_GAUGE.labels(self.name, worker.name).set_to_current_time()
        except Exception:  # pragma: no cover
            self.logger.exception(f"exception from transform {worker.name} ")
            self.take_offline()

    def run_logic_engine(self, data_block):
        """
        Run Logic Engine.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        if not data_block:
            raise RuntimeError("Cannot run logic engine on data block that is 'None'.")

        if self.logic_engine is None:
            self.logger.info("No logic engine to run")
            return None

        try:
            actions = new_facts = None
            with LOGICENGINE_RUN_HISTOGRAM.labels(self.name, self.logic_engine.name).time():
                self.logger.info("Run logic engine %s", self.logic_engine.name)
                self.logger.debug("Run logic engine %s %s", self.logic_engine.name, data_block)
                actions, new_facts = self.logic_engine.module_instance.evaluate(data_block)
                self.logger.info("Run logic engine %s done", self.logic_engine.name)
                LOGICENGINE_RUN_GAUGE.labels(self.name, self.logic_engine.name).set_to_current_time()
                self.logger.info(
                    "Logic engine %s generated newfacts: %s",
                    self.logic_engine.name,
                    new_facts.to_dict(orient="records"),
                )
                self.logger.info("Logic engine %s generated actions: %s", self.logic_engine.name, actions)

            data = {"de_logicengine_facts": new_facts}
            header = datablock.Header(data_block.taskmanager_id, create_time=time.time(), creator="logicengine")
            self.data_block_put(data, header, data_block)
            return actions
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected logic engine error!")
            raise

    def run_publishers(self, actions, data_block):
        """
        Run Publishers in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        if not data_block:
            return
        try:
            for action_list in actions.values():
                for action in action_list:
                    worker = self.publisher_workers[action]
                    name = worker.name
                    self.logger.info(f"Run publisher {name}")
                    self.logger.debug(f"Run publisher {name} {data_block}")
                    try:
                        with PUBLISHER_RUN_HISTOGRAM.labels(self.name, name).time():
                            rc = worker.module_instance.publish(data_block)
                            if rc is False:
                                self.publisher_status_board.update(worker.module_key, rc)
                            PUBLISHER_RUN_GAUGE.labels(self.name, name).set_to_current_time()
                    except KeyError as e:
                        if self.state.should_stop():
                            self.logger.warning(f"TaskManager stopping, ignore exception {name} publish() call: {e}")
                            continue
                        raise  # pragma: no cover
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise
