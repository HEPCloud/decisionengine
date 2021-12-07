# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
ValidConfig represents a valid JSON document.

The decision engine requires each of its configuration files to be
valid JSON.  This is achieved by either supplying a valid Jsonnet or
JSON document upfront.

Vetting of a file for JSON validity happens upon construction of a
'ValidConfig' object.  A fully constructed 'ValidConfig' object thus
corresponds to a valid JSON document.
"""

import json
import os
import sys

from collections import UserDict

import _jsonnet


def _config_from_file(config_file, jpaths=None):
    if os.path.getsize(config_file) == 0:
        raise RuntimeError(f"Empty configuration file {config_file}")

    jpathdirs = [os.path.dirname(os.path.realpath(__file__))]
    if jpaths is not None:
        jpathdirs = jpaths + jpathdirs
    basename, ext = os.path.splitext(config_file)
    config_str = _jsonnet.evaluate_file(str(config_file), jpathdir=jpathdirs)
    if ext != ".jsonnet":
        print(f"Please rename '{config_file}' to '{basename}.jsonnet'.", file=sys.stderr)
    return json.loads(config_str)


class ValidConfig(UserDict):
    """
    ValidConfig represents a valid JSON configuration in the form of a dictionary.

    In addition to the normal dictionary operations, users may call 'dump()' to print
    out in a string form the JSON configuration.
    """

    def __init__(self, filename, jpathdirs=None):
        super().__init__(_config_from_file(filename, jpathdirs))

    def dump(self):
        "Print dictionary data to a valid JSON string."
        return json.dumps(self.data, sort_keys=True, indent=2)
