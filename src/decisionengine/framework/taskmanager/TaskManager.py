"""
Task Manager
"""
import importlib
import threading
import logging
import structlog
import time
import multiprocessing
import uuid

import pandas

from decisionengine.framework.dataspace import dataspace
from decisionengine.framework.dataspace import datablock
from decisionengine.framework.modules import Module
from decisionengine.framework.modules.Publisher import Publisher
from decisionengine.framework.modules.Source import Source
from decisionengine.framework.modules.Transform import Transform
from decisionengine.framework.logicengine.LogicEngine import LogicEngine
from decisionengine.framework.taskmanager.ProcessingState import State
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState
from decisionengine.framework.taskmanager.module_graph import ensure_no_circularities
from decisionengine.framework.util.subclasses import all_subclasses
from decisionengine.framework.modules.de_logger import LOGGERNAME


_TRANSFORMS_TO = 300  # 5 minutes
_DEFAULT_SCHEDULE = 300  # ""

delogger = structlog.getLogger(LOGGERNAME)
delogger = delogger.bind(module=__name__.split(".")[-1])


def _find_only_one_subclass(module, base_class):
    """
    Search through module looking for only one subclass of the supplied base_class
    """
    subclasses = all_subclasses(module, base_class)
    if not subclasses:
        raise RuntimeError(
            f"Could not find a decision-engine '{base_class.__name__}' in the module:\n"
            f"  '{module.__name__}'")
    if len(subclasses) > 1:
        error_msg = (
            f"Found more than one decision-engine '{base_class.__name__}' in the module\n"
            + f"'{module.__name__}':\n\n")
        for cls in subclasses:
            error_msg += " - " + cls + "\n"
        error_msg += "\nSpecify which subclass you want via the configuration 'name: <one of the above>'."
        raise RuntimeError(error_msg)
    return subclasses[0]


def _create_module_instance(config_dict, base_class):
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

    class_type = getattr(my_module, class_name)
    return class_type(config_dict["parameters"])


class Worker:
    """
    Provides interface to loadable modules an events to sycronise
    execution
    """

    def __init__(self, conf_dict, base_class):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the worker
        """
        self.worker = _create_module_instance(conf_dict, base_class)
        self.module = conf_dict["module"]
        self.name = self.worker.__class__.__name__
        self.schedule = conf_dict.get("schedule", _DEFAULT_SCHEDULE)
        self.data_updated = threading.Event()
        self.stop_running = threading.Event()

        # NOTE: THIS MUST BE LOGGED TO de logger, because channel logger does not exist yet
        delogger.debug(
            f"Creating worker: module={self.module} name={self.name} parameters={conf_dict['parameters']} schedule={self.schedule}"
        )


def _make_workers_for(configs, base_class):
    return {name: Worker(e, base_class) for name, e in configs.items()}


class Channel:
    """
    Decision Channel.
    Instantiates workers according to channel configuration
    """

    def __init__(self, channel_dict):
        """
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        """

        delogger.debug("Creating channel source")
        self.sources = _make_workers_for(channel_dict["sources"], Source)
        delogger.debug("Creating channel logicengine")
        self.le_s = _make_workers_for(channel_dict["logicengines"],
                                      LogicEngine)
        delogger.debug("Creating channel publisher")
        self.publishers = _make_workers_for(channel_dict["publishers"],
                                            Publisher)

        delogger.debug("Creating channel transform")
        transforms = _make_workers_for(channel_dict["transforms"], Transform)
        self.transforms = ensure_no_circularities(self.sources, transforms,
                                                  self.publishers)
        self.task_manager = channel_dict.get("task_manager", {})


class TaskManager:
    """
    Task Manager
    """

    def __init__(self, name, generation_id, channel_dict, global_config):
        """
        :type name: :obj:`str`
        :arg name: Name of channel corresponding to this task manager
        :type generation_id: :obj:`int`
        :arg generation_id: Task Manager generation id provided by caller
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        :type global_config: :obj:`dict`
        :arg global_config: global configuration
        """
        self.id = str(uuid.uuid4()).upper()
        self.dataspace = dataspace.DataSpace(global_config)
        self.data_block_t0 = datablock.DataBlock(
            self.dataspace, name, self.id,
            generation_id)  # my current data block
        self.name = name
        self.logger = structlog.getLogger(f"{self.name}")
        self.logger = self.logger.bind(module=__name__.split(".")[-1])
        self.channel = Channel(channel_dict)
        self.state = ProcessingState()
        self.loglevel = multiprocessing.Value("i", logging.WARNING)
        self.lock = threading.Lock()

        # The rest of this function will go away once the source-proxy
        # has been reimplemented.
        for src_worker in self.channel.sources.values():
            src_worker.worker.post_create(global_config)

    def wait_for_all(self, events_done):
        """
        Wait for all sources or transforms to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        self.logger.info("Waiting for all tasks to run")

        try:
            while not all([e.is_set() for e in events_done]):
                time.sleep(1)
                if self.state.should_stop():
                    break

            for e in events_done:
                e.clear()
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise

    def wait_for_any(self, events_done):
        """
        Wait for any sources to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        try:
            while not any([e.is_set() for e in events_done]):
                time.sleep(1)
                if self.state.should_stop():
                    break

            for e in events_done:
                if e.is_set():
                    e.clear()
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise

    def run(self):
        """
        Task Manager main loop
        """
        self.logger.setLevel(self.loglevel.value)
        self.logger.info(f"Starting Task Manager {self.id}")
        done_events, source_threads = self.start_sources(self.data_block_t0)
        # This is a boot phase
        # Wait until all sources run at least one time
        self.wait_for_all(done_events)
        self.logger.info("All sources finished")
        if not self.state.has_value(State.BOOT):
            for thread in source_threads:
                thread.join()
            self.logger.error(
                f"Error occured during initial run of sources. Task Manager {self.name} exits"
            )
            return

        while not self.state.should_stop():
            try:
                self.decision_cycle()
                with self.state.lock:
                    if not self.state.should_stop():
                        # If we are signaled to stop, don't override that state
                        # otherwise the last decision_cycle completed without error
                        self.state.set(State.STEADY)
                if not self.state.should_stop():
                    # the last decision_cycle completed without error
                    self.state.set(State.STEADY)
                    self.wait_for_any(done_events)
            except Exception:  # pragma: no cover
                self.logger.exception(
                    "Exception in the task manager main loop")
                self.logger.error(
                    "Error occured. Task Manager %s exits with state %s",
                    self.id, self.get_state_name())
                break

        else:
            # we did not use 'break' to exit the loop
            self.logger.info(
                f"Task Manager {self.id} received stop signal and exits")

        for source in self.channel.sources.values():
            source.stop_running.set()

        for thread in source_threads:
            thread.join()

    def get_state(self):
        return self.state.get()

    def get_state_value(self):
        return self.get_state().value

    def get_state_name(self):
        return self.get_state().name

    def get_produces(self):
        # FIXME: What happens if a transform and source have the same name?
        produces = {}
        for name, mod in self.channel.sources.items():
            produces[name] = list(mod.worker._produces.keys())
        for name, mod in self.channel.transforms.items():
            produces[name] = list(mod.worker._produces.keys())
        return produces

    def get_consumes(self):
        # FIXME: What happens if a transform and publisher have the same name?
        consumes = {}
        for name, mod in self.channel.transforms.items():
            consumes[name] = list(mod.worker._consumes.keys())
        for name, mod in self.channel.publishers.items():
            consumes[name] = list(mod.worker._consumes.keys())
        return consumes

    def set_loglevel_value(self, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.loglevel.get_lock():
            # Convert from string to int form using technique
            # suggested by logging module
            self.loglevel.value = getattr(logging, log_level)

    def get_loglevel(self):
        with self.loglevel.get_lock():
            return self.loglevel.value

    def set_to_shutdown(self):
        self.state.set(State.SHUTTINGDOWN)
        delogger.debug("Shutting down. Will call shutdown on all publishers")
        for publisher_worker in self.channel.publishers.values():
            publisher_worker.worker.shutdown()
        self.state.set(State.SHUTDOWN)

    def take_offline(self, current_data_block):
        """
        offline and stop task manager
        """
        self.state.set(State.OFFLINE)
        # invalidate data block
        # not implemented yet

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
            self.logger.error(
                f"data_block put expecting {dict} type, got {type(data)}")
            return
        self.logger.debug(f"data_block_put {data}")
        with data_block.lock:
            metadata = datablock.Metadata(
                data_block.taskmanager_id,
                state="END_CYCLE",
                generation_id=data_block.generation_id)
            for key, product in data.items():
                data_block.put(key, product, header, metadata=metadata)

    def do_backup(self):
        """
        Duplicate current data block and return its copy

        :rtype: :obj:`~datablock.DataBlock`

        """

        with self.lock:
            data_block = self.data_block_t0.duplicate()
            self.logger.debug(f"Duplicated block {data_block}")
        return data_block

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.do_backup()
        try:
            self.run_transforms(data_block_t1)
        except Exception:  # pragma: no cover
            self.logger.exception("Error in decision cycle(transforms) ")
            # We do not call 'take_offline' here because it has
            # already been called in the run_transform code on
            # operating on a separate thread.

        actions_facts = []
        try:
            actions_facts = self.run_logic_engine(data_block_t1)
            self.logger.info("ran all logic engines")
        except Exception:  # pragma: no cover
            self.logger.exception("Error in decision cycle(logic engine) ")
            self.take_offline(data_block_t1)

        for a_f in actions_facts:
            try:
                self.run_publishers(a_f["actions"], a_f["newfacts"],
                                    data_block_t1)
            except Exception:  # pragma: no cover
                self.logger.exception("Error in decision cycle(publishers) ")
                self.take_offline(data_block_t1)

    def run_source(self, src):
        """
        Get the data from source
        and put it into the data block

        :type src: :obj:`~Worker`
        :arg src: source Worker
        """

        # If task manager is in offline state, do not keep executing sources.
        while not self.state.should_stop():
            try:
                self.logger.info(f"Src {src.name} calling acquire")
                data = src.worker.acquire()
                Module.verify_products(src.worker, data)
                self.logger.info(f"Src {src.name} acquire returned")
                self.logger.info(f"Src {src.name} filling header")
                if data:
                    t = time.time()
                    header = datablock.Header(
                        self.data_block_t0.taskmanager_id,
                        create_time=t,
                        creator=src.module)
                    self.logger.info(f"Src {src.name} header done")
                    self.data_block_put(data, header, self.data_block_t0)
                    self.logger.info(f"Src {src.name} data block put done")
                else:
                    self.logger.warning(
                        f"Src {src.name} acquire retuned no data")
                src.data_updated.set()
                self.logger.info(f"Src {src.name} {src.module} finished cycle")
            except Exception:
                self.logger.exception(f"Exception running source {src.name} ")
                self.take_offline(self.data_block_t0)
                break
            if src.schedule > 0:
                s = src.stop_running.wait(src.schedule)
                if s:
                    self.logger.info(
                        f"received stop_running signal for {src.name}")
                    break
            else:
                self.logger.info(f"source {src.name} runs only once")
                break
        self.logger.info(f"stopped {src.name}")

    def start_sources(self, data_block=None):
        """
        Start sources, each in a separate thread

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """

        event_list = []
        source_threads = []

        for key, source in self.channel.sources.items():
            self.logger.info(f"starting loop for {key}")
            event_list.append(source.data_updated)
            thread = threading.Thread(target=self.run_source,
                                      name=source.name,
                                      args=(source, ))
            source_threads.append(thread)
            # Cannot catch exception from function called in separate thread
            thread.start()
        return (event_list, source_threads)

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

        for key, transform in self.channel.transforms.items():
            self.logger.info(f"starting transform {key}")
            self.run_transform(transform, data_block)
        self.logger.info("all transforms finished")

    def run_transform(self, transform, data_block):
        """
        Run a transform

        :type transform: :obj:`~Worker`
        :arg transform: source Worker
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        consume_keys = list(transform.worker._consumes.keys())

        self.logger.info("transform: %s expected keys: %s provided keys: %s",
                         transform.name, consume_keys, list(data_block.keys()))
        self.logger.info("run transform %s", transform.name)
        try:
            data = transform.worker.transform(data_block)
            self.logger.debug(f"transform returned {data}")
            t = time.time()
            header = datablock.Header(data_block.taskmanager_id,
                                      create_time=time.time(),
                                      creator=transform.name)
            self.data_block_put(data, header, data_block)
            self.logger.info("transform put data")
        except Exception:  # pragma: no cover
            self.logger.exception(
                f"exception from transform {transform.name} ")
            self.take_offline(data_block)

    def run_logic_engine(self, data_block=None):
        """
        Run Logic Engine.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        le_list = []
        if not data_block:
            return

        try:
            for le in self.channel.le_s:
                self.logger.info("run logic engine %s",
                                 self.channel.le_s[le].name)
                self.logger.debug("run logic engine %s %s",
                                  self.channel.le_s[le].name, data_block)
                rc = self.channel.le_s[le].worker.evaluate(data_block)
                le_list.append(rc)
                self.logger.info("run logic engine %s done",
                                 self.channel.le_s[le].name)
                self.logger.info(
                    "logic engine %s generated newfacts: %s",
                    self.channel.le_s[le].name,
                    rc["newfacts"].to_dict(orient="records"),
                )
                self.logger.info("logic engine %s generated actions: %s",
                                 self.channel.le_s[le].name, rc["actions"])

            # Add new facts to the datablock
            # Add empty dataframe if nothing is available
            if le_list:
                all_facts = pandas.concat([i["newfacts"] for i in le_list],
                                          ignore_index=True)
            else:
                self.logger.info(
                    "Logic engine(s) did not return any new facts")
                all_facts = pandas.DataFrame()

            data = {"de_logicengine_facts": all_facts}
            t = time.time()
            header = datablock.Header(data_block.taskmanager_id,
                                      create_time=t,
                                      creator="logicengine")
            self.data_block_put(data, header, data_block)
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise
        else:
            return le_list

    def run_publishers(self, actions, facts, data_block=None):
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
                    publisher = self.channel.publishers[action]
                    name = publisher.name
                    self.logger.info(f"run publisher {name}")
                    self.logger.debug(f"run publisher {name} {data_block}")

                    try:
                        publisher.worker.publish(data_block)
                    except KeyError as e:
                        if self.state.should_stop():
                            self.logger.warning(
                                f"TaskManager stopping, ignore exception {name} publish() call: {e}"
                            )
                            continue
                        else:
                            raise
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise
