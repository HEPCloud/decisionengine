#!/usr/bin/env python

import argparse
import xmlrpclib
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
        "--status",
        action='store_true',
        help="print status server")

    args = parser.parse_args()

    con_string = "http://{}:{}".format(args.host,args.port)
    s = xmlrpclib.ServerProxy(con_string)

    if args.status:
        print s.status()

    if args.stop_channel:
        print s.stop_channel(args.stop_channel)


    if args.start_channel:
        print s.start_channel(args.start_channel)

    if args.stop_channels:
        print s.stop_channels()

    if args.start_channels:
        print s.start_channels()

    if args.show_config:
        conf = s.show_config()
        pprint.pprint(conf)

    if args.stop:
        s.stop()
