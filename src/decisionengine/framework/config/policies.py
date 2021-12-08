# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Decision-engine default configuration policies.

For the decision-engine process, the configuration policies are:

- The global configuration file must be named 'decision_engine.jsonnet'
  and it must reside in (a) a directory that can be accessed through
  the 'CONFIG_PATH' environment variable, or (b) the /etc/decisionengine
  directory.

- All channel configurations must reside in (a) a directory accessible
  through the 'CHANNEL_CONFIG_PATH' environment variable, or (b) a
  'config.d' subdirectory of the /etc/decisionengine directory.

The utilities provided in this module provide simple means of
accessing the configuration artifacts according to the policies listed
above.  Please consult the documentation for each function below for
more detailed information.
"""

import os
import pathlib

GLOBAL_CONFIG_FILENAME = "decision_engine.jsonnet"


def valid_dir(path, scope):
    """
    Throws if the supplied path object is not a directory, otherwise returns the path object.
    """
    if not path.is_dir():
        raise RuntimeError(f"{scope} configuration directory '{path}' not found")
    return path


def global_config_dir():
    """
    Retrieve global configuration dir as pathlib.Path object.

    This is the directory that houses the 'decision_engine.jsonnet'
    global configuration file.

    This function checks that the 'CONFIG_PATH' variable has been set
    or will use /etc/decisionengine otherwise.  If the path exists as
    a directory, then the directory path is returned as a string;
    otherwise an exception is raised.
    """
    global_config_dir = pathlib.Path(os.getenv("CONFIG_PATH", "/etc/decisionengine"))
    return valid_dir(global_config_dir, "Global")


def channel_config_dir(parent_dir=None):
    """
    Retrieve the channel configuration directory as a pathlib.Path object.

    This function returns a path object according to the following
    precedence rules:

    1. If the 'parent_dir' argument is provided, the returned path
       object will correspond to '{parent_dir}/config.d'.
    2. If the 'CHANNEL_CONFIG_PATH' environment variable has been set,
       the returned path object will correspond to
       ${CHANNEL_CONFIG_PATH}.
    3. If neither 1 or 2 apply, the returned path object corresponds
       to '{global_config_dir()}/config.d' (see documentation for
       'global_config_dir()').

    Regardless of the precedence rule used, the returned path object
    must be a valid directory or an exception will be raised--i.e. if
    the 'parent_dir' argument is supplied, and the resulting path
    object is not a valid directory, the function will exit with an
    exception and not attempt rule 2 or 3.
    """
    if parent_dir:
        channel_config_dir = pathlib.Path(parent_dir, "config.d")
        return valid_dir(channel_config_dir, "Channel")

    env_value = os.getenv("CHANNEL_CONFIG_PATH")
    if env_value:
        channel_config_dir = pathlib.Path(env_value)
        return valid_dir(channel_config_dir, "Channel")

    channel_config_dir = global_config_dir().joinpath("config.d")
    return valid_dir(channel_config_dir, "Channel")


def global_config_file(parent_dir=None):
    """
    Return the pathlib.Path object corresponding to the global configuration.

    If supplied, the 'parent_dir' is assumed to be the full path
    corresponding to a directory containing the
    'decision_engine.jsonnet' file.  If not provided, the global
    configuration directory is determined based on the behavior of the
    'global_config_dir()' function.

    An exception is raised if no 'decision_engine.jsonnet' file is found.
    """
    if parent_dir:
        path = pathlib.Path(parent_dir, GLOBAL_CONFIG_FILENAME)
    else:
        path = global_config_dir().joinpath(GLOBAL_CONFIG_FILENAME)
    if not path.is_file():
        raise RuntimeError(f"Global configuration file '{path}' not found")
    return path
