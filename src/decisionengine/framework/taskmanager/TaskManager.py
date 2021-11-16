"""
Task manager
"""
import importlib
import multiprocessing
import socket
import time
import uuid

import structlog

from kombu import Connection, Exchange, Queue
from kombu.pools import connections, producers

from decisionengine.framework.dataspace import datablock, dataspace
from decisionengine.framework.logicengine.LogicEngine import LogicEngine, passthrough_configuration
from decisionengine.framework.managers.ComponentManager import ComponentManager
from decisionengine.framework.modules import Module
from decisionengine.framework.modules.logging_configDict import CHANNELLOGGERNAME, DELOGGER_CHANNEL_NAME, LOGGERNAME
from decisionengine.framework.modules.Publisher import Publisher
from decisionengine.framework.modules.Source import Source
from decisionengine.framework.modules.Transform import Transform
from decisionengine.framework.taskmanager.module_graph import ensure_no_circularities
from decisionengine.framework.taskmanager.ProcessingState import State
from decisionengine.framework.util.metrics import Gauge, Histogram
from decisionengine.framework.util.subclasses import all_subclasses

_DEFAULT_SCHEDULE = 300  # 5 minutes

# Metrics for monitoring TaskManager
CHANNEL_STATE_GAUGE = Gauge(
    "de_channel_state",
    "Channel state",
    [
        "channel_name",
    ],
)

SOURCE_ACQUIRE_GAUGE = Gauge(
    "de_source_last_acquire_timestamp_seconds",
    "Last time a source successfully ran its acquire function",
    [
        "channel_name",
        "source_name",
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

SOURCE_RUN_HISTOGRAM = Histogram(
    "de_source_run_seconds",
    "Time spent running source",
    [
        "channel_name",
        "source_name",
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

delogger = structlog.getLogger(LOGGERNAME)
delogger = delogger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


def _find_only_one_subclass(module, base_class):
    """
    Search through module looking for only one subclass of the supplied base_class
    """
    subclasses = all_subclasses(module, base_class)
    if not subclasses:
        raise RuntimeError(
            f"Could not find a decision-engine '{base_class.__name__}' in the module '{module.__name__}'"
        )
    if len(subclasses) > 1:
        error_msg = (
            f"Found more than one decision-engine '{base_class.__name__}' in the module '{module.__name__}':\n\n"
        )
        for cls in subclasses:
            error_msg += " - " + cls + "\n"
        error_msg += "\nSpecify which subclass you want via the configuration 'name: <one of the above>'."
        raise RuntimeError(error_msg)
    return subclasses[0]


def _create_module_instance(config_dict, base_class, channel_name):
    """
    Create instance of dynamically loaded module
    """
    my_module = importlib.import_module(config_dict["module"])
    class_name = config_dict.get("name")
    if class_name is None:
        if base_class == LogicEngine:
            # Icky kludge until we remove explicit LogicEngine 'module' specification
            class_name = "LogicEngine"
        else:
            class_name = _find_only_one_subclass(my_module, base_class)

    delogger.debug(f"in TaskManager, importlib has imported module {class_name}")
    class_type = getattr(my_module, class_name)
    return class_type(dict(**config_dict["parameters"], channel_name=channel_name))


class Worker:
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, key, conf_dict, base_class, channel_name):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """
        self.module_instance = _create_module_instance(conf_dict, base_class, channel_name)
        self.module = conf_dict["module"]
        self.module_key = key
        self.full_key = f"{channel_name}.{self.module_key}"
        self.name = self.module_instance.__class__.__name__
        self.schedule = conf_dict.get("schedule", _DEFAULT_SCHEDULE)

        # NOTE: THIS MUST BE LOGGED TO de logger, because channel logger does not exist yet
        delogger.debug(
            f"Creating worker: module={self.module} name={self.name} parameters={conf_dict['parameters']} schedule={self.schedule}"
        )


def _make_workers_for(configs, base_class, channel_name):
    return {key: Worker(key, e, base_class, channel_name) for key, e in configs.items()}


class TaskManager(ComponentManager):
    """
    Task manager
    """

    def __init__(self, name, channel_dict, global_config, de_source_workers=None):
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
        super().__init__(channel_dict.get("channel_name", name))

        self.id = str(uuid.uuid4()).upper()
        self.dataspace = dataspace.DataSpace(global_config)
        self.data_block_t0 = datablock.DataBlock(self.dataspace, name, self.id, 1)  # my current data block
        self.logger = structlog.getLogger(CHANNELLOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=self.name)

        self.broker_url = global_config.get("broker_url", "redis://localhost:6379/0")
        self.logger.debug(f"Using data-broker URL: {self.broker_url}")

        self.logger.debug("Creating channel sources")
        self.source_workers = _make_workers_for(channel_dict["sources"], Source, self.name)
        if de_source_workers is not None:
            # Decision engine owns the sources
            de_source_workers[self.name] = self.source_workers

        self.logger.debug("Creating channel publishers")
        self.publisher_workers = _make_workers_for(channel_dict["publishers"], Publisher, self.name)

        self.logger.debug("Creating channel logic engines")
        configured_le_s = channel_dict.get("logicengines")
        if configured_le_s is None:
            self.logger.debug(
                "No 'logicengines' configuration detected; will use default configuration, which unconditionally executes all configured publishers."
            )
            configured_le_s = passthrough_configuration(channel_dict["publishers"].keys())
        if len(configured_le_s) > 1:
            raise RuntimeError("Cannot support more than one logic engine per channel.")

        self.logic_engine = None
        if configured_le_s:
            key, config = configured_le_s.popitem()
            self.logic_engine = Worker(key, config, LogicEngine, self.name)

        self.logger.debug("Creating channel transforms")
        transform_workers = _make_workers_for(channel_dict["transforms"], Transform, self.name)
        self.transform_workers = ensure_no_circularities(self.source_workers, transform_workers, self.publisher_workers)

        exchange_name = global_config.get("exchange_name", "hepcloud_topic_exchange")
        self.logger.debug(f"Creating topic exchange {exchange_name} for channel {self.name}")
        self.exchange = Exchange(exchange_name, "topic")
        self.connection = Connection(self.broker_url)

        expected_source_products = set()
        queues = {}
        for worker in self.source_workers.values():
            # FIXME: Just keeping track of instance names will not
            #        work whenever we have multiple source instances
            #        of the same source type.
            expected_source_products.update(worker.module_instance._produces.keys())
            self.logger.debug(f"Creating queue {worker.full_key} with routing key {worker.full_key}")
            queues[worker.full_key] = Queue(
                worker.full_key,
                exchange=self.exchange,
                routing_key=worker.full_key,
                auto_delete=True,
            )
        self.expected_source_products = expected_source_products
        self.queues = queues

        # Caching to determine if all sources have run at least once.
        self.sources_have_run_once = False
        self.source_product_cache = {}

        # The rest of this function will go away once the source-proxy
        # has been reimplemented.
        for src_worker in self.source_workers.values():
            src_worker.module_instance.post_create(global_config)

    def run(self):
        """
        Task manager main loop
        """
        self.logger.setLevel(self.loglevel.value)
        self.logger.info(f"Starting task manager {self.id}")
        self.logger.debug(f"Expected source products {self.expected_source_products}")
        source_threads = self.start_sources()
        self.start_cycles()

        for thread in source_threads:
            thread.join()

    def start_cycles(self):
        """
        Start decision cycles
        """
        _cl = Connection(self.broker_url)
        with connections[_cl].acquire(block=True) as conn:

            def run_cycle(body, message):
                module_spec = body["source_module"]
                module_name = body["class_name"]
                data = body["data"]
                assert data
                self.logger.debug(f"Data received from {module_name}: {data}")

                if not self.sources_have_run_once:
                    self.source_product_cache.update(**data)
                    missing_products = self.expected_source_products - set(self.source_product_cache.keys())
                    if missing_products:
                        self.logger.info(f"Waiting on more data (missing {missing_products})")
                        message.ack()
                        return
                    self.logger.info("All sources have executed at least once")
                    data = self.source_product_cache
                    self.sources_have_run_once = True

                header = datablock.Header(
                    self.data_block_t0.taskmanager_id, create_time=time.time(), creator=module_spec
                )
                self.logger.info(f"Source {module_name} header done")

                try:
                    self.data_block_put(data, header, self.data_block_t0)
                except Exception:  # pragma: no cover
                    self.logger.exception("Exception inserting data into the data block.")
                    self.logger.error(f"Could not insert data from the following message\n{body}")
                    message.ack()
                    return

                self.logger.info(f"Source {module_name} data block put done")

                try:
                    self.decision_cycle()
                    with self.state.lock:
                        if not self.state.should_stop():
                            # If we are signaled to stop, don't override that state
                            # otherwise the last decision_cycle completed without error
                            self.state.set(State.STEADY)
                            CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())
                except Exception:  # pragma: no cover
                    self.logger.exception("Exception in the task manager main loop")
                    self.logger.error(
                        "Error occured. Task manager %s exits with state %s", self.id, self.get_state_name()
                    )
                message.ack()

            with conn.Consumer(self.queues.values(), accept=["pickle"], callbacks=[run_cycle]):
                self.logger.debug(f"Channel {self.name} is listening for events")
                while not self.state.should_stop():
                    try:
                        # If source has been brought offline while the drain_events method is
                        # executing, it will stall.  We therefore impose an arbitrary 5-second
                        # timeout so that the 'should_stop()' method called in the while condition
                        # will yield false and thus terminate the loop.
                        conn.drain_events(timeout=5)
                    except TimeoutError:  # pragma: no cover
                        # no events found in time
                        pass
                    except socket.timeout:  # pragma: no cover
                        # no events found in time
                        pass
                self.logger.info(f"Task manager {self.id} received stop signal and is exiting")

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

    def set_to_shutdown(self):
        self.state.set(State.SHUTTINGDOWN)
        CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())
        self.logger.debug("Shutting down. Will call shutdown on all publishers")
        for worker in self.publisher_workers.values():
            worker.module_instance.shutdown()
        self.state.set(State.SHUTDOWN)
        CHANNEL_STATE_GAUGE.labels(self.name).set(self.get_state_value())

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
            # This is too long to find, so im leaving it here to make it obvious whats going on
            #   you'll want to update it eventually.
            # metadata = datablock.Metadata(data_block.component_manager_id,
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

    def run_source(self, worker):
        """
        Get the data from source
        and put it into the data block

        :type worker: :obj:`~Worker`
        :arg worker: Source worker
        """
        with producers[self.connection].acquire(block=True) as producer:
            # If task manager is in offline state, do not keep executing sources.
            while not self.state.should_stop():
                try:
                    self.logger.info(f"Source {worker.name} calling acquire")
                    data = worker.module_instance.acquire()
                    Module.verify_products(worker.module_instance, data)
                    self.logger.info(f"Source {worker.name} acquire returned")
                    SOURCE_ACQUIRE_GAUGE.labels(self.name, worker.name).set_to_current_time()
                    self.logger.debug(f"Publishing data to queue {worker.full_key} with routing key {worker.full_key}")
                    producer.publish(
                        dict(source_module=worker.module, class_name=worker.name, data=data),
                        routing_key=worker.full_key,
                        exchange=self.exchange,
                        serializer="pickle",
                        declare=[
                            self.exchange,
                            self.queues[worker.full_key],
                        ],
                    )
                    self.logger.info(f"Source {worker.name} {worker.module} finished cycle")
                except Exception:
                    self.logger.exception(f"Exception running source {worker.name} ")
                    self.take_offline()
                    break
                if worker.schedule > 0:
                    time.sleep(worker.schedule)
                else:
                    self.logger.info(f"Source {worker.name} runs only once")
                    break
        self.logger.info(f"Stopped {worker.name}")

    def start_sources(self):
        """
        Start sources, each in a separate thread
        """
        source_threads = []

        for key, source in self.source_workers.items():
            self.logger.info(f"starting loop for {source.name}->{key}")
            SOURCE_ACQUIRE_GAUGE.labels(self.name, source.name)
            thread = multiprocessing.Process(target=self.run_source, name=source.name, args=(source,))
            source_threads.append(thread)
            thread.start()

        return source_threads

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
                            worker.module_instance.publish(data_block)
                            PUBLISHER_RUN_GAUGE.labels(self.name, name).set_to_current_time()
                    except KeyError as e:
                        if self.state.should_stop():
                            self.logger.warning(f"TaskManager stopping, ignore exception {name} publish() call: {e}")
                            continue
                        raise  # pragma: no cover
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise
