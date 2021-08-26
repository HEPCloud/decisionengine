"""
Global Logger config dictionary used by all loggers (in their own subkeys)
"""
import structlog

userformat = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")

pre_chain = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    timestamper,
]


# this dictionary is a shared singleton used as
# a global store of the runtime logger's settings.
pylogconfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
            # "foreign_pre_chain": pre_chain,
            "format": userformat,
        },
        "for_JSON": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=False),
            "format": "%(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "plain",
        },
        # "file_all_debug": {
        #                   "level": "DEBUG",
        #                   "class": "logging.handlers.RotatingFileHandler",
        #                   "filename": "/var/log/decisionengine/all_debug.log",
        #                   "maxBytes": 200*1000000,
        #                   "backupCount": 2,
        #                   "formatter": "plain",
        # },
        "de_file_debug": {
            "level": "DEBUG",
            "formatter": "plain",
        },
        "de_file_info": {
            "level": "INFO",
            "formatter": "plain",
        },
        "file_structlog_debug": {
            "level": "DEBUG",
            "formatter": "for_JSON",
        },
    },
    "loggers": {
        "default": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True,
        },
        "decisionengine": {
            "handlers": ["file_structlog_debug", "de_file_debug", "de_file_info"],
            "level": "DEBUG",
            "propagate": True,
        },
        # "": {#this gives me ALL logging at handler level into handler file
        #   "handlers": ["file_all_debug"],
        #   "propagate": True,
        # },
    },
}

structlog.configure(
    processors=pre_chain
    + [
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(sort_keys=True),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
