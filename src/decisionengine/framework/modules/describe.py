# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import argparse

from decisionengine.framework.modules.print_description import (
    print_consumes,
    print_produces,
    print_supported_config,
    spec_if_main,
)


# =============================================================================
# Configuration description
def _par_type(par_type, default_value):
    if par_type is None:
        # Take type of 'default' argument if type is not provided.
        if default_value is not None:
            return default_value.__class__
        return None
    return par_type


def _par_default(par_type, default_value):
    if default_value is None:
        return None
    # If we get this far, par_type has either been specified or is
    # inferred by the type of the default value.
    assert par_type is not None
    # Specified par_type always wins if it is non-null
    return par_type(default_value)


class Parameter:
    def __init__(self, name, type=None, default=None, comment=None):
        self.name = name
        self.my_type = _par_type(type, default)
        try:
            self.default = _par_default(self.my_type, default)
        except Exception:
            raise RuntimeError(
                f"An error occurred while processing the parameter '{name}':\n"
                + f"The specified type '{self.my_type.__name__}' conflicts with the type "
                + f"of the default value '{default}' (type '{default.__class__.__name__}')"
            )
        self.comment = comment


def supports_config(*args):
    supported_config = {par.name: (par.my_type, par.default, par.comment) for par in args}

    def decorator(cls):
        # @supports_config may be called from the base class and any
        # subclasses--hence why we update the the dictionary and not
        # create it afresh for each call.
        config = getattr(cls, "_supported_config", {})
        config.update(supported_config)
        cls._supported_config = config
        return cls

    return decorator


class ModuleProgramOptions:
    def __init__(self, module_spec, cls):
        self._module_spec = module_spec
        self._cls = cls
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument(
            "--describe",
            action="store_true",
            help="print config. template along with produces and consumes information",
        )
        self._parser.add_argument(
            "--config-template", action="store_true", help="print the expected module configuration"
        )
        self.invoked = False

    def process_args(self):
        args = self._parser.parse_args()
        if args.describe:
            print_consumes(self._cls)
            print_produces(self._cls)
            print_supported_config(self._module_spec, self._cls)
        elif args.config_template:
            print_supported_config(self._module_spec, self._cls)
        return args


def main_wrapper(cls, program_options=ModuleProgramOptions):
    module_spec = spec_if_main(cls)
    if not module_spec:
        return

    parser = program_options(module_spec, cls)
    parser.process_args()
