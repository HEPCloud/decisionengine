import logging
import tempfile
import unittest

import pytest

import decisionengine.framework.modules.de_logger as de_logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        mylogger = logging.getLogger("decision_engine")
        while mylogger.hasHandlers():
            try:
                mylogger.removeHandler(mylogger.handlers[0])
            except Exception:
                break

    def test_by_nonsense_is_err(self):
        with pytest.raises(ValueError) as err:
            with tempfile.NamedTemporaryFile() as log:
                de_logger.set_logging(log_level='INFO', max_backup_count=6,
                                      file_rotate_by="nonsense", max_file_size=1000000,
                                      log_file_name=log.name)
        assert "Incorrect 'file_rotate_by'" in str(err.value)

    def test_by_size(self):
        with tempfile.NamedTemporaryFile() as log:
            de_logger.set_logging(log_level='INFO', max_backup_count=6,
                                  file_rotate_by="size", max_file_size=1000000,
                                  log_file_name=log.name)
            mylogger = de_logger.get_logger()
            assert mylogger.hasHandlers() is True
            assert 'RotatingFileHandler' in str(mylogger.handlers)
            de_logger.set_stream_logging()
            assert mylogger.debug('debug') is None
            assert mylogger.info('infomsg') is None

#    def test_by_time(self):
#        with tempfile.NamedTemporaryFile() as log:
#            de_logger.set_logging(log_level='INFO', rotation_interval=1,
#                                  file_rotate_by="time", rotation_time_unit='D',
#                                  log_file_name=log.name)
#            mylogger = de_logger.get_logger()
#            assert mylogger.hasHandlers() is True
#            assert 'TimedRotatingFileHandler' in str(mylogger.handlers)
#            de_logger.set_stream_logging()
#            assert mylogger.debug('debug') is None
#            assert mylogger.info('infomsg') is None
