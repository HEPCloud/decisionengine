# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Logger to use in all modules
"""
import logging
import logging.config
import logging.handlers
import os
import tempfile

import structlog

import decisionengine.framework.modules.logging_configDict as logconf
import decisionengine.framework.modules.QueueLogger as QueueLogger

MB = 1000000

delogger = structlog.getLogger(logconf.LOGGERNAME)
delogger = delogger.bind(module=__name__.split(".")[-1], channel=logconf.DELOGGER_CHANNEL_NAME)

queue_logger = QueueLogger.QueueLogger()


def configure_logging(
    log_level="DEBUG",
    file_rotate_by="size",
    rotation_time_unit="D",
    rotation_interval=1,
    max_backup_count=6,
    max_file_size=200 * MB,
    log_file_name="/tmp/decision_engine_logs/decisionengine.log",
    start_q_logger="True",
):
    """

    :type log_level: :obj:`str`
    :arg log_level: log level
    :type file_rotate_by: :obj: `str`
    :arg file_rotate_by: files rotation by size or by time
    :type rotation_time_unit: :obj:`str`
    :arg rotation_time_unit: unit of time for file rotation
    :type rotation_interval: :obj:`int`
    :arg rotation_interval: time in rotation_time_units between file rotations
    :type log_file_name: :obj:`str`
    :arg log_file_name: log file name
    :type  max_file_size: :obj:`int`
    :arg  max_file_size: maximal size of log file. If reached save and start new log.
    :type  max_backup_count: :obj:`int`
    :arg  max_backup_count: start rotation after this number is reached
    :rtype: None
    """
    if log_file_name in (None, ""):
        # we explicitly asked for no name, but a filename
        # is actually required for this to work.
        log_file_name = tempfile.NamedTemporaryFile().name

    dirname = os.path.dirname(log_file_name)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    delogger.setLevel(getattr(logging, log_level.upper()))
    if delogger.handlers:
        delogger.debug("Reusing existing logging handlers")
        return None

    # configure handlers
    handlers_list = []

    if file_rotate_by == "size":
        for files in logconf.de_outfile_info:
            handler = logging.handlers.RotatingFileHandler(
                filename=f"{log_file_name}" + files[0], maxBytes=max_file_size, backupCount=max_backup_count
            )
            handler.setLevel(files[1])
            handler.setFormatter(logging.Formatter(files[2]))
            handlers_list.append(handler)

    elif file_rotate_by == "time":
        for files in logconf.de_outfile_info:
            handler = logging.handlers.TimedRotatingFileHandler(
                filename=f"{log_file_name}" + files[0],
                when=rotation_time_unit,
                interval=rotation_interval,
                backupCount=max_backup_count,
            )
            handler.setLevel(files[1])
            handler.setFormatter(logging.Formatter(files[2]))
            handlers_list.append(handler)

    else:
        raise ValueError(f"Incorrect 'file_rotate_by':'{file_rotate_by}:'")

    structlog_handlers_list = [handlers_list.pop(i) for i in logconf.structlog_file_index]

    # setup standard file handlers
    for h in handlers_list:
        delogger.addHandler(h)

    # setup the queue logger
    if start_q_logger == "True":
        queue_logger.setup_queue_logging(delogger, structlog_handlers_list)
        queue_logger.start()

    delogger.debug("de logging setup complete")


def get_logger():
    """
    get default logger - "decisionengine"
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    return delogger


def get_queue_logger():
    """
    get QueueLogger which owns the logging queues and listeners
    :rtype: :class:`decisionengine.framework.modules.QueueLogger``
    """
    return queue_logger


def stop_queue_logger():
    queue_logger.stop()


if __name__ == "__main__":
    configure_logging(
        "ERROR",
        "size",
        "D",
        1,
        max_backup_count=5,
        max_file_size=100000,
        log_file_name=f"{os.environ.get('HOME')}/de_log/decision_engine_log0",
    )
    delogger.error("THIS IS ERROR")
    delogger.info("THIS IS INFO")
    delogger.debug("THIS IS DEBUG")
