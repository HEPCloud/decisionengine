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
import multiprocessing
import pandas as pd
import os
import tabulate
import uuid

import socketserver
import xmlrpc.server

from decisionengine.framework.config import ChannelConfigHandler, ValidConfig, policies
import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.dataspace.dataspace as dataspace
import decisionengine.framework.taskmanager.TaskManager as TaskManager

CONFIG_UPDATE_PERIOD = 10  # seconds
FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(module)s - %(process)d - %(threadName)s - %(levelname)s - %(message)s")

def _channel_preamble(name):
    header = f'Channel: {name}'
    rule = '=' * len(header)
    return '\n' + rule + '\n' + header + '\n' + rule + '\n\n'


class Worker(multiprocessing.Process):

    def __init__(self, task_manager, logger_config):
        super().__init__()
        self.task_manager = task_manager
        self.logger_config = logger_config

    def run(self):
        logger = logging.getLogger()
        logger_rotate_by = self.logger_config.get("file_rotate_by", "size")

        if logger_rotate_by == "size":
            file_handler = logging.handlers.RotatingFileHandler(os.path.join(
                                                                os.path.dirname(
                                                                    self.logger_config["log_file"]),
                                                                self.task_manager.name + ".log"),
                                                                maxBytes=self.logger_config.get("max_file_size",
                                                                200 * 1000000),
                                                                backupCount=self.logger_config.get("max_backup_count",
                                                                6))
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(
                                                                     os.path.dirname(
                                                                         self.logger_config["log_file"]),
                                                                     self.task_manager.name + ".log"),
                                                                     when=self.logger_config.get("rotation_time_unit", 'D'),
                                                                     interval=self.logger_config.get("rotation_time_interval", '1'))

        file_handler.setFormatter(FORMATTER)
        logger.setLevel(logging.WARNING)
        logger.addHandler(file_handler)
        channel_log_level = self.logger_config.get("global_channel_log_level", "WARNING")
        self.task_manager.set_loglevel(channel_log_level)
        self.task_manager.run()


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
        self.task_managers = {}
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

    def rpc_print_product(self, product, columns=None, query=None):
        found = False
        txt = "Product {}: ".format(product)
        for ch, worker in self.task_managers.items():
            if not worker:
                txt += f"Channel {ch} is in ERROR state\n"
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
                column_names = []
                if columns:
                    column_names = columns.split(",")
                if query:
                    if column_names:
                        txt += "{}\n".format(tabulate.tabulate(df.loc[:, column_names].query(query),
                                                               headers='keys',
                                                               tablefmt='psql'))
                    else:
                        txt += "{}\n".format(tabulate.tabulate(df.query(query),
                                                               headers='keys',
                                                               tablefmt='psql'))

                else:
                    if column_names:
                        txt += "{}\n".format(tabulate.tabulate(df.loc[:, column_names],
                                                               headers='keys',
                                                               tablefmt='psql'))
                    else:
                        txt += "{}\n".format(tabulate.tabulate(df,
                                                               headers='keys',
                                                               tablefmt='psql'))
            except Exception as e:
                txt += "\t\t{}\n".format(e)
        if not found:
            txt += "Not produced by any module\n"
        return txt[:-1]

    def rpc_print_products(self):
        channel_keys = self.task_managers.keys()
        if not channel_keys:
            return "No channels are currently active.\n"

        width = max([len(x) for x in channel_keys]) + 1
        txt = ""
        for ch, worker in self.task_managers.items():
            if not worker:
                txt += f"Channel {ch} is in ERROR state\n"
                continue

            sname = worker.task_manager.get_state_name()
            txt += "channel: {:<{width}}, id = {:<{width}}, state = {:<10} \n".format(ch,
                                                                                      worker.task_manager.id,
                                                                                      sname,
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
        channel_keys = self.task_managers.keys()
        if not channel_keys:
            return "No channels are currently active.\n" + self.reaper_status()

        txt = ""
        width = max([len(x) for x in channel_keys]) + 1
        for ch, worker in self.task_managers.items():
            if not worker:
                txt += f"Channel {ch} is in ERROR state\n"
                continue

            sname = worker.task_manager.get_state_name()
            txt += "channel: {:<{width}}, id = {:<{width}}, state = {:<10} \n".format(ch,
                                                                                      worker.task_manager.id,
                                                                                      sname,
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
        self.reaper_stop()
        self.stop_channels()
        self.shutdown()
        return "OK"

    def start_channel(self, channel_name, channel_config):
        generation_id = 1
        taskmanager_id = str(uuid.uuid4()).upper()
        task_manager = TaskManager.TaskManager(channel_name,
                                               taskmanager_id,
                                               generation_id,
                                               channel_config,
                                               self.global_config)
        worker = Worker(task_manager,
                        self.global_config['logger'])
        self.task_managers[channel_name] = worker
        worker.start()
        self.logger.info(f"Channel {channel_name} started")

    def start_channels(self):
        self.channel_config_loader.load_all_channels()
        for name, config in self.channel_config_loader.get_channels().items():
            try:
                self.start_channel(name, config)
            except Exception as e:
                self.logger.error(f"Channel {name} failed to start : {e}")

    def rpc_start_channel(self, channel_name):
        if channel_name in self.task_managers:
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
        self.stop_channel(channel)
        return "OK"

    def stop_channel(self, channel):
        worker = self.task_managers[channel]
        worker.task_manager.set_state(TaskManager.State.SHUTTINGDOWN)
        worker.join(self.global_config.get("shutdown_timeout", 10))
        del self.task_managers[channel]

    def stop_channels(self):
        for channel_name in self.task_managers:
            self.stop_channel(channel_name)

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
        worker = self.task_managers[channel]
        return logging.getLevelName(worker.task_manager.get_loglevel())

    def rpc_set_channel_log_level(self, channel, log_level):
        """Assumes log_level is a string corresponding to the supported logging-module levels."""
        worker = self.task_managers[channel]
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

    def _disable_channels_with_terminated_processes(self):
        channels_to_remove = []
        for channel, process in self.task_managers.items():
            if process and not process.is_alive():
                channels_to_remove.append(channel)
        for channel in channels_to_remove:
            self.task_managers[channel] = None

    # The 'service_actions' method here overrides the socketserver
    # base class' implementation.  It is called during the
    # 'serve_forever' call for each iteration of the server-request
    # loop, which is typically executed once every 0.5 seconds.
    def service_actions(self):
        self._disable_channels_with_terminated_processes()

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
        'server_address': ['localhost', options.port] # Use Jsonnet-supported schema (i.e. not a tuple)
    })
    return global_config

def _get_de_conf_manager(global_config_dir, channel_config_dir, options):
    config_file = os.path.join(global_config_dir, options.config)
    if not os.path.isfile(config_file):
        raise Exception(f"Config file '{config_file}' not found")

    global_config = _get_global_config(config_file, options)
    conf_manager = ChannelConfigHandler.ChannelConfigHandler(global_config, channel_config_dir)

    if not conf_manager.get_channels():
        logging.info(f"No channel configurations available in {channel_config_dir}")

    return (global_config, conf_manager)

def _start_de_server(global_config, channel_config_loader):
    '''start the DE server with the passed global configuration and config manager'''
    server_address = tuple(global_config.get('server_address'))
    server = DecisionEngine(global_config,
                            channel_config_loader,
                            server_address)
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
