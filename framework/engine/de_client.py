#!/usr/bin/env python3

import argparse
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
import pprint

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--port",
        default="8888",
        help="server port(8888)")

    parser.add_argument(
        "--stop-channel",
        help="channel name")

    parser.add_argument(
        "--stop-channels",
        action='store_true',
        help="stop all channels")

    parser.add_argument(
        "--start-channels",
        action='store_true',
        help="start all channels")

    parser.add_argument(
        "--start-channel",
        help="channel name")


    parser.add_argument(
        "--host",
        default="localhost",
        help="host name (localhost)")

    parser.add_argument(
        "--stop",
        action='store_true',
        help="stop server")

    parser.add_argument(
        "--show-config",
        action='store_true',
        help="print configuration")

    parser.add_argument(
        "--reload-config",
        action="store_true",
        help="reload configuration")

    parser.add_argument(
        "--status",
        action='store_true',
        help="print status server")

    parser.add_argument(
        "--print-product",
        help="product name")

    parser.add_argument(
        "--print-products",
        action='store_true',
        help="print products")

    parser.add_argument(
        "--query",
        help="panda query, e.g. \" FigureOfMerit != inf \"")

    parser.add_argument(
        "--columns",
        help="comma separated list of columns")

    parser.add_argument(
        "--channel-log-level",
        nargs=2,
        help="<channel name> log_level, e.g. <channel name> INFO ")

    parser.add_argument(
        "--reaper-start",
        action='store_true',
        help="start the database cleanup process")

    parser.add_argument(
        "--reaper-start-delay-secs",
        default="0",
        type=int,
        help="Delay the database cleanup process start")

    parser.add_argument(
        "--reaper-stop",
        action='store_true',
        help="stop the database cleanup process")

    parser.add_argument(
        "--reaper-status",
        action='store_true',
        help="show the database cleanup process status")

    args = parser.parse_args()

    con_string = "http://{}:{}".format(args.host, args.port)
    s = xmlrpclib.ServerProxy(con_string, allow_none=True)

    if args.status:
        print(s.status())

    if args.stop_channel:
        print(s.stop_channel(args.stop_channel))

    if args.start_channel:
        print(s.start_channel(args.start_channel))

    if args.stop_channels:
        print(s.stop_channels())

    if args.start_channels:
        print(s.start_channels())

    if args.channel_log_level:
      print(s.set_channel_log_level(args.channel_log_level[0],args.channel_log_level[1]))

    if args.show_config:
        conf = s.show_config()
        pprint.pprint(conf)

    if args.reload_config:
        print(s.reload_config())

    if args.print_products:
        print(s.print_products())

    if args.print_product:
        print(s.print_product(args.print_product,
                              args.columns,
                              args.query))

    if args.stop:
        s.stop()

    if args.reaper_stop:
        print(s.reaper_stop())

    if args.reaper_start:
        print(s.reaper_start(args.reaper_start_delay_secs))

    if args.reaper_status:
        print(s.reaper_status())
