"""
Logger to use in all modules
"""
import os
import logging
import logging.handlers
import logging.config
import structlog
import decisionengine.framework.modules.logging_configDict as configDict

MB = 1000000

logger = structlog.getLogger("decision_engine")
logger = logger.bind(module=__name__.split(".")[-1])


def set_logging(
    log_level,
    file_rotate_by,
    rotation_time_unit="D",
    rotation_interval=1,
    max_backup_count=6,
    max_file_size=200 * MB,
    log_file_name="/tmp/decision_engine_logs/decision_engine_log",
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
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    dirname = os.path.dirname(log_file_name)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)

    logger.setLevel(getattr(logging, log_level.upper()))
    if logger.handlers:
        return

    configDict.pylogconfig["handlers"]["de_file_debug"].update({"filename": "{}_debug".format(log_file_name)})
    configDict.pylogconfig["handlers"]["de_file_info"].update({"filename": "{}".format(log_file_name)})
    configDict.pylogconfig["handlers"]["file_structlog_debug"].update(
        {"filename": "{}_structlog_debug".format(log_file_name)}
    )

    if file_rotate_by == "size":
        configDict.pylogconfig["handlers"]["de_file_debug"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )
        configDict.pylogconfig["handlers"]["de_file_info"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )
        configDict.pylogconfig["handlers"]["file_structlog_debug"].update(
            {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": max_file_size,
                "backupCount": max_backup_count,
            }
        )

    else:
        raise ValueError(f"Incorrect 'file_rotate_by':'{file_rotate_by}:'")

    logging.config.dictConfig(configDict.pylogconfig)
    logger.debug("de logging setup complete")


def get_logger():
    """
    get default logger - "decision_engine"
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    return logger


def set_stream_logging(logger_name="decision_engine"):
    """
    This is for debugging.
    Set stream logging for logger.
    :type logger_name: :obj:`str`
    :arg logger_name: logger name
    :rtype: :class:`logging.Logger`
    """

    stlogger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    stlogger.addHandler(handler)
    stlogger.setLevel(logging.DEBUG)
    return stlogger


if __name__ == "__main__":
    set_logging(
        "ERROR",
        "size",
        "D",
        1,
        max_backup_count=5,
        max_file_size=100000,
        log_file_name="%s/de_log/decision_engine_log0" % (os.environ.get("HOME")),
    )
    logger.error("THIS IS ERROR")
    logger.info("THIS IS INFO")
    logger.debug("THIS IS DEBUG")
