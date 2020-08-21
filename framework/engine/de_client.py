#!/usr/bin/env python3

import argparse
import xmlrpc.client
import pprint

def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--port",
        metavar='<port number>',
        default="8888",
        help="Default port is 8888")

    parser.add_argument(
        "--start-channels",
        action='store_true',
        help="start all channels")

    parser.add_argument(
        "--stop-channels",
        action='store_true',
        help="stop all channels")

    parser.add_argument(
        "--start-channel",
        metavar="<channel name>")

    parser.add_argument(
        "--stop-channel",
        metavar="<channel name>")

    parser.add_argument(
        "--host",
        metavar='<hostname>',
        default="localhost",
        help="Default hostname is 'localhost'")

    parser.add_argument(
        "--stop",
        action='store_true',
        help="stop server")

    parser.add_argument(
        "--show-config",
        action='store_true',
        help="print configuration")

    parser.add_argument(
        "--show-channel-config",
        metavar="<channel name>",
        help="print channel configuration")

    parser.add_argument(
        "--show-de-config",
        action='store_true',
        help="print Decision Engine configuration")

    parser.add_argument(
        "--reload-config",
        action="store_true",
        help="reload configuration")

    parser.add_argument(
        "--status",
        action='store_true',
        help="print server status")

    parser.add_argument(
        "--print-product",
        metavar="<product name>")

    parser.add_argument(
        "--print-products",
        action='store_true',
        help="print products")

    parser.add_argument(
        "--query",
        help="panda query, e.g. \"FigureOfMerit != infs\"")

    parser.add_argument(
        "--columns",
        help="comma separated list of columns")

    parser.add_argument(
        "--print-engine-loglevel",
        action='store_true',
        help="print engine log level")

    parser.add_argument(
        "--get-channel-loglevel",
        metavar='<channel name>',
        help="print channel log level")

    parser.add_argument(
        "--set-channel-loglevel",
        nargs=2,
        metavar=('<channel name>', '<log level>'),
        help="Possible levels are NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL")

    parser.add_argument(
        "--reaper-start",
        action='store_true',
        help="start the database cleanup process")

    parser.add_argument(
        "--reaper-start-delay-secs",
        metavar='<number of seconds>',
        default="0",
        type=int,
        help="Delay the database cleanup process start time by the specified number of seconds.")

    parser.add_argument(
        "--reaper-stop",
        action='store_true',
        help="stop the database cleanup process")

    parser.add_argument(
        "--reaper-status",
        action='store_true',
        help="show the database cleanup process status")

    return parser

def build_xmlrpc_connection(host, port):
    return xmlrpc.client.ServerProxy(f"http://{host}:{port}", allow_none=True)

def execute_command_from_args(argsparsed, xmlrpcsocket):
    '''argsparsed should be from create_parser in this file'''

    if argsparsed.status:
        return xmlrpcsocket.status()

    if argsparsed.stop_channel:
        return xmlrpcsocket.stop_channel(argsparsed.stop_channel)

    if argsparsed.start_channel:
        return xmlrpcsocket.start_channel(argsparsed.start_channel)

    if argsparsed.stop_channels:
        return xmlrpcsocket.stop_channels()

    if argsparsed.start_channels:
        return xmlrpcsocket.start_channels()

    if argsparsed.print_engine_loglevel:
        return xmlrpcsocket.get_log_level()

    if argsparsed.get_channel_loglevel:
        level = argsparsed.get_channel_loglevel
        if level == "UNITTEST":
            return "NOTSET"
        else:
            return xmlrpcsocket.get_channel_log_level(argsparsed.get_channel_loglevel)

    if argsparsed.set_channel_loglevel:
        return xmlrpcsocket.set_channel_log_level(argsparsed.set_channel_loglevel[0], argsparsed.set_channel_loglevel[1])

    if argsparsed.show_config:
        return pprint.pformat(xmlrpcsocket.show_config("all"))

    if argsparsed.show_channel_config:
        channel = argsparsed.show_channel_config
        return pprint.pformat(xmlrpcsocket.show_config(channel))

    if argsparsed.show_de_config:
        return xmlrpcsocket.show_de_config()

    if argsparsed.reload_config:
        return xmlrpcsocket.reload_config()

    if argsparsed.print_products:
        return xmlrpcsocket.print_products()

    if argsparsed.print_product:
        return xmlrpcsocket.print_product(argsparsed.print_product,
                                          argsparsed.columns,
                                          argsparsed.query)

    if argsparsed.stop:
        return xmlrpcsocket.stop()

    if argsparsed.reaper_stop:
        return xmlrpcsocket.reaper_stop()

    if argsparsed.reaper_start:
        return xmlrpcsocket.reaper_start(argsparsed.reaper_start_delay_secs)

    if argsparsed.reaper_status:
        return xmlrpcsocket.reaper_status()

def main(args_to_parse=None):
    '''If you pass a list of args, they will be used instead of sys.argv'''

    parser = create_parser()
    args = parser.parse_args(args_to_parse)
    socket = build_xmlrpc_connection(args.host, args.port)
    return execute_command_from_args(args, socket)


if __name__ == "__main__":
    print(main())
