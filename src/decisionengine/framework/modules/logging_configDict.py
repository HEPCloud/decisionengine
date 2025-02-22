# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Global Logger config dictionary used by all loggers (in their own subkeys)
"""
import logging

import structlog

LOGGERNAME = "decisionengine"
DELOGGER_CHANNEL_NAME = "engine"

# name of loggers for all channels
# note, these loggers exist in different processes, so they can have the same
# name but still be accurately accessed within that channel
# (the channel name as recorded in the logs is by default the name of the config file
# for the channel OR alternately can be set in the config file using the key "channel_name")
CHANNELLOGGERNAME = "channel"
SOURCELOGGERNAME = "source"

# name suffixes and log levels of the output files from the main logger
# the base name is given by the "log_file" config parameter in the config file
# since the channel logger also log to the structlog file, we need to index of
# that element to correctly identify it in the Workers
userformat = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"

de_outfile_info = (
    ("_debug.log", logging.DEBUG, userformat),
    (".log", logging.INFO, userformat),
    ("_structlog_debug.log", logging.DEBUG, "%(message)s"),
)

# location in de_outfile_info of structlog info
structlog_file_index = [2]

timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)

pre_chain = [
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    timestamper,
]

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
