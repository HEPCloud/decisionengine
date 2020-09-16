import os

DEFAULT_GLOBAL_CONFIG_FILENAME = 'decision_engine.jsonnet'

def default_global_config_dir():
    global_config_dir = os.getenv("CONFIG_PATH", "/etc/decisionengine")
    if not os.path.isdir(global_config_dir):
        raise Exception(f"Config dir '{global_config_dir}' not found")
    return global_config_dir

def default_channel_config_dir(global_config_dir=None):
    if global_config_dir is None:
        global_config_dir = default_global_config_dir()
    channel_config_dir = os.getenv("CHANNEL_CONFIG_PATH",
                                   os.path.join(global_config_dir, "config.d"))
    if not os.path.isdir(channel_config_dir):
        raise Exception(f"Channel config dir '{channel_config_dir}' not found")

    return channel_config_dir

def default_global_config_file(global_config_dir=None):
    if global_config_dir is None:
        global_config_dir = default_global_config_dir()
    config_file = os.path.join(global_config_dir, DEFAULT_GLOBAL_CONFIG_FILENAME)
    if not os.path.isfile(config_file):
        raise Exception(f"Config file '{config_file}' not found")
    return config_file
