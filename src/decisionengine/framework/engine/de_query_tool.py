#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import argparse
import xmlrpc.client

from functools import partial

from decisionengine.framework.engine.ClientMessageReceiver import ClientMessageReceiver


def create_parser():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("--format", metavar="<format>", help="Possible formats are 'csv', 'json'.")
    optional.add_argument(
        "--since",
        metavar="<time>",
        help="Minimum start time for task managers. "
        "If omitted, searches only the current task manager.\n"
        "(e.g. 2021-03-21 11:00:00)",
    )
    optional.add_argument("--port", metavar="<port number>", default="8888", help="Default port is 8888")
    optional.add_argument("--host", metavar="<hostname>", default="localhost", help="Default hostname is 'localhost'")
    optional.add_argument(
        "-v", "--verbose", action="store_true", help="Include exception message in printout if server is inaccessible"
    )

    positional = parser.add_argument_group("positional arguments")
    positional.add_argument("product", metavar="<product>", help="product to query")

    return parser


def command_for_args(argsparsed, de_socket):
    """Calls the proper function for the arguments passed to de_query_tool.

    Args:
        argsparsed (Namespace): Should be from create_parser in this file.
        de_socket (ServerProxy): RPC Server Proxy.

    Returns:
        str: Output of the command.
    """

    return partial(de_socket.query_tool, argsparsed.product, argsparsed.format, argsparsed.since)


def main(args_to_parse=None, logger_name="de_query_tool"):
    """Main function for de_query_tool

    Args:
        args_to_parse (list, optional): If you pass a list of args, they will be used instead of sys.argv. Defaults to None.

    Returns:
        str: Query result
    """

    parser = create_parser()
    args = parser.parse_args(args_to_parse)
    url = f"http://{args.host}:{args.port}"
    de_socket = xmlrpc.client.ServerProxy(url, allow_none=True)
    try:
        receiver = ClientMessageReceiver(*de_socket.kombu_info(), "de_query_tool", logger_name)
        return receiver.execute(command_for_args(args, de_socket))
    except OSError as e:
        msg = (
            f"An error occurred while trying to access a DE server at '{url}'\n"
            + "Please ensure that the host and port names correspond to a running DE instance."
        )
        if args.verbose:
            msg += f"\n{e}"
        return msg
    except Exception as e:  # pragma: no cover
        msg = f"An error occurred while trying to access a DE server at '{url}'."
        if args.verbose:
            msg += f"\n{e}"
        return msg


def console_scripts_main(args_to_parse=None):
    """
    This is the entry point for the setuptools auto generated scripts.
    Setuptools thinks a return from this function is an error message.
    """
    msg = main(args_to_parse)
    if msg is None or isinstance(msg, int):
        return msg
    if isinstance(msg, str) and msg.startswith("An error occurred while trying to access a DE server at"):
        return msg
    print(msg)


if __name__ == "__main__":
    console_scripts_main()
