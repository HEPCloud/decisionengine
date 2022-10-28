# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pprint
import sys

import structlog

import decisionengine.framework.modules.logging_configDict as logconf

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.modules import describe as _describe
from decisionengine.framework.modules.describe import Parameter, supports_config
from decisionengine.framework.modules.Module import Module, produces

__all__ = ["Parameter", "Source", "describe", "produces", "supports_config"]


class Source(Module):
    _produces = {}

    def __init__(self, set_of_parameters):
        super().__init__(set_of_parameters)

        self.logger = structlog.getLogger(logconf.SOURCELOGGERNAME)

    # acquire: The action function for a source. Will
    # retrieve data from external sources and issue a
    # DataBlock "put" transaction.
    def acquire(self):
        print("Called Source.acquires")


# ===============================================================
# Override standard module program options
def _find_one_config(config_filename, module_spec):
    full_config = ValidConfig(config_filename)
    sources = full_config.get("sources")
    if sources is None:
        sys.exit(f"Could not locate 'sources' configuration block in {config_filename}.")

    found_configs = {k: v for k, v in sources.items() if v.get("module") == module_spec}
    if len(found_configs) == 0:
        sys.exit(f"No configuration in {config_filename} is supported by {module_spec}.")
    if len(found_configs) > 1:
        sys.exit(
            f"Located more than one configuration supported by {module_spec}.\n"
            f"Please choose one of {list(found_configs.keys())}."
        )

    full_module_config = list(found_configs.items())[0]
    parameters = full_module_config[1].get("parameters")
    if parameters is None:
        sys.exit(
            f"Configuration for '{full_module_config[0]}' source in {config_filename}"
            " does not contain a 'parameters' table."
        )
    return parameters


def describe(cls, sample_config=None):
    class SourceProgramOptions(_describe.ModuleProgramOptions):
        def __init__(self, module_spec, cls):
            super().__init__(module_spec, cls)
            self._parser.add_argument(
                "-c",
                "--acquire-with-config",
                metavar="<channel config. file>",
                help="run the 'acquire' method of the source as configured in the 'sources'"
                " block of the full channel configuration",
            )
            if sample_config is not None:
                self._parser.add_argument(
                    "-s",
                    "--acquire-with-sample-config",
                    action="store_true",
                    help="run the 'acquire' method using the default configuration provided " "by the module",
                )

        def process_args(self):
            args = super().process_args()
            config = None
            if args.acquire_with_config:
                config = _find_one_config(args.acquire_with_config, self._module_spec)
                print(f"Running acquire for source {cls.__name__} using configuration from {args.acquire_with_config}:")
            if sample_config is not None and args.acquire_with_sample_config:
                config = sample_config
                print(f"Running acquire for source {cls.__name__} using default configuration:")
            if config is not None:
                print()
                pprint.pprint(config)
                print("\nProduced products:\n")
                print(cls(config).acquire())

    return _describe.main_wrapper(cls, SourceProgramOptions)
