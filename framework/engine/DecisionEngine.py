#!/usr/bin/env python3
"""
Main loop for Decision Engine.
The following environment variable points to decision engine configuration file:
``DECISION_ENGINE_CONFIG_FILE``
if this environment variable is not defined the ``DE-Config.py`` file from the ``../tests/etc/` directory will be used.
"""

import argparse
import importlib
import logging
import signal
import sys
import pandas as pd
import os
import tabulate
import json

import socketserver
import xmlrpc.server

from decisionengine.framework.config import ChannelConfigHandler, ValidConfig, policies
from decisionengine.framework.engine.Workers import Worker, Workers
import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.dataspace.dataspace as dataspace
import decisionengine.framework.taskmanager.ProcessingState as ProcessingState
import decisionengine.framework.taskmanager.TaskManager as TaskManager


def _channel_preamble(name):
    header = f'Channel: {name}'
    rule = '=' * len(header)
    return '\n' + rule + '\n' + header + '\n' + rule + '\n\n'


class RequestHandler(xmlrpc.server.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class DecisionEngine(socketserver.ThreadingMixIn,
                     xmlrpc.server.SimpleXMLRPCServer):

    def __init__(self, global_config, channel_config_loader, server_address):
        xmlrpc.server.SimpleXMLRPCServer.__init__(self,
                                                  server_address,
                                                  logRequests=False,
                                                  requestHandler=RequestHandler)

        self.logger = logging.getLogger("decision_engine")
        signal.signal(signal.SIGHUP, self.handle_sighup)
        self.workers = Workers()
        self.channel_config_loader = channel_config_loader
        self.global_config = global_config
        self.dataspace = dataspace.DataSpace(self.global_config)
        self.reaper = dataspace.Reaper(self.global_config)
        self.logger.info("DecisionEngine started on {}".format(server_address))

    def get_logger(self):
        return self.logger

    def _dispatch(self, method, params):
        try:
            # methods allowed to be executed by rpc have 'rpc_' pre-pended
            func = getattr(self, "rpc_" + method)
        except AttributeError:
            raise Exception(f'method "{method}" is not supported')
        return func(*params)

    def block_until(self, state):
        with self.workers.unguarded_access() as workers:
            if not workers:
                self.logger.info('No active channels.')
            for tm in workers.values():
                if tm.is_alive():
                    tm.wait_until(state)

    def block_while(self, state):
        with self.workers.unguarded_access() as workers:
            if not workers:
                self.logger.info('No active channels.')
            for tm in workers.values():
                if tm.is_alive():
                    tm.wait_while(state)

    def rpc_block_while(self, state_str):
        allowed_state = None
        try:
            allowed_state = ProcessingState.State[state_str]
        except Exception:
            return f'{state_str} is not a valid channel state.'
        self.block_while(allowed_state)
        return f'No channels in {state_str} state.'

    def rpc_show_config(self, channel):
        """
        Show the configuration for a channel.

        :type channel: string
        """
        txt = ""
        channels = self.channel_config_loader.get_channels()
        if channel == 'all':
            for ch in channels:
                txt += _channel_preamble(ch)
                txt += self.channel_config_loader.print_channel_config(ch)
            return txt

        if channel not in channels:
            return f"There is no active channel named {channel}."

        txt += _channel_preamble(channel)
        txt += self.channel_config_loader.print_channel_config(channel)
        return txt

    def rpc_show_de_config(self):
        return self.global_config.dump()

    def rpc_print_product(self, product, columns=None, query=None, types=False, format=None):
        def dataframe_to_table(df):
            return "{}\n".format(tabulate.tabulate(df, headers='keys', tablefmt='psql'))

        def dataframe_to_vertical_tables(df):
            txt = ""
            for i in range(len(df)):
                txt += f"Row {i}\n"
                txt += "{}\n".format(tabulate.tabulate(df.T.iloc[:, [i]], tablefmt='psql'))
            return txt

        def dataframe_to_column_names(df):
            columns = df.columns.values.reshape([len(df.columns), 1])
            return "{}\n".format(tabulate.tabulate(columns, headers=['columns'], tablefmt='psql'))

        def dataframe_to_json(df):
            return "{}\n".format(json.dumps(json.loads(df.to_json()), indent=4))

        found = False
        txt = "Product {}: ".format(product)
        with self.workers.access() as workers:
            for ch, worker in workers.items():
                if not worker.is_alive():
                    txt += f"Channel {ch} is in not active\n"
                    continue

                channel_config = self.channel_config_loader.get_channels()[ch]
                produces = self.channel_config_loader.get_produces(channel_config)
                r = [x for x in list(produces.items()) if product in x[1]]
                if not r:
                    continue
                found = True
                txt += " Found in channel {}\n".format(ch)
                tm = self.dataspace.get_taskmanager(ch)
                try:
                    data_block = datablock.DataBlock(self.dataspace,
                                                     ch,
                                                     taskmanager_id=tm['taskmanager_id'],
                                                     sequence_id=tm['sequence_id'])
                    data_block.generation_id -= 1
                    df = data_block[product]
                    df = pd.read_json(df.to_json())
                    dataframe_formatter = dataframe_to_table
                    if format == 'vertical':
                        dataframe_formatter = dataframe_to_vertical_tables
                    if format == 'column-names':
                        dataframe_formatter = dataframe_to_column_names
                    if format == 'json':
                        dataframe_formatter = dataframe_to_json
                    if types:
                        for column in df.columns:
                            df.insert(
                                df.columns.get_loc(column) + 1,
                                f"{column}.type",
                                df[column].transform(lambda x: type(x).__name__)
                            )
                    column_names = []
                    if columns:
                        column_names = columns.split(",")
                    if query:
                        if column_names:
                            txt += dataframe_formatter(df.loc[:, column_names].query(query))
                        else:
                            txt += dataframe_formatter(df.query(query))

                    else:
                        if column_names:
                            txt += dataframe_formatter(df.loc[:, column_names])
                        else:
                            txt += dataframe_formatter(df)
                except Exception as e:
                    txt += "\t\t{}\n".format(e)
        if not found:
            txt += "Not produced by any module\n"
        return txt[:-1]

    def rpc_print_products(self):
        with self.workers.access() as workers:
            channel_keys = workers.keys()
            if not channel_keys:
                return "No channels are currently active.\n"

            width = max([len(x) for x in channel_keys]) + 1
            txt = ""
            for ch, worker in workers.items():
                if not worker.is_alive():
                    txt += f"Channel {ch} is in ERROR state\n"
                    continue

                txt += "channel: {:<{width}}, id = {:<{width}}, state = {:<10} \n".format(ch,
                                                                                          worker.task_manager_id,
                                                                                          worker.get_state_name(),
                                                                                          width=width)
                tm = self.dataspace.get_taskmanager(ch)
                data_block = datablock.DataBlock(self.dataspace,
                                                 ch,
                                                 taskmanager_id=tm['taskmanager_id'],
                                                 sequence_id=tm['sequence_id'])
                data_block.generation_id -= 1
                channel_config = self.channel_config_loader.get_channels()[ch]
                produces = self.channel_config_loader.get_produces(channel_config)
                for i in ("sources",
                          "transforms",
                          "logicengines",
                          "publishers"):
                    txt += "\t{}:\n".format(i)
                    modules = channel_config.get(i, {})
                    for mod_name, mod_config in modules.items():
                        txt += "\t\t{}\n".format(mod_name)
                        products = produces.get(mod_name, [])
                        for product in products:
                            try:
                                df = data_block[product]
                                df = pd.read_json(df.to_json())
                                txt += "{}\n".format(tabulate.tabulate(df,
                                                                       headers='keys', tablefmt='psql'))
                            except Exception as e:
                                txt += "\t\t\t{}\n".format(e)
        return txt[:-1]

    def rpc_status(self):
        with self.workers.access() as workers:
            channel_keys = workers.keys()
            if not channel_keys:
                return "No channels are currently active.\n" + self.reaper_status()

            txt = ""
            width = max([len(x) for x in channel_keys]) + 1
            for ch, worker in workers.items():
                txt += "channel: {:<{width}}, id = {:<{width}}, state = {:<10} \n".format(ch,
                                                                                          worker.task_manager_id,
                                                                                          worker.get_state_name(),
                                                                                          width=width)
                channel_config = self.channel_config_loader.get_channels()[ch]
                for i in ("sources",
                          "transforms",
                          "logicengines",
                          "publishers"):
                    txt += "\t{}:\n".format(i)
                    modules = channel_config.get(i, {})
                    for mod_name, mod_config in modules.items():
                        txt += "\t\t{}\n".format(mod_name)
                        my_module = importlib.import_module(
                            mod_config.get('module'))
                        produces = None
                        consumes = None
                        try:
                            produces = getattr(my_module, 'PRODUCES')
                        except AttributeError:
                            pass
                        try:
                            consumes = getattr(my_module, 'CONSUMES')
                        except AttributeError:
                            pass
                        txt += "\t\t\tconsumes : {}\n".format(consumes)
                        txt += "\t\t\tproduces : {}\n".format(produces)
        return txt + self.reaper_status()

    def rpc_stop(self):
        self.shutdown()
        self.stop_channels()
        self.reaper_stop()
        return "OK"

    def start_channel(self, channel_name, channel_config):
        generation_id = 1
        task_manager = TaskManager.TaskManager(channel_name,
                                               generation_id,
                                               channel_config,
                                               self.global_config)
        worker = Worker(task_manager, self.global_config['logger'])
        with self.workers.access() as workers:
            workers[channel_name] = worker
        self.logger.debug(f"Trying to start {channel_name}")
        worker.start()
        worker.wait_while(ProcessingState.State['BOOT'])
        self.logger.info(f"Channel {channel_name} started")

    def start_channels(self):
        self.channel_config_loader.load_all_channels()

        if not self.channel_config_loader.get_channels():
            self.logger.info("No channel configurations available in " +
                             f"{self.channel_config_loader.channel_config_dir}")

        for name, config in self.channel_config_loader.get_channels().items():
            try:
                self.start_channel(name, config)
            except Exception as e:
                self.logger.error(f"Channel {name} failed to start : {e}")

    def rpc_start_channel(self, channel_name):
        with self.workers.access() as workers:
            if channel_name in workers:
                return f"ERROR, channel {channel_name} is running"

        success, result = self.channel_config_loader.load_channel(channel_name)
        if not success:
            return result
        self.start_channel(channel_name, result)
        return "OK"

    def rpc_start_channels(self):
        self.start_channels()
        return "OK"

    def rpc_stop_channel(self, channel):
        if not self.stop_channel(channel):
            return f"No channel found with the name {channel}."
        return "OK"

    def stop_worker(self, worker):
        if worker.is_alive():
            worker.task_manager.take_offline(None)
            worker.join(self.global_config.get("shutdown_timeout", 10))
        if worker.exitcode is None:
            worker.terminate()

    def stop_channel(self, channel):
        with self.workers.access() as workers:
            if channel not in workers:
                return False
            self.logger.debug(f"Trying to stop {channel}")
            self.stop_worker(workers[channel])
            del workers[channel]
        return True

    def stop_channels(self):
        with self.workers.access() as workers:
            for worker in workers.values():
                self.stop_worker(worker)
            workers.clear()

    def rpc_stop_channels(self):
        self.stop_channels()
        return "OK"

    def handle_sighup(self, signum, frame):
        self.reaper_stop()
        self.stop_channels()
        self.start_channels()
        self.reaper_start(delay=self.global_config['dataspace'].get('reaper_start_delay_seconds', 1818))

    def rpc_get_log_level(self):
        engineloglevel = self.get_logger().getEffectiveLevel()
        return logging.getLevelName(engineloglevel)

    def rpc_get_channel_log_level(self, channel):
        with self.workers.access() as workers:
            if channel not in workers:
                return f"No channel found with the name {channel}."

            worker = workers[channel]
            if not worker.is_alive():
                return f"Channel {channel} is in ERROR state."
            return logging.getLevelName(worker.task_manager.get_loglevel())

    def rpc_set_channel_log_level(self, channel, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        with self.workers.access() as workers:
            if channel not in workers:
                return f"No channel found with the name {channel}."

            worker = workers[channel]
            if not worker.is_alive():
                return f"Channel {channel} is in ERROR state."

            log_level_code = getattr(logging, log_level)
            if worker.task_manager.get_loglevel() == log_level_code:
                return f"Nothing to do. Current log level is : {log_level}"
            worker.task_manager.set_loglevel(log_level)
        return f"Log level changed to : {log_level}"

    def rpc_reaper_start(self, delay=0):
        '''
        Start the reaper process after 'delay' seconds.
        Default 0 seconds delay.
        :type delay: int
        '''
        self.reaper_start(delay)
        return "OK"

    def reaper_start(self, delay):
        self.reaper.start(delay)

    def rpc_reaper_stop(self):
        self.reaper_stop()
        return "OK"

    def reaper_stop(self):
        self.reaper.stop()

    def rpc_reaper_status(self):
        interval = self.reaper.get_retention_interval()
        state = self.reaper.get_state()
        txt = 'reaper:\n\tstate: {}\n\tretention_interval: {}'.format(state, interval)
        return txt

    def reaper_status(self):
        interval = self.reaper.get_retention_interval()
        state = self.reaper.get_state()
        txt = '\nreaper:\n\tstate: {}\n\tretention_interval: {}\n'.format(state, interval)
        return txt


def parse_program_options(args=None):
    ''' If args is a list, it will be used instead of sys.argv '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--port",
                        default=8888,
                        type=int,
                        choices=range(1, 65535),
                        metavar="<port number>",
                        help="Default port number is 8888; allowed values are in the half-open interval [1, 65535).")
    parser.add_argument("--config",
                        default=policies.GLOBAL_CONFIG_FILENAME,
                        metavar="<filename>",
                        help="Configuration file for initializing server; default behavior is to choose " +
                        f"'{policies.GLOBAL_CONFIG_FILENAME}' located in the CONFIG_PATH directory.")
    return parser.parse_args(args)


def _get_global_config(config_file, options):
    global_config = None
    try:
        global_config = ValidConfig.ValidConfig(config_file)
    except Exception as msg:
        sys.exit(f"Failed to load configuration {config_file}\n{msg}")

    global_config.update({
        'server_address': ['localhost', options.port]  # Use Jsonnet-supported schema (i.e. not a tuple)
    })
    return global_config


def _get_de_conf_manager(global_config_dir, channel_config_dir, options):
    config_file = os.path.join(global_config_dir, options.config)
    if not os.path.isfile(config_file):
        raise Exception(f"Config file '{config_file}' not found")

    global_config = _get_global_config(config_file, options)
    conf_manager = ChannelConfigHandler.ChannelConfigHandler(global_config, channel_config_dir)

    return (global_config, conf_manager)


def _create_de_server(global_config, channel_config_loader):
    '''Create the DE server with the passed global configuration and config manager'''
    server_address = tuple(global_config.get('server_address'))
    return DecisionEngine(global_config, channel_config_loader, server_address)


def _start_de_server(global_config, channel_config_loader):
    '''Create and start the DE server with the passed global configuration and config manager'''
    server = _create_de_server(global_config, channel_config_loader)
    server.reaper_start(delay=global_config['dataspace'].get('reaper_start_delay_seconds', 1818))
    server.start_channels()
    server.serve_forever()


def main(args=None):
    '''
    If args is None, sys.argv will be used instead
    If args is a list, it will be used instead of sys.argv (for unit testing)
    '''
    options = parse_program_options(args)
    global_config_dir = policies.global_config_dir()
    global_config, channel_config_loader = _get_de_conf_manager(global_config_dir,
                                                                policies.channel_config_dir(),
                                                                options)
    try:
        _start_de_server(global_config, channel_config_loader)
    except Exception as e:
        sys.exit("Server Address: {}\n".format(global_config.get('server_address')) +
                 "Config Dir: {}\n".format(global_config_dir) +
                 "Fatal Error: {}\n".format(e))


if __name__ == "__main__":
    main()
