import multiprocessing

from logging.handlers import QueueHandler, QueueListener


class QueueLogger:
    def __init__(self):
        self.structlog_q = multiprocessing.Queue(-1)
        self.structlog_q_handler = QueueHandler(self.structlog_q)
        self.structlog_listener = None

    def format_logger(self, logger):
        logger.addHandler(self.structlog_q_handler)

    def configure_listener(self, handlers):
        self.structlog_listener = QueueListener(self.structlog_q, *handlers, respect_handler_level=True)

    def setup_queue_logging(self, logger, handlers):
        self.format_logger(logger)
        self.configure_listener(handlers)

    def start(self):
        self.structlog_listener.start()

    def stop(self):
        if self.structlog_listener is not None:
            self.structlog_listener.stop()
