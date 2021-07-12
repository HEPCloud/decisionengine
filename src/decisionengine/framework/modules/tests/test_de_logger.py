import gc
import tempfile

import pytest
import structlog

import decisionengine.framework.modules.de_logger as de_logger
from decisionengine.framework.modules.de_logger import LOGGERNAME

@pytest.fixture
def log_setup():
    my_log = structlog.getLogger(LOGGERNAME)

    # make sure it is in a known "unconfigured state"
    while len(my_log.handlers) > 0:
        my_log.removeHandler(my_log.handlers[0])

    yield my_log

    # make sure we leave this without any handlers
    while len(my_log.handlers) > 0:
        my_log.removeHandler(my_log.handlers[0])

    gc.collect()


@pytest.mark.usefixtures("log_setup")
@pytest.mark.skip(reason="test failing under structlog config, needs re-working")
def test_by_nonsense_is_err(log_setup):
    with pytest.raises(ValueError) as err:
        with tempfile.NamedTemporaryFile() as log:
            de_logger.set_logging(
                log_level="INFO",
                max_backup_count=6,
                file_rotate_by="nonsense",
                max_file_size=1000000,
                log_file_name=log.name,
            )
    assert "Incorrect 'file_rotate_by'" in str(err.value)


@pytest.mark.usefixtures("log_setup")
@pytest.mark.skip(reason="test failing under structlog config, needs re-working")
def test_by_size(log_setup):
    with tempfile.NamedTemporaryFile() as log:
        de_logger.set_logging(
            log_level="INFO", max_backup_count=6, file_rotate_by="size", max_file_size=1000000, log_file_name=log.name
        )

        assert log_setup.hasHandlers() is True
        assert "RotatingFileHandler" in str(log_setup.handlers)
        assert log_setup.debug("debug") is None
        assert log_setup.info("infomsg") is None


@pytest.mark.usefixtures("log_setup")
@pytest.mark.skip(reason="test failing under structlog config, needs re-working")
def test_by_time(log_setup):
    with tempfile.NamedTemporaryFile() as log:
        de_logger.set_logging(
            log_level="INFO", rotation_interval=1, file_rotate_by="time", rotation_time_unit="D", log_file_name=log.name
        )

        assert log_setup.hasHandlers() is True
        assert "TimedRotatingFileHandler" in str(log_setup.handlers)
        assert log_setup.debug("debug") is None
        assert log_setup.info("infomsg") is None
