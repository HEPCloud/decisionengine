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


def _config_from_file(config_file):
    if os.path.getsize(config_file) == 0:
        raise RuntimeError(f"Empty configuration file {config_file}")

    config_str = None
    basename, ext = os.path.splitext(config_file)
    config_str = _jsonnet.evaluate_file(str(config_file))
    if ext != ".jsonnet":
        print(f"Please rename '{config_file}' to '{basename}.jsonnet'.", file=sys.stderr)
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
