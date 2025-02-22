# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import threading

import structlog

import decisionengine.framework.dataspace.dataspace as dataspace

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME
from decisionengine.framework.taskmanager.ProcessingState import ProcessingState, State, STOPPING_CONDITIONS


class Reaper:
    """
    Reaper provides functionality of periodic deletion
    of data older than retention_interval in days

    The class attributes indicate a rational set of defaults
    that shouldn't be altered by user configuration.
    """

    MIN_RETENTION_INTERVAL_DAYS = 7
    MIN_SECONDS_BETWEEN_RUNS = 2 * 60 * 59

    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """
        # Validate configuration
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)
        self.logger.debug("Initializing a reaper")

        # since we must validate this, have a private store space
        self.__retention_interval = self.MIN_RETENTION_INTERVAL_DAYS
        self.__seconds_between_runs = self.MIN_SECONDS_BETWEEN_RUNS

        if not config.get("dataspace"):
            self.logger.exception("Error in initializing Reaper!")
            raise dataspace.DataSpaceConfigurationError(
                "Invalid dataspace configuration: " "dataspace key not found in dictionary"
            )
        elif not isinstance(config.get("dataspace"), dict):
            self.logger.exception("Error in initializing Reaper!")
            raise dataspace.DataSpaceConfigurationError(
                "Invalid dataspace configuration: " "dataspace key must correspond to a dictionary"
            )
        try:
            db_driver_name = config["dataspace"]["datasource"]["name"]
            db_driver_module = config["dataspace"]["datasource"]["module"]
            db_driver_config = config["dataspace"]["datasource"]["config"]
            self.retention_interval = config["dataspace"]["retention_interval_in_days"]
            self.seconds_between_runs = config["dataspace"].get("reaper_run_interval", 24 * 60 * 60)
        except KeyError:
            self.logger.exception("Error in initializing Reaper!")
            raise dataspace.DataSpaceConfigurationError("Invalid dataspace configuration")

        self.datasource = dataspace.DataSourceLoader().create_datasource(
            db_driver_module, db_driver_name, db_driver_config
        )

        self.thread = None
        self.state = ProcessingState()

    @property
    def retention_interval(self):
        """We have data constraints, so use a property to track"""
        return self.__retention_interval

    @retention_interval.setter
    def retention_interval(self, value):
        if int(value) < self.MIN_RETENTION_INTERVAL_DAYS:
            self.logger.exception("Error in initializing Reaper!")
            raise ValueError(
                f"For safety the data retention interval has to be greater than {self.MIN_RETENTION_INTERVAL_DAYS} days"
            )
        self.logger.debug(f"Reaper setting retention_interval to {value}.")
        self.__retention_interval = int(value)

    @property
    def seconds_between_runs(self):
        """We have data constraints, so use a property to track"""
        return self.__seconds_between_runs

    @seconds_between_runs.setter
    def seconds_between_runs(self, value):
        if int(value) < self.MIN_SECONDS_BETWEEN_RUNS:
            self.logger.exception("Error in initializing Reaper!")
            raise ValueError(
                f"For performance the time between runs to be greater than {self.MIN_SECONDS_BETWEEN_RUNS} seconds"
            )
        self.logger.debug(f"Reaper setting seconds_between_runs to {value}.")
        self.__seconds_between_runs = int(value)

    def reap(self):
        """
        Actually spawn the query to delete the old records.
        Lock the state as this task doesn't have a cancel option.
        """
        with self.state.lock:
            if self.state.should_stop():
                return
            self.logger.info("Reaper.reap() started.")
            self.state.set(State.ACTIVE)
            self.datasource.delete_data_older_than(self.retention_interval)
            self.state.set(State.STEADY)
            self.logger.info("Reaper.reap() completed.")

    def _reaper_loop(self, delay):
        """
        The thread actually runs this.
        """
        self.logger.debug("Reaper thread started.")
        between_runs = delay
        while not self.state.should_stop():
            try:
                with self.state.lock:
                    if not self.state.should_stop():
                        # The start function will block until the state is changed from BOOT
                        # If we are signaled to stop, don't override that state
                        self.state.set(State.IDLE)

                self.logger.debug(f"Reaper waiting {between_runs} seconds or for a stop.")
                self.state.wait_until(STOPPING_CONDITIONS, timeout=between_runs)

                # in stop state, end wait and get out of the loop ASAP
                if self.state.should_stop():
                    self.logger.debug(f"Reaper received a stop event: {self.state.get()}.")
                else:
                    self.reap()
                    # after waiting the initial delay time
                    #  use the self.seconds_between_runs as the delay
                    if between_runs != self.seconds_between_runs:
                        between_runs = self.seconds_between_runs
            except Exception:  # pragma: no cover
                self.state.set(State.ERROR)
                self.logger.exception(f"Reaper.reap() failed: {self.state.get()}.")
                break
        else:
            # we did not use 'break' to exit the loop
            self.state.set(State.SHUTDOWN)
            self.logger.info("Reaper shutdown cleanly.")

    def start(self, delay=0):
        """
        Start thread with an optional delay to start the thread in X seconds
        """
        if self.state.should_stop() and not self.state.inactive():
            self.logger.debug(f"Reaper asked to start during stop: {self.state.get()}.")

        if isinstance(self.thread, threading.Thread) and self.thread.is_alive():
            try:
                # threads need to end, else we orphan one and make a new thread
                raise RuntimeError("Reaper asked to start, but it is running already.")
            except RuntimeError as __e:
                self.logger.exception(__e)
                raise

        try:
            # each invocation must be a new thread
            with self.state.lock:
                self.state.set(State.BOOT)
                self.thread = threading.Thread(
                    group=None, target=self._reaper_loop, args=(delay,), name="Reaper_loop_thread"
                )

                self.thread.start()
        except Exception:  # pragma: no cover
            self.logger.exception("Reaper loop thread not started")

        self.state.wait_while(State.BOOT)

    def stop(self):
        """
        Try to stop the reaper, will block if the reaper cannot be interrupted.
        """
        if isinstance(self.thread, threading.Thread):
            if self.thread.is_alive():
                with self.state.lock:
                    if not self.state.should_stop():
                        self.logger.debug("Sending reaper State.SHUTTINGDOWN signal")
                        self.state.set(State.SHUTTINGDOWN)
                if self.state.has_value(State.SHUTTINGDOWN):
                    self.state.wait_while(State.SHUTTINGDOWN)
                self.logger.info(f"Reaper shutdown : {self.state.get()}.")
                self.thread.join()
            else:
                self.logger.debug(f"Reaper tried to stop but is stopped already: {self.state.get()}.")
        else:
            self.logger.debug("Reaper tried to stop but was never started")

    def __repr__(self):  # pragma: no cover
        return (
            f"Reaper, retention interval {self.retention_interval,} days, "
            f"between runs wait {self.seconds_between_runs} seconds, state {self.state.get()}"
        )
