'''
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
'''

import os

GLOBAL_CONFIG_FILENAME = 'decision_engine.jsonnet'

def global_config_dir():
    '''
    Retrieve global configuration dir as string.

    This is the directory that houses the 'decision_engine.jsonnet'
    global configuration file.

    This function checks that the 'CONFIG_PATH' variable has been set
    or will use /etc/decisionengine otherwise.  If the path exists as
    a directory, then the directory path is returned as a string;
    otherwise an exception is raised.
    '''
    global_config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
    if not os.path.isdir(global_config_dir):
        raise Exception(f"Config dir '{global_config_dir}' not found")
    return global_config_dir

def channel_config_dir(parent_dir=None):
    '''
    Retrieve the channel configuration directory as a string.

    This directory contains all channel configuration files.  This function assumes that
    the directory can be accessed by using the 'CHANNEL_CONFIG_PATH' environment variable.
    If that variable has not been set, then the value of 'parent_dir' is prepended to
    'config.d', which is then assumed to be the full path to the channel-configuration
    directory.

    If the 'parent_dir' argument is not provided, the global configuration directory is
    used as the parent (see documentation for 'global_config_dir()').

    If the final path for the channel configuration directory does not
    correspond to a directory, an exception is raised.
    '''
    if parent_dir is None:
        parent_dir = global_config_dir()
    channel_config_dir = os.getenv("CHANNEL_CONFIG_PATH",
                                   os.path.join(parent_dir, "config.d"))
    if not os.path.isdir(channel_config_dir):
        raise Exception(f"Channel config dir '{channel_config_dir}' not found")

    return channel_config_dir

def global_config_file(global_config_dir=None):
    '''
    Retrieve the path (as a string) corresponding to the global configuration.

    If supplied, the 'global_config_dir' is assumed to be the full path
    corresponding to a directory containing the 'decision_engine.jsonnet'
    file.   If not provided, the global configuration directory is determined
    based on the behavior of the 'global_config_dir()' function.

    An exception is raised if no 'decision_engine.jsonnet' file is found.
    '''
    if global_config_dir is None:
        global_config_dir = global_config_dir()
    config_file = os.path.join(global_config_dir, GLOBAL_CONFIG_FILENAME)
    if not os.path.isfile(config_file):
        raise Exception(f"Config file '{config_file}' not found")
    return config_file
