"""
Logger to use in all modules
"""
import logging
import logging.config
import logging.handlers
import os

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME
from decisionengine.framework.modules.logging_configDict import pylogconfig as logconf

MB = 1000000

logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


def set_logging(
    log_level,
    file_rotate_by,
    rotation_time_unit="D",
    rotation_interval=1,
    max_backup_count=6,
    max_file_size=200 * MB,
    log_file_name="/tmp/decision_engine_logs/decisionengine.log",
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
    :arg  max_backup_count: start rotaion after this number is reached
    :rtype: None
    """
    dirname = os.path.dirname(log_file_name)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    logger.setLevel(getattr(logging, log_level.upper()))
    if logger.handlers:
        logger.debug("Reusing existing logging handlers")
        return None

    # logconf is our global object edited in global space on purpose

    logconf["handlers"]["de_file_debug"].update({"filename": f"{log_file_name}_debug.log"})
    logconf["handlers"]["de_file_info"].update({"filename": f"{log_file_name}.log"})
    logconf["handlers"]["file_structlog_debug"].update({"filename": f"{log_file_name}_structlog_debug.log"})

    if file_rotate_by == "size":
        logconf["handlers"]["de_file_debug"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )
        logconf["handlers"]["de_file_info"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )
        logconf["handlers"]["file_structlog_debug"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )

    elif file_rotate_by == "time":
        logconf["handlers"]["de_file_debug"].update(
            {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": rotation_time_unit,
                "interval": rotation_interval,
            }
        )
        logconf["handlers"]["de_file_info"].update(
            {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": rotation_time_unit,
                "interval": rotation_interval,
            }
        )
        logconf["handlers"]["file_structlog_debug"].update(
            {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": rotation_time_unit,
                "interval": rotation_interval,
            }
        )
    else:
        raise ValueError(f"Incorrect 'file_rotate_by':'{file_rotate_by}:'")

    logging.config.dictConfig(logconf)
    logger.debug("de logging setup complete")


def get_logger():
    """
    get default logger - "decisionengine"
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    return logger


if __name__ == "__main__":
    set_logging(
        "ERROR",
        "size",
        "D",
        1,
        max_backup_count=5,
        max_file_size=100000,
        log_file_name=f"{os.environ.get('HOME')}/de_log/decision_engine_log0",
    )
    logger.error("THIS IS ERROR")
    logger.info("THIS IS INFO")
    logger.debug("THIS IS DEBUG")
