# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import gc
import tempfile

import pytest
import structlog

import decisionengine.framework.modules.de_logger as de_logger

from decisionengine.framework.modules.logging_configDict import LOGGERNAME


@pytest.fixture()
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


def test_by_nonsense_is_err(log_setup):
    with pytest.raises(ValueError, match=r".*Incorrect 'file_rotate_by'.*"), tempfile.NamedTemporaryFile() as log:
        log.flush()
        de_logger.configure_logging(
            log_level="INFO",
            max_backup_count=6,
            file_rotate_by="nonsense",
            max_file_size=1000000,
            log_file_name=log.name,
        )


def test_by_size(log_setup):
    with tempfile.NamedTemporaryFile() as log:
        log.flush()
        de_logger.configure_logging(
            log_level="INFO",
            max_backup_count=6,
            file_rotate_by="size",
            max_file_size=1000000,
            log_file_name=log.name,
            start_q_logger="False",
        )

        assert log_setup.hasHandlers() is True
        assert "RotatingFileHandler" in str(log_setup.handlers)
        assert log_setup.debug("debug") is None
        assert log_setup.info("infomsg") is None


def test_by_time(log_setup):
    with tempfile.NamedTemporaryFile() as log:
        log.flush()
        de_logger.configure_logging(
            log_level="INFO",
            rotation_interval=1,
            file_rotate_by="time",
            rotation_time_unit="D",
            log_file_name=log.name,
            start_q_logger="False",
        )

        assert log_setup.hasHandlers() is True
        assert "TimedRotatingFileHandler" in str(log_setup.handlers)
        assert log_setup.debug("debug") is None
        assert log_setup.info("infomsg") is None
