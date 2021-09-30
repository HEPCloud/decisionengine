"""
Source Manager
"""
import multiprocessing
import time

import structlog

from decisionengine.framework.dataspace import datablock
from decisionengine.framework.managers.ComponentManager import ComponentManager, create_runner
from decisionengine.framework.modules.logging_configDict import LOGGERNAME
from decisionengine.framework.taskmanager.ProcessingState import State

_DEFAULT_SCHEDULE = 300  # 5 minutes

delogger = structlog.getLogger(LOGGERNAME)
delogger = delogger.bind(module=__name__.split(".")[-1])


class SourceRunner:
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
        self.data_updated = multiprocessing.Event()
        self.stop_running = multiprocessing.Event()
        delogger.debug(
            "Creating source execution runner: module=%s name=%s parameters=%s schedule=%s",
            self.module,
            self.name,
            conf_dict["parameters"],
            self.schedule,
        )


class Source:
    """
    Decision Source.
    Instantiates Source runners according to the provided Source configuration
    """

    def __init__(self, name, source_dict):
        """
        :type source_dict: :obj:`dict`
        :arg source_dict: Source configuration
        """
        self.name = name
        self.source_runner = SourceRunner(source_dict)


class SourceManager(ComponentManager):
    """
    Source Manager: Runs decision cycle for transforms and publishers
    """

    def __init__(self, name, generation_id, source_config, global_config, data_block_queue):
        super().__init__(name, generation_id, global_config)

        self.source = Source(self.name, source_config)
        self.data_block_queue = data_block_queue
        self.lock = multiprocessing.Lock()

    def data_block_send(self, source_name, source_id, data, header):
        block_info = {"source_name": source_name, "source_id": source_id, "data": data, "header": header}
        self.data_block_queue.put(block_info)

    def run(self):
        src = self.source.source_runner
        delogger.setLevel(self.loglevel.value)
        delogger.info(f"Starting Source Manager {self.id}")

        # Then run the work loop to continually update the sources every 'period'
        while not self.state.should_stop():
            try:
                # Run the source
                delogger.info(f"Source {src.name} calling acquire")
                data = src.runner.acquire()
                delogger.info(f"Source {src.name} acquire retuned")
                delogger.info(f"Source {src.name} filling header")

                # Process the data block
                if data:
                    t = time.time()
                    header = datablock.Header(self.id, create_time=t, creator=src.module)
                    delogger.info(f"Source {src.name} header done")

                    # Send the datablock to the DecisionEngine process SubscriptionHandler
                    self.data_block_send(src.name, self.id, data, header)
                    delogger.info(f"Source {src.name} data block send done")
                else:
                    delogger.warning(f"Source {src.name} acquire retuned no data")
                src.run_counter += 1
                delogger.info(f"Source {src.name} {src.module} finished cycle")

                # If its the first time, update state so that anything waiting for the source to run for the first time proceeds
                if self.state.get() == State.BOOT:
                    self.state.set(State.STEADY)

                # Once we have run the source (be it 1st or nth time) we should wait for the configured interval before running again (shutting down if the signal is raised)
                if src.schedule > 0:
                    stop = src.stop_running.wait(src.schedule)
                    if stop:
                        delogger.info(f"Received stop_running signal for {src.name}")
                        break
                else:
                    delogger.info(f"Source {src.name} runs only once")
                    break
            except Exception:  # pragma: no cover
                delogger.exception("Exception in the main loop for a source")
                delogger.error("Error occured. Source %s exits with state %s", self.id, self.get_state_name())
                break
        self.take_offline(self.data_block_t0)
        delogger.info(f"Source {self.name} ({self.id}) is ending its loop.")
