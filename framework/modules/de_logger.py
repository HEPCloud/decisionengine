#!/usr/bin/env python
"""
Looger to use in all modules
"""
import os
import logging
import logging.handlers

LOG_FILE='/tmp/decision_engine_logs/decision_engine_log'
MB=1000000
ROTATE_AFTER = 6

def set_logging(log_file_name=LOG_FILE, max_file_size= 200*MB, max_backup_count = ROTATE_AFTER):
    """

    :type log_file_name: :obj:`str`
    :arg log_file_name: log file name
    :type  max_file_size: :obj:`int`
    :arg  max_file_size: maximal size of log file. If reached save and start new log.
    :type  max_backup_count: :obj:`int`
    :arg  max_backup_count: start rotaion after this number is reached
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    if not os.path.exists(os.path.dirname(log_file_name)):
        os.makedirs(os.path.dirname(log_file_name))
    logger = logging.getLogger("decision_engine")
    if logger.handlers:
        return

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(threadName)s - %(levelname)s - %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(log_file_name,
                                                        maxBytes=max_file_size,
                                                        backupCount=max_backup_count)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    debug_handler = logging.handlers.RotatingFileHandler("%s_debug"%(log_file_name,),
                                                         maxBytes=max_file_size,
                                                         backupCount=max_backup_count)
    debug_handler.setFormatter(formatter)
    debug_handler.setLevel(logging.DEBUG)
    logger.addHandler(debug_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger

def get_logger():
    """
    get default logger - "decision_engine"
    :rtype: :class:`logging.Logger` - rotating file logger
    """
    return logging.getLogger("decision_engine")


def set_stream_logging(logger_name=''):
    """
    This is for debugging.
    Set stream logging for logger.

    :type logger_name: :obj:`str`
    :arg logger_name: logger name
    :rtype: :class:`logging.Logger`
    """

    logger = logging.getLogger("decision_engine")
    #logger =  logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)
    #logger =  logging.getLogger(__name__)

    return logger

if __name__ == '__main__':
    my_logger = logging.getLogger("decision_engine")
    set_logging(log_file_name = '%s/de_log/decision_engine_log0'%(os.environ.get('HOME')),
                max_file_size = 100000,
                max_backup_count = 5)
    my_logger.info("THIS IS INFO")
    my_logger.error("THIS IS ERROR")
    my_logger.debug("THIS IS DEBUG")
