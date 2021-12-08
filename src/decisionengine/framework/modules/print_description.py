# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import inspect
import pathlib
import sys

from decisionengine.framework.util.subclasses import all_subclasses


def _print_value(v):
    return f'"{v}"' if isinstance(v, str) else f"{v}"


def _print_type(type_or_value):
    typename = ""
    if type_or_value is None:
        typename = "unknown"
    else:
        typename = getattr(type_or_value, "__name__", str(type_or_value.__class__))
    return f"type '{typename}'"


def _print_comment(comment):
    lines = comment.split("\n")
    if len(lines) == 1:
        return f" - {comment}"

    result = "\n"
    for line in lines:
        result += "\n    " + line
    result += "\n"
    return result


def _spec_from_file_name(filename):
    # Has to be a better way to do this
    full_path = pathlib.Path(filename).resolve()
    par = full_path.parent
    while (par / "__init__.py").exists():
        par = par.parent
    module_spec = full_path.as_posix().replace(par.as_posix() + "/", "")
    # With Python 3.9, we can use remove(suffix|prefix)
    module_spec = module_spec.replace(".py", "")
    return module_spec.replace("/", ".")


# =============================================
def print_consumes(cls):
    if not hasattr(cls, "_consumes") or not cls._consumes:
        return

    printed_consumes = "\nThe following products are consumed:\n\n"
    for name, type in cls._consumes.items():
        printed_consumes += f" - {name} ({_print_type(type)})\n"
    print(printed_consumes)


def print_produces(cls):
    if not hasattr(cls, "_produces") or not cls._produces:
        return

    printed_produces = "\nThe following products are produced:\n\n"
    for name, type in cls._produces.items():
        printed_produces += f" - {name} ({_print_type(type)})\n"
    print(printed_produces)


def print_supported_config(module_spec, cls):
    base_class = inspect.getmro(cls)[1]
    subclasses = all_subclasses(sys.modules.get("__main__"), base_class)
    printed_string = "\nSupported channel configuration:\n\n  <module name>: {\n"
    printed_string += f"    module: '{module_spec}',\n"
    printed_string += f"    name: '{cls.__name__}',"
    if len(subclasses) == 1:
        printed_string += "  # optional - can be inferred by framework"
    printed_string += "\n    parameters: {\n"
    comments = []

    if hasattr(cls, "_supported_config"):
        for name, (type, value, comment) in cls._supported_config.items():
            printed_string += f"      {name}:"
            if value is not None:
                printed_string += " " + _print_value(value) + ",  # default value\n"
            else:
                printed_string += " <" + _print_type(type) + ">,\n"
            if value is not None or comment is not None:
                comments.append((name, type, comment))
    printed_string += "    }\n  }\n"
    if comments:
        printed_string += "\nwhere\n"
        for name, type, comment in comments:
            printed_string += f"\n  {name} ({_print_type(type)})"
            if comment:
                printed_string += _print_comment(comment)
    printed_string += "\n"
    print(printed_string)


def spec_if_main(cls):
    # This should always return 'None' unless the module in which cls
    # is defined is __main__.  Unfortunately, it's not easy to
    # determine that.
    main_module = sys.modules.get("__main__")
    assert main_module is not None

    # If cls is not available in the main module, then we're not
    # invoking the code (in which it's defined) as __main__.
    if cls.__name__ not in dir(main_module):
        return None

    # This is the case we care about.
    if cls.__module__ == "__main__":
        return _spec_from_file_name(main_module.__file__)

    # This last case happens whenever the value passed to describe is
    # a type alias:
    #
    #   MySource = another.Source
    #   Source.describe(MySource)
    #
    # In this case, the cls' module will not be '__main__' but
    # 'another.Source'.
    return cls.__module__
