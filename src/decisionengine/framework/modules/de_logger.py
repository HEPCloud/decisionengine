"""
Logger to use in all modules
"""
import os
import logging
import logging.handlers

MB = 1000000

def set_logging(log_level,
                file_rotate_by,
                rotation_time_unit='D',
                rotation_interval=1,
                max_backup_count=6,
                max_file_size=200 * MB,
                log_file_name='/tmp/decision_engine_logs/decision_engine_log'):
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
    logger = logging.getLogger("decision_engine")
    logger.setLevel(getattr(logging, log_level.upper()))

    if logger.handlers:
        logger.debug('Reusing existing logging handlers')
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(threadName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z")
    file_handler = None

    if file_rotate_by == "size":
        file_handler = logging.handlers.RotatingFileHandler(log_file_name,
                                                            maxBytes=max_file_size,
                                                            backupCount=max_backup_count)
    elif file_rotate_by == "time":
        file_handler = logging.handlers.TimedRotatingFileHandler(log_file_name,
                                                                 when=rotation_time_unit,
                                                                 interval=rotation_interval)
    else:
        raise ValueError(f"Incorrect 'file_rotate_by':'{file_rotate_by}:'")

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    if log_file_name != '/dev/null':
        if file_rotate_by == "size":
            debug_handler = logging.handlers.RotatingFileHandler("{}_debug".format(log_file_name),
                                                                 maxBytes=max_file_size,
                                                                 backupCount=max_backup_count)
        elif file_rotate_by == "time":
            debug_handler = logging.handlers.TimedRotatingFileHandler("{}_debug".format(log_file_name),
                                                                      when=rotation_time_unit,
                                                                      interval=rotation_interval)
        else:
            raise ValueError(f"Incorrect 'file_rotate_by':'{file_rotate_by}:'")

        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(logging.DEBUG)
        logger.addHandler(debug_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

    return logger


def get_logger():
    """
    get default logger - "decision_engine"
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    return logging.getLogger("decision_engine")


def set_stream_logging(logger_name='decision_engine'):
    """
    This is for debugging.
    Set stream logging for logger.

    :type logger_name: :obj:`str`
    :arg logger_name: logger name
    :rtype: :class:`logging.Logger`
    """
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    my_logger = logging.getLogger("decision_engine")
    set_logging("ERROR",
                "size",
                'D',
                1,
                max_backup_count=5,
                max_file_size=100000,
                log_file_name='%s/de_log/decision_engine_log0' % (os.environ.get('HOME')))
    my_logger.info("THIS IS INFO")
    my_logger.info("THIS IS INFO")
    my_logger.debug("THIS IS DEBUG")
