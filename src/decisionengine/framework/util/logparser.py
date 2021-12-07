#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import argparse
import fileinput
import json
import os


def create_parser():
    parser = argparse.ArgumentParser(
        description="Simple log file parser to filter the records and print only part of them."
    )
    # need to use the default group, otherwise --help is in a separate group by itself
    parser.add_argument(
        "-f",
        "--fields",
        metavar="<fields>",
        default="",
        help="comma separated list of field numbers to select in the structured log message. Start from 0",
    )
    parser.add_argument(
        "-k",
        "--keys",
        metavar="<keys>",
        default="",
        help="comma separated list of keys to select in the structured log message",
    )
    parser.add_argument(
        "-i",
        "--input_separator",
        metavar="<input separator>",
        default=" - ",
        help="input separator. Defaults to ' - '.",
    )
    parser.add_argument(
        "-s", "--separator", metavar="<separator>", default=",", help="output separator. Defaults to comma, ','"
    )
    parser.add_argument(
        "-c",
        "--constraint",
        metavar="<constraint>",
        action="append",
        help="line selection constraint. Repeat the option for multiple constraints. Format: '(field # | key) value'."
        " Integers are always considered field numbers.",
    )
    parser.add_argument(
        "-l",
        "--loglevel",
        metavar="<loglevel>",
        action="store",
        help="add constraint for log level. Same as '-c 3 <loglevel>'",
    )
    parser.add_argument(
        "-e",
        "--logdirectory",
        metavar="<logdirectory>",
        action="store",
        default="/var/log/decisionengine",
        help="log files directory. Default is '/var/log/decisionengine'",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Include exception messages")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug, e.g. to use for unit test")
    positional = parser.add_argument_group("positional arguments")
    positional.add_argument(
        "logfile",
        metavar="<logfile>",
        nargs="?",
        help="log file to parse. File names without directory are searched also in the default log files directory."
        " Using stdin if '-' or if none is provided",
    )

    return parser


def parse_constraints(constraints, loglevel=None):
    """Parse and combine the constraints

    Args:
        constraints (list|None): List of constraints
        loglevel (str): Logging level, e.g. DEBUG, INFO, ...

    Returns:
        dict: combined constraint dictionary

    """
    if not constraints and not loglevel:
        return None
    constraint = {"fields": [], "keys": []}
    if loglevel:
        # The log level is the 4th field in each log line
        constraint["fields"].append((3, loglevel))
    if constraints:
        for c in constraints:
            i, v = c.split(maxsplit=1)
            try:
                constraint["fields"].append((int(i), v))
            except ValueError:
                # TODO: add also time constraints: before, after, ...
                constraint["keys"].append((i, v))
    return constraint


def matches_constraint(constraint, linelist, linedict):
    """Return True if all constraints are marched

    Args:
        constraint (dict|None): combined constraints
        linelist (list): List of line fields
        linedict (dict): Dictionary with structured elements

    Returns:
        bool: True is all constraints are matched, False otherwise

    """
    if constraint is None:
        return True
    # if constraint is not None, it will always have "fields" and "keys"
    if constraint["fields"]:
        try:
            if not all(linelist[i] == v for i, v in constraint["fields"]):
                return False
        except IndexError:
            # In case records have variable number of fields (change in the log format)
            return False
    if constraint["keys"]:
        try:
            if not all(linedict[k] == v for k, v in constraint["keys"]):
                return False
        except KeyError:
            # Some records may have keys not present in others. Only positive matches are True
            return False
    return True


def execute_command_from_args(argsparsed, logfile=None, constraint=None):
    """Parse the log file as requested.

    Args:
        argsparsed (Namespace): Parsed arguments from create_parser in this file.
        logfile (path): Log file path.
        constraint (dict): Combined constraints dictionary

    Returns:
        str: Output of the command.
    """

    outlines = []
    fields = []
    keys = []
    if argsparsed.fields:
        fields = [int(i) for i in argsparsed.fields.split(",")]
    if argsparsed.keys:
        keys = argsparsed.keys.split(",")
    if not fields and not keys:
        raise ValueError("No field or key specified")

    # If you would call fileinput.input() without files it would try to process all arguments.
    # We pass '-' as only file when argparse got no files which will cause fileinput to read from stdin
    with fileinput.input(files=(logfile,) if logfile else ("-",)) as f:
        for full_line in f:
            line = full_line.strip()
            if not line:
                # Skip empty lines
                continue
            linelist = line.split(argsparsed.input_separator)
            if linelist[-1][0] == "{":
                linedict = json.loads(linelist[-1])
            else:
                linedict = {}
            if not matches_constraint(constraint, linelist, linedict):
                continue
            outline = ""
            # Guaranteed to have at least one field or key
            # IndexError and KeyError needed to cover irregular lines
            for i in fields:
                try:
                    outline += f"{argsparsed.separator}{linelist[i]}"
                except IndexError:
                    outline += f"{argsparsed.separator}NOT_AVAILABLE"
            for k in keys:
                try:
                    outline += f"{argsparsed.separator}{linedict[k]}"
                except KeyError:
                    outline += f"{argsparsed.separator}NOT_AVAILABLE"
            print(outline[len(argsparsed.separator) :])
            if argsparsed.debug:
                outlines.append(outline[len(argsparsed.separator) :])

    return "\n".join(outlines)


def main(args_to_parse=None):
    """Main function for logparser

    Args:
        args_to_parse (list, optional): If you pass a list of args, they will be used instead of sys.argv.
        Defaults to None.

    Returns:
        str: Parsing result
    """

    parser = create_parser()
    args = parser.parse_args(args_to_parse)
    logfile = args.logfile
    if (
        logfile
        and logfile != "-"
        and not os.path.exists(logfile)
        and logfile == os.path.basename(logfile)
        and os.path.exists(os.path.join(args.logdirectory, logfile))
    ):
        logfile = os.path.join(args.logdirectory, logfile)
        if args.verbose:
            print(f"Found log file in the default log directory: '{logfile}'")
    constraint = parse_constraints(args.constraint, args.loglevel)
    try:
        return execute_command_from_args(args, logfile, constraint)
    except KeyboardInterrupt:  # pragma: no cover
        # When working in a pipe from stdin must be interrupted w/ a signal
        return ""
    except ValueError as e:
        msg = (
            f"An error occurred while trying to parse '{logfile}'\n"
            + "Please ensure that you requested some fields or keys."
        )
        if args.verbose:
            msg = f" {msg}\n{e}"
        return msg
    except FileNotFoundError as e:
        msg = (
            f"An error occurred while trying to parse '{logfile}'\n"
            + "Please ensure that the log file name is correct."
        )
        if args.verbose:
            msg = f" {msg}\n{e}"
        return msg
    except Exception as e:  # pragma: no cover
        msg = f"An error occurred while trying to parse '{logfile}'."
        if args.verbose:
            msg = f" {msg}\n{e}"
        return msg


def console_scripts_main(args_to_parse=None):
    """
    This is the entry point for the setuptools auto generated scripts.
    Setuptools thinks a return from this function is an error message.
    """
    msg = main(args_to_parse)
    if "An error occurred while trying to parse" in msg:
        return msg
    # Regular output already printed line by line.
    # Returned here only for test purposes when bebug is enabled


if __name__ == "__main__":
    mmsg = console_scripts_main()
    # Checking the return value to emulate the behavior of the setuptools invoker
    if mmsg:
        if mmsg[0] == " ":
            print(mmsg[1:])
        exit(1)
