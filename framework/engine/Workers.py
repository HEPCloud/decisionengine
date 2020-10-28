import logging
import multiprocessing
import os
import threading

import decisionengine.framework.taskmanager.ProcessingState as ProcessingState

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(module)s - %(process)d - %(threadName)s - %(levelname)s - %(message)s")


class Worker(multiprocessing.Process):

    def __init__(self, task_manager, logger_config):
        super().__init__()
        self.task_manager = task_manager
        self.task_manager_id = task_manager.id
        self.logger_config = logger_config

    def wait_until(self, state):
        return self.task_manager.state.wait_until(state)

    def wait_while(self, state):
        return self.task_manager.state.wait_while(state)

    def get_state_name(self):
        return self.task_manager.get_state_name()

    def run(self):
        logger = logging.getLogger()
        logger_rotate_by = self.logger_config.get("file_rotate_by", "size")

        if logger_rotate_by == "size":
            file_handler = logging.handlers.RotatingFileHandler(os.path.join(
                                                                os.path.dirname(
                                                                    self.logger_config["log_file"]),
                                                                self.task_manager.name + ".log"),
                                                                maxBytes=self.logger_config.get("max_file_size",
                                                                200 * 1000000),
                                                                backupCount=self.logger_config.get("max_backup_count",
                                                                6))
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(
                                                                     os.path.dirname(
                                                                         self.logger_config["log_file"]),
                                                                     self.task_manager.name + ".log"),
                                                                     when=self.logger_config.get("rotation_time_unit", 'D'),
                                                                     interval=self.logger_config.get("rotation_time_interval", '1'))

        file_handler.setFormatter(FORMATTER)
        logger.setLevel(logging.WARNING)
        logger.addHandler(file_handler)
        channel_log_level = self.logger_config.get("global_channel_log_level", "WARNING")
        self.task_manager.set_loglevel(channel_log_level)
        self.task_manager.run()


class Workers:
    def __init__(self):
        self._workers = {}
        self._lock = threading.Lock()

    def access(self):
        class Lock:
            def __init__(self, workers, lock):
                self._workers = workers
                self._lock = lock

            def _update_channel_states(self):
                for channel, process in self._workers.items():
                    if process.is_alive():
                        continue
                    if process.task_manager.state.inactive():
                        continue
                    process.task_manager.state.set(ProcessingState.State.ERROR)

            def __enter__(self):
                self._lock.acquire()
                self._update_channel_states()
                return self._workers

            def __exit__(self, error, type, bt):
                self._lock.release()

        return Lock(self._workers, self._lock)

    def unguarded_access(self):
        class NoLock:
            def __init__(self, workers, lock):
                self._workers = workers
                self._lock = lock  # Only used to update channels while entering context

            def _update_channel_states(self):
                for channel, process in self._workers.items():
                    if process.is_alive():
                        continue
                    if process.task_manager.state.inactive():
                        continue
                    process.task_manager.state.set(ProcessingState.State.ERROR)

            def __enter__(self):
                with self._lock:
                    self._update_channel_states()
                return self._workers

            def __exit__(self, error, type, bt):
                pass

        return NoLock(self._workers, self._lock)
