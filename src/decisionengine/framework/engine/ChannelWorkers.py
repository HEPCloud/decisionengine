# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import logging
import multiprocessing
import os
import threading

import structlog

import decisionengine.framework.modules.de_logger as de_logger
import decisionengine.framework.modules.logging_configDict as logconf
import decisionengine.framework.taskmanager.ProcessingState as ProcessingState

MB = 1000000


class ChannelWorker(multiprocessing.Process):
    """
    Class that encapsulates a channel's task manager as a separate process.

    This class' run function is called whenever the process is
    started.  If the process is abruptly terminated--e.g. the run
    method is preempted by a signal or an os._exit(n) call--the
    ChannelWorker object will still exist even if the operating-system
    process no longer does.

    To determine the exit code of this process, use the
    ChannelWorker.exitcode value, provided by the multiprocessing.Process
    base class.
    """

    def __init__(self, task_manager, logger_config):
        super().__init__(name=f"DEChannelWorker-{task_manager.name}")
        self.task_manager = task_manager
        self.logger_config = logger_config

    def wait_while(self, state, timeout=None):
        return self.task_manager.state.wait_while(state, timeout)

    def get_state_name(self):
        return self.task_manager.get_state_name()

    def get_produces(self):
        return self.task_manager.get_produces()

    def get_consumes(self):
        return self.task_manager.get_consumes()

    def setup_logger(self):
        myname = self.task_manager.name
        myfilename = os.path.join(os.path.dirname(self.logger_config["log_file"]), myname + ".log")
        start_q_logger = self.logger_config.get("start_q_logger", "True")

        self.logger = structlog.getLogger(logconf.CHANNELLOGGERNAME)

        # setting a default value here. value from config file is set in call
        # self.task_manager.set_loglevel_value after logger configuration is completed
        logging.getLogger(logconf.CHANNELLOGGERNAME).setLevel(logging.DEBUG)

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
            self.task_manager.state.set(ProcessingState.State.ERROR)
            raise ValueError(f"Incorrect 'logger_rotate_by':'{logger_rotate_by}:'")

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(logconf.userformat))

        self.logger.addHandler(handler)

        if start_q_logger == "True":
            self.logger.addHandler(de_logger.get_queue_logger().structlog_q_handler)

        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=myname)

        channel_log_level = self.logger_config.get("global_channel_log_level", "WARNING")
        self.task_manager.set_loglevel_value(channel_log_level)

    def run(self):
        self.setup_logger()
        self.logger.debug(f"Worker for channel {self.task_manager.name} starting cycles")
        self.task_manager.run_cycles()


class ChannelWorkers:
    """
    This class manages and provides access to the task-manager workers.

    The intention is that the decision engine never directly interacts with the
    workers but refers to them via a context manager:

      with workers.access() as ws:
          # Access to ws now protected
          ws['new_channel'] = ChannelWorker(...)

    In cases where the decision engine's block_while method must be
    called (e.g. during tests), one should use unguarded access:

      ws = workers.get_unguarded()
      # Access to ws is unprotected
      ws['new_channel'].wait_while(...)

    Calling a blocking method while using the protected context
    manager (i.e. workers.access()) will likely result in a deadlock.
    """

    def __init__(self):
        self._workers = {}
        self._lock = threading.Lock()

    class Access:
        def __init__(self, workers, lock):
            self._workers = workers
            self._lock = lock

        def __enter__(self):
            self._lock.acquire()
            return self._workers

        def __exit__(self, error, type, bt):
            self._lock.release()

    def accessed_by_another_thread(self):
        return self._lock.locked()

    def access(self):
        return self.Access(self._workers, self._lock)

    def get_unguarded(self):
        return self._workers
