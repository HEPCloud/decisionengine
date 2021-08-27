import logging
import structlog
import multiprocessing
import os
import threading

import decisionengine.framework.taskmanager.ProcessingState as ProcessingState
from decisionengine.framework.modules.logging_configDict import pylogconfig as logconf
from decisionengine.framework.modules.logging_configDict import CHANNELLOGGERNAME

MAX_CHANNEL_FILE_SIZE = 200 * 1000000


class Worker(multiprocessing.Process):
    '''
    Class that encapsulates a channel's task manager as a separate process.

    This class' run function is called whenever the process is
    started.  If the process is abruptly terminated--e.g. the run
    method is pre-empted by a signal or an os._exit(n) call--the
    Worker object will still exist even if the operating-system
    process no longer does.

    To determine the exit code of this process, use the
    Worker.exitcode value, provided by the multiprocessing.Process
    base class.
    '''

    def __init__(self, task_manager, logger_config):
        super().__init__(name=f'DEWorker-{task_manager.name}')
        self.task_manager = task_manager
        self.task_manager_id = task_manager.id
        self.logger_config = logger_config
        self.logger = None

    def wait_until(self, state, timeout=None):
        return self.task_manager.state.wait_until(state, timeout)

    def wait_while(self, state, timeout=None):
        return self.task_manager.state.wait_while(state, timeout)

    def get_state_name(self):
        return self.task_manager.get_state_name()

    def get_produces(self):
        return self.task_manager.get_produces()

    def get_consumes(self):
        return self.task_manager.get_consumes()

    def run(self):

        myname = self.task_manager.name
        myfilename = os.path.join(
            os.path.dirname(self.logger_config["log_file"]), myname + ".log"
        )

        self.logger = structlog.getLogger(CHANNELLOGGERNAME)

        # setting a default value here. value from config file is set in call
        # self.task_manager.set_loglevel_value after logger configuration is completed
        logging.getLogger(CHANNELLOGGERNAME).setLevel(logging.DEBUG)

        # TODO:
        # alter decisionengine.framework.modules.de_logger set_logging
        # so we can reuse it here and reduce duplication
        logger_rotate_by = self.logger_config.get("file_rotate_by", "size")

        # logconf is our global object edited in global space on purpose

        if logger_rotate_by == "size":
            logconf["handlers"].update(
                {
                    myname: {
                        "level": "DEBUG",
                        "filename": myfilename,
                        "formatter": "plain",
                        "class": "logging.handlers.RotatingFileHandler",
                        "maxBytes": MAX_CHANNEL_FILE_SIZE,
                        "backupCount": self.logger_config.get("max_backup_count", 6),
                    }
                }
            )
        elif logger_rotate_by == "time":
            logconf["handlers"].update(
                {
                    myname: {
                        "level": "DEBUG",
                        "filename": myfilename,
                        "formatter": "plain",
                        "class": "logging.handlers.TimedRotatingFileHandler",
                        "when": "D",
                        "interval": 1,
                    }
                }
            )
        else:
            raise ValueError(f"Incorrect 'logger_rotate_by':'{logger_rotate_by}:'")

        logconf["loggers"].update(
            {
                CHANNELLOGGERNAME: {
                    "handlers": [myname, "file_structlog_debug"],
                }
            }
        )
        logging.config.dictConfig(logconf)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=myname)

        channel_log_level = self.logger_config.get(
            "global_channel_log_level", "WARNING"
        )
        self.task_manager.set_loglevel_value(channel_log_level)
        self.task_manager.run()


class Workers:
    '''
    This class manages and provides access to the task-manager workers.

    The intention is that the decision engine never directly interacts with the
    workers but refers to them via a context manager:

      with workers.access() as ws:
          # Access to ws now protected
          ws['new_channel'] = Worker(...)

    In cases where the decision engine's block_while or block_until
    methods must be called (e.g. during tests), one should used the
    unguarded access:

      with workers.unguarded_access() as ws:
          # Access to ws is unprotected
          ws['new_channel'].wait_until(...)

    Calling a blocking method while using the protected context
    manager (i.e. workers.access()) will likely result in a deadlock.
    '''

    def __init__(self):
        self._workers = {}
        self._lock = threading.Lock()

    def _update_channel_states(self):
        with self._lock:
            for process in self._workers.values():
                if process.is_alive():
                    continue
                if process.task_manager.state.inactive():
                    continue
                process.task_manager.state.set(ProcessingState.State.ERROR)

    class Access:
        def __init__(self, workers, lock):
            self._workers = workers
            self._lock = lock

        def __enter__(self):
            if self._lock:
                self._lock.acquire()
            return self._workers

        def __exit__(self, error, type, bt):
            if self._lock:
                self._lock.release()

    def access(self):
        self._update_channel_states()
        return self.Access(self._workers, self._lock)

    def unguarded_access(self):
        self._update_channel_states()
        return self.Access(self._workers, None)
