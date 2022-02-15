# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import logging

import pytest

import decisionengine.framework.modules.QueueLogger as QueueLogger


@pytest.fixture()
def queue_logger_setup():
    q_log = QueueLogger.QueueLogger()
    yield q_log

    del q_log


@pytest.fixture()
def log_setup():
    test_log = logging.getLogger("test_logger")
    yield test_log

    del test_log


@pytest.fixture()
def handler_setup():
    test_handler = [logging.FileHandler(filename="/tmp/decisionengine.log")]
    yield test_handler

    del test_handler


@pytest.fixture(autouse=True)
def setup_queue_logging(queue_logger_setup, log_setup, handler_setup):
    queue_logger_setup.setup_queue_logging(log_setup, handler_setup)
    yield queue_logger_setup

    del queue_logger_setup


def test_setup_queue_logging(queue_logger_setup, log_setup, handler_setup):
    # queue_logger_setup.setup_queue_logging(log_setup, handler_setup)

    assert queue_logger_setup.structlog_q is not None
    assert isinstance(queue_logger_setup.structlog_q_handler, logging.handlers.QueueHandler)
    assert "QueueHandler" in str(log_setup.handlers)
    assert isinstance(queue_logger_setup.structlog_listener, logging.handlers.QueueListener)


def test_start_queue_logger(queue_logger_setup, log_setup, handler_setup):
    # queue_logger_setup.setup_queue_logging(log_setup, handler_setup)
    queue_logger_setup.start()

    assert queue_logger_setup.structlog_listener._thread is not None


def test_stop_queue_logger(queue_logger_setup, log_setup, handler_setup):
    # queue_logger_setup.setup_queue_logging(log_setup, handler_setup)
    queue_logger_setup.start()
    queue_logger_setup.stop()

    assert queue_logger_setup.structlog_listener._thread is None
