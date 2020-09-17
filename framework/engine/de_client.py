#!/usr/bin/env python3

import argparse
import xmlrpc.client

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port",
        metavar='<port number>',
        default="8888",
        help="Default port is 8888")
    parser.add_argument(
        "--host",
        metavar='<hostname>',
        default="localhost",
        help="Default hostname is 'localhost'")
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Include exception message in printout if server is inaccessible")


    server = parser.add_argument_group("Decision Engine server options")
    server.add_argument(
        "--stop",
        action='store_true',
        help="stop server")
    server.add_argument(
        "--status",
        action='store_true',
        help="print server status")
    server.add_argument(
        "--show-de-config",
        action='store_true',
        help="print server configuration")
    server.add_argument(
        "--reload-config",
        action="store_true",
        help="reload configuration")
    server.add_argument(
        "--print-engine-loglevel",
        action='store_true',
        help="print engine log level")

    channels = parser.add_argument_group("Channel-specific options")
    channels.add_argument(
        "--start-channels",
        action='store_true',
        help="start all channels")
    channels.add_argument(
        "--stop-channels",
        action='store_true',
        help="stop all channels")
    channels.add_argument(
        "--start-channel",
        metavar="<channel name>")
    channels.add_argument(
        "--stop-channel",
        metavar="<channel name>")
    channels.add_argument(
        "--show-config",
        action='store_true',
        help="print configuration")
    channels.add_argument(
        "--show-channel-config",
        metavar="<channel name>",
        help="print channel configuration")
    channels.add_argument(
        "--get-channel-loglevel",
        metavar='<channel name>',
        help="print channel log level")
    channels.add_argument(
        "--set-channel-loglevel",
        nargs=2,
        metavar=('<channel name>', '<log level>'),
        help="Possible levels are NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL")

    products = parser.add_argument_group('Product-specific options')
    products.add_argument(
        "--print-product",
        metavar="<product name>")
    products.add_argument(
        "--print-products",
        action='store_true',
        help="print products")
    products.add_argument(
        "--columns",
        help="comma separated list of columns")
    products.add_argument(
        "--query",
        help="panda query, e.g. \"FigureOfMerit != infs\"")

    reaper = parser.add_argument_group("Database reaper options")
    reaper.add_argument(
        "--reaper-start",
        action='store_true',
        help="start the database cleanup process")
    reaper.add_argument(
        "--reaper-start-delay-secs",
        metavar='<number of seconds>',
        default="0",
        type=int,
        help="Delay the database cleanup process start time by the specified number of seconds.")
    reaper.add_argument(
        "--reaper-stop",
        action='store_true',
        help="stop the database cleanup process")
    reaper.add_argument(
        "--reaper-status",
        action='store_true',
        help="show the database cleanup process status")

    return parser

def execute_command_from_args(argsparsed, de_socket):
    '''argsparsed should be from create_parser in this file'''

    # Server-specific options
    if argsparsed.status:
        return de_socket.status()
    if argsparsed.show_de_config:
        return de_socket.show_de_config()
    if argsparsed.reload_config:
        return de_socket.reload_config()
    if argsparsed.stop:
        return de_socket.stop()
    if argsparsed.print_engine_loglevel:
        return de_socket.get_log_level()

    # Channel-specific options
    if argsparsed.stop_channel:
        return de_socket.stop_channel(argsparsed.stop_channel)
    if argsparsed.start_channel:
        return de_socket.start_channel(argsparsed.start_channel)
    if argsparsed.stop_channels:
        return de_socket.stop_channels()
    if argsparsed.start_channels:
        return de_socket.start_channels()
    if argsparsed.get_channel_loglevel:
        level = argsparsed.get_channel_loglevel
        if level == "UNITTEST":
            return "NOTSET"
        else:
            return de_socket.get_channel_log_level(argsparsed.get_channel_loglevel)
    if argsparsed.set_channel_loglevel:
        return de_socket.set_channel_log_level(argsparsed.set_channel_loglevel[0],
                                               argsparsed.set_channel_loglevel[1])
    if argsparsed.show_config:
        return de_socket.show_config("all")
    if argsparsed.show_channel_config:
        return de_socket.show_config(argsparsed.show_channel_config)

    # Product-specific options
    if argsparsed.print_products:
        return de_socket.print_products()
    if argsparsed.print_product:
        return de_socket.print_product(argsparsed.print_product,
                                       argsparsed.columns,
                                       argsparsed.query)

    # Database-reaper options
    if argsparsed.reaper_stop:
        return de_socket.reaper_stop()
    if argsparsed.reaper_start:
        return de_socket.reaper_start(argsparsed.reaper_start_delay_secs)
    if argsparsed.reaper_status:
        return de_socket.reaper_status()

def main(args_to_parse=None):
    '''If you pass a list of args, they will be used instead of sys.argv'''

    parser = create_parser()
    args = parser.parse_args(args_to_parse)
    url = f"http://{args.host}:{args.port}"
    de_socket = xmlrpc.client.ServerProxy(url, allow_none=True)
    try:
        return execute_command_from_args(args, de_socket)
    except Exception as e:
        msg = f"An error occurred while trying to access a DE server at '{url}'\n" + \
            "Please ensure that the host and port names correspond to a running DE instance."
        if args.verbose:
            msg += f'\n{e}'
        return msg


if __name__ == "__main__":
    print(main())
