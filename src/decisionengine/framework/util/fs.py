# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os

from pathlib import Path

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


def files_with_extensions(dir_path, *extensions):
    """
    Return all files in dir_path that match the provided extensions.

    If no extensions are given, then all files in dir_path are returned.

    Results are sorted by channel name to ensure stable output.
    """
    logger.debug(f"dir_path is {dir_path}!")

    if len(extensions) == 0:
        extensions = ""
        logger.info("file extensions have zero length")

    name_to_path = []

    try:
        for entry in Path(dir_path).iterdir():
            if not entry.is_file():
                continue
            if entry.name.endswith(extensions):
                channel_name = os.path.splitext(entry.name)[0]
                name_to_path.append([channel_name, str(entry)])
    except FileNotFoundError:
        logger.exception("invalid path to config file given")
        raise
    except Exception:  # pragma: no cover
        logger.exception("Unexpected error!")
        raise
    else:
        return tuple(sorted(name_to_path, key=lambda x: x[0]))
