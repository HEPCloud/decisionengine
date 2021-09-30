"""
Channel Manager
"""
import queue
import threading
import time

import pandas as pd
import structlog

from decisionengine.framework.dataspace import datablock
from decisionengine.framework.managers.ComponentManager import ComponentManager, create_runner
from decisionengine.framework.managers.SourceSubscriptionManager import Subscription
from decisionengine.framework.modules.logging_configDict import LOGGERNAME
from decisionengine.framework.taskmanager.ProcessingState import State

_MAX_WAIT = 300  # 5 minutes
_DEFAULT_SCHEDULE = 300  # ""

delogger = structlog.getLogger(LOGGERNAME)
delogger = delogger.bind(module=__name__.split(".")[-1])


class TaskRunner:
    """
    Provides interface to loadable modules and events for synchronization of execution
    """

    def __init__(self, conf_dict):
        """
        :type conf_dict: :obj:`dict`
        :arg conf_dict: configuration dictionary describing the runner
        """

        self.runner = create_runner(conf_dict["module"], conf_dict["name"], conf_dict["parameters"])
        self.module = conf_dict["module"]
        self.name = self.runner.__class__.__name__
        self.schedule = conf_dict.get("schedule", _DEFAULT_SCHEDULE)
        self.run_counter = 0
        self.data_updated = threading.Event()
        self.stop_running = threading.Event()
        delogger.debug(
            "Creating channel execution runner: module=%s name=%s parameters=%s schedule=%s",
            self.module,
            self.name,
            conf_dict["parameters"],
            self.schedule,
        )


def _make_runners_for(configs):
    return {name: TaskRunner(e) for name, e in configs.items()}


class Channel:
    """
    Decision Channel.
    Instantiates runners according to channel configuration
    """

    def __init__(self, channel_dict):
        """
        :type channel_dict: :obj:`dict`
        :arg channel_dict: channel configuration
        """

        delogger.debug("Creating channel transform")
        self.transforms = _make_runners_for(channel_dict["transforms"])
        delogger.debug("Creating channel logicengine")
        self.le_s = _make_runners_for(channel_dict["logicengines"])
        delogger.debug("Creating channel publisher")
        self.publishers = _make_runners_for(channel_dict["publishers"])
        self.channel_manager = channel_dict.get("channel_manager", {})


class ChannelManager(ComponentManager):
    """
    Channel Manager: Runs decision cycle for transforms and publishers
    """

    def __init__(
        self, name, dataspace, generation_id, channel_dict, global_config, subscribe_queue, channel_subscribed
    ):

        super().__init__(name, generation_id, global_config)

        self.all_sources = list(channel_dict["sources"].keys())
        self.channel = Channel(channel_dict)
        self.source_new_data = {}  # Maintains flags for each source which is True if new data products have been sent
        self.subscribe_queue = subscribe_queue
        self.channel_subscribed = channel_subscribed
        self.channel_subscribed[self.id] = False
        self.lock = threading.Lock()
        self.dataspace = dataspace
        self.channel_data_source = None  # Set to the appropriate multiprocessing.Queue by the DecisionEngine itself after the Channel is instantiated
        self.channel_data_block = datablock.DataBlock(
            self.dataspace, name, self.id, generation_id
        )  # All DataBlock access for this channel

    def wait_for_all(self, events_done):
        """
        Wait for all sources or transforms to finish

        :type events_done: :obj:`list`
        :arg events_done: list of events to wait for
        """
        delogger.info("Waiting for all channels to run")

        try:
            while not all(e.is_set() for e in events_done):
                time.sleep(1)
                if self.state.should_stop():
                    break

            for e in events_done:
                e.clear()
        except Exception:  # pragma: no cover
            delogger.exception("Unexpected error!")
            raise

    def wait_for_all_sources(self, channel_sources):
        """
        Wait for all sources this channel is interested in to finish their execution

        :type channel_sources: :obj:`list`
        :arg channel_sources: list of sources that need to be polled for completion
        """
        delogger.info("Waiting for all sources to run")
        all_ready = False
        while not all_ready:
            sources_ran = []
            for source in channel_sources:
                try:
                    source_ran = self.source_new_data[source]
                    sources_ran.append(source_ran)
                except KeyError:
                    # If the source has not run yet, this is to be expected
                    pass
            if len(sources_ran) > 0 and all(sources_ran):
                all_ready = True
            else:
                time.sleep(1)
                if self.state.should_stop():
                    break

    def wait_for_any_source(self, channel_sources):
        """
        Waits for any source this channel is interested in to post an updated data block before allowing continuation

        :type channel_sources: :obj:`list`
        :arg channel_sources: list of sources to be watched for updated data
        """
        delogger.info("Waiting for any source to run")
        while True:
            sources_ran = []
            for source in channel_sources:
                source_ran = self.source_new_data[source]
                if source_ran:
                    sources_ran.append(source)
            if len(sources_ran) > 0:
                return sources_ran
            else:
                time.sleep(1)
                if self.state.should_stop():
                    break

    def reset_source_flags(self, sources):
        """
        Sets self.source_new_data to False for the sources which are being used by this decision cycle

        :type sources: :obj:`list`
        :arg sources: list of source names that are to be set back to the "not-updated" state
        """
        for source in sources:
            self.source_new_data[source] = False

    def register_with_sources(self, channel_id, channel_name, all_sources):
        """
        Sends registration information for the sources that the channel is interested in to the SourceSubscriptionManager
        """
        for source in all_sources:
            self.source_new_data[source] = False

        sub = Subscription(channel_id, channel_name, all_sources)
        self.subscribe_queue.put(sub)

    def wait_for_registration(self, channel_id):
        has_registered = self.channel_subscribed[channel_id]
        while not has_registered:
            time.sleep(1)
            has_registered = self.channel_subscribed[channel_id]

    def check_for_new_data_products(self):
        """
        Check the incoming data product queue, insert into datablock, and update source_new_data appropriately
        """
        while True:
            try:
                new_product = self.channel_data_source.get(False)
            except queue.Empty:
                break
            source_name = new_product["source_name"]
            data = new_product["data"]
            header = new_product["header"]

            self.data_block_put(data, header, self.channel_data_block)
            self.source_new_data[source_name] = True

    def run(self):
        """
        Channel Manager main loop
        """
        delogger.setLevel(self.loglevel.value)
        delogger.info(f"Starting Channel Manager {self.id}")
        delogger.info(f"Registering Channel Manager {self.id} source subscriptions")
        self.source_new_data = dict.fromkeys(self.all_sources, False)
        self.register_with_sources(self.id, self.name, self.all_sources)
        self.wait_for_registration(self.id)
        delogger.info(f"Registered Channel manager {self.id} for sources ")
        self.check_for_new_data_products()
        self.wait_for_all_sources(self.all_sources)
        delogger.info("All sources finished")
        self.state.set(State.STEADY)

        # Should a decision cycle be automatically started at this point?
        # self.decision_cycle()

        while not self.state.should_stop():
            try:
                updated_sources = self.wait_for_any_source(self.all_sources)
                self.reset_source_flags(updated_sources)
                self.decision_cycle()
                if self.state.should_stop():
                    delogger.info(f"Channel Manager {self.id} received stop signal and exits")
                    for transform in self.channel.transforms.values():
                        transform.stop_running.set()
                        time.sleep(5)
                    break
            except Exception:  # pragma: no cover
                delogger.exception("Exception in the channel manager main loop")
                delogger.error("Error occured. Channel Manager %s exits with state %s", self.id, self.get_state_name())
                break
            time.sleep(1)

    def do_backup(self):
        """
        Duplicate current data block and return its copy

        :rtype: :obj:`~datablock.DataBlock`

        """

        with self.lock:
            data_block = self.data_block_t0.duplicate()
            delogger.debug(f"Duplicated block {data_block}")
        return data_block

    def decision_cycle(self):
        """
        Decision cycle to be run periodically (by trigger)
        """

        data_block_t1 = self.do_backup()
        try:
            self.run_transforms(data_block_t1)
        except Exception:
            delogger.exception("error in decision cycle(transforms) ")
            # We do not call 'take_offline' here because it has
            # already been called in the run_transform code on
            # operating on a separate thread.

        actions_facts = []
        try:
            actions_facts = self.run_logic_engine(data_block_t1)
            delogger.info("ran all logic engines")
        except Exception:
            delogger.exception("error in decision cycle(logic engine) ")
            self.take_offline(data_block_t1)

        for a_f in actions_facts:
            try:
                self.run_publishers(a_f["actions"], a_f["newfacts"], data_block_t1)
            except Exception:
                delogger.exception("error in decision cycle(publishers) ")
                self.take_offline(data_block_t1)

    def run_transforms(self, data_block=None):
        """
        Run transforms.
        So far in main process.

        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block

        """
        delogger.info("run_transforms")
        delogger.debug(f"run_transforms: data block {data_block}")
        if not data_block:
            return
        event_list = []
        threads = []
        for key, transform in self.channel.transforms.items():
            delogger.info(f"starting transform {key}")
            event_list.append(transform.data_updated)
            thread = threading.Thread(target=self.run_transform, name=transform.name, args=(transform, data_block))
            threads.append(thread)
            # Cannot catch exception from function called in separate thread
            thread.start()

        self.wait_for_all(event_list)
        for thread in threads:
            thread.join()
        delogger.info("all transforms finished")

    def run_transform(self, transform, data_block):
        """
        Run a transform

        :type transform: :obj:`~TaskRunner`
        :arg transform: source TaskRunner
        :type data_block: :obj:`~datablock.DataBlock`
        :arg data_block: data block
        """
        max_wait = self.channel.channel_manager.get("data_TO", _MAX_WAIT)
        consume_keys = transform.runner.consumes()

        delogger.info(
            "transform: %s expected keys: %s provided keys: %s", transform.name, consume_keys, list(data_block.keys())
        )
        loop_counter = 0
        while not self.state.should_stop():
            # Check if data is ready
            if set(consume_keys) <= set(data_block.keys()):
                # data is ready -  may run transform()
                delogger.info("run transform %s", transform.name)
                try:
                    with data_block.lock:
                        data = transform.runner.transform(data_block)
                    delogger.debug(f"transform returned {data}")
                    t = time.time()
                    header = datablock.Header(data_block.component_manager_id, create_time=t, creator=transform.name)
                    self.data_block_put(data, header, data_block)
                    delogger.info("transform put data")
                except Exception:
                    delogger.exception(f"exception from transform {transform.name} ")
                    self.take_offline(data_block)
                break
            s = transform.stop_running.wait(1)
            if s:
                delogger.info(f"received stop_running signal for {transform.name}")
                break
            loop_counter += 1
            if loop_counter == max_wait:
                delogger.info(f"transform {transform.name} did not get consumes data" f"in {max_wait} seconds. Exiting")
                break
        transform.data_updated.set()

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
                delogger.info("run logic engine %s", self.channel.le_s[le].name)
                delogger.debug("run logic engine %s %s", self.channel.le_s[le].name, data_block)
                rc = self.channel.le_s[le].runner.evaluate(data_block)
                le_list.append(rc)
                delogger.info("run logic engine %s done", self.channel.le_s[le].name)
                delogger.info(
                    "logic engine %s generated newfacts: %s",
                    self.channel.le_s[le].name,
                    rc["newfacts"].to_dict(orient="records"),
                )
                delogger.info("logic engine %s generated actions: %s", self.channel.le_s[le].name, rc["actions"])

            # Add new facts to the datablock
            # Add empty dataframe if nothing is available
            if le_list:
                all_facts = pd.concat([i["newfacts"] for i in le_list], ignore_index=True)
            else:
                delogger.info("Logic engine(s) did not return any new facts")
                all_facts = pd.DataFrame()

            data = {"de_logicengine_facts": all_facts}
            t = time.time()
            header = datablock.Header(data_block.component_manager_id, create_time=t, creator="logicengine")
            self.data_block_put(data, header, data_block)
        except Exception:  # pragma: no cover
            delogger.exception("Unexpected error!")
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
            log = delogger
            for action_list in actions.values():
                for action in action_list:
                    publisher = self.channel.publishers[action]
                    name = publisher.name
                    log.info(f"run publisher {name}")
                    log.debug(f"run publisher {name} {data_block}")
                    try:
                        publisher.runner.publish(data_block)
                    except KeyError as e:
                        if self.state.should_stop():
                            log.warning(f"ChannelManager stopping, ignore exception {name} publish() call: {e}")
                            continue
                        else:
                            raise
        except Exception:
            delogger.exception("Unexpected error!")
            raise
