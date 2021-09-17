"""
ValidConfig represents a valid JSON document.

The decision engine requires each of its configuration files to be
valid JSON.  This is achieved by either supplying a valid Jsonnet or
JSON document upfront, or by providing a Python dictionary that can be
trivially converted to a JSON document.

Vetting of a file for JSON validity happens upon construction of a
'ValidConfig' object.  A fully constructed 'ValidConfig' object thus
corresponds to a valid JSON document.
"""

import json
import os
import sys

from collections import UserDict

import _jsonnet


def _convert_to_json(config_file):
    """
    Attempt to convert JSON non-compliant configuration into a compliant one.

    This is a temporary facility to aid the migration of Python-based
    configurations to Jsonnet-based ones.  Python dictionaries that
    are similar in structure to JSON documents are generally trivially
    convertible.
    """
    global_config = None
    try:
        with open(config_file) as f:
            try:
                global_config = eval(f.read())
            except Exception as msg:
                raise RuntimeError(
                    f"Configuration file {config_file} contains errors:\n{msg}\n"
                    "The supplied configuration must be a valid Jsonnet/JSON document."
                )
    except Exception as msg:
        raise RuntimeError(f"Failed to read configuration file {config_file}\n{msg}")

    if not isinstance(global_config, dict):
        raise RuntimeError("The supplied configuration must be a valid Jsonnet/JSON document.")

    json_config = None
    try:
        json_config = json.dumps(global_config)
    except Exception:
        raise RuntimeError("The supplied configuration is not convertible to a Jsonnet/JSON document.")

    print(
        f"The supplied configuration file {config_file} is not a valid Jsonnet/JSON document.\n"
        "It has been converted to a valid JSON construct, but it should be fixed.",
        file=sys.stderr,
    )
    return json_config


def _config_from_file(config_file):
    if os.path.getsize(config_file) == 0:
        raise RuntimeError(f"Empty configuration file {config_file}")

    config_str = None
    basename, ext = os.path.splitext(config_file)
    try:
        config_str = _jsonnet.evaluate_file(str(config_file))
        if ext != ".jsonnet":
            print(f"Please rename '{config_file}' to '{basename}.jsonnet'.", file=sys.stderr)
    except Exception:
        # Conversion allowed only for files that do not yet have a
        # '.jsonnet' extension.
        if ext != ".jsonnet":
            config_str = _convert_to_json(config_file)
        else:
            raise

    return json.loads(config_str)


class ValidConfig(UserDict):
    """
    ValidConfig represents a valid JSON configuration in the form of a dictionary.

    In addition to the normal dictionary operations, users may call 'dump()' to print
    out in a string form the JSON configuration.
    """

    def __init__(self, filename):
        super().__init__(_config_from_file(filename))

    def dump(self):
        "Print dictionary data to a valid JSON string."
        return json.dumps(self.data, sort_keys=True, indent=2)
