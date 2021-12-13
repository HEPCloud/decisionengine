# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import multiprocessing

from logging.handlers import QueueHandler, QueueListener


class QueueLogger:
    def __init__(self):
        self.structlog_q = None
        self.structlog_q_handler = None
        self.structlog_listener = None
        self.initialized = False

    def initialize_q(self):
        self.structlog_q = multiprocessing.Queue(-1)
        self.structlog_q_handler = QueueHandler(self.structlog_q)
        self.initialized = True

    def format_logger(self, logger):
        logger.addHandler(self.structlog_q_handler)

    def configure_listener(self, handlers):
        self.structlog_listener = QueueListener(self.structlog_q, *handlers, respect_handler_level=True)

    def setup_queue_logging(self, logger, handlers):
        self.initialize_q()
        self.format_logger(logger)
        self.configure_listener(handlers)

    def start(self):
        self.structlog_listener.start()

    def stop(self):
        if self.initialized:
            self.structlog_listener.stop()
