#!/usr/bin/env python3

import os
import socket
import multiprocessing
import time

import unittest

import decisionengine.framework.engine.DecisionEngine as de_server
import decisionengine.framework.engine.de_client as de_client

def get_random_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


# Insulate from parent environments
multiprocessing.set_start_method('spawn')

_HOME = '127.0.0.1'
_LOG_LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

class TestClientServerPython(unittest.TestCase):
    def setUp(self):
        self.port = str(get_random_port())

        os.environ['CONFIG_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/etc/decisionengine/'
        os.environ['DECISIONENGINE_NO_CHANNELS'] = "1"

        self.server_proc = multiprocessing.Process(target=de_server.main,
                                                   args=([('--port', self.port)]),
                                                   name='de-server')
        self.server_proc.start()

        time.sleep(1)
        if not self.server_proc.is_alive():
            raise RuntimeError('Unable to start test DE Server')

        time.sleep(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((_HOME, int(self.port)))

        if self.server_proc.exitcode:
            raise RuntimeError('DE Server terminated too early')

        if len(multiprocessing.active_children()) < 1:
            raise RuntimeError('DE Server child process not found')

        elif len(multiprocessing.active_children()) > 1:
            raise RuntimeError('DE Server old child process not terminated')

    def tearDown(self):
        del os.environ['DECISIONENGINE_NO_CHANNELS']

        try:
            self.de_client_request('--stop')
        except ConnectionRefusedError:
            # server already shutdown
            pass

        if self.server_proc.is_alive():
            self.server_proc.terminate()

    def de_client_request(self, *args):
        return de_client.main([f'--host={_HOME}', '--port', self.port, *args])

    def test_client_can_get_de_server_show_config(self):
        output = self.de_client_request('--show-config')
        self.assertNotEqual('{}', output, msg="DE didn't share channel configs")

    def test_client_can_get_de_server_reload_config(self):
        output = self.de_client_request('--reload-config')
        self.assertEqual('OK', output, msg="DE didn't say OK")

    def test_client_can_get_de_server_reaper_status(self):
        output = self.de_client_request('--reaper-status')
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('retention_interval:', output, msg="Couldn't find reaper interval")

    def test_client_can_get_de_server_reaper_stop(self):
        output = self.de_client_request('--reaper-stop')
        self.assertEqual('OK', output, msg="DE didn't say OK")

        # get status to be sure
        output = self.de_client_request('--reaper-status')
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('State.STOPPED', output, msg="reaper state incorrect")

    def test_client_can_get_de_server_reaper_start_delay(self):
        # make sure the reaper is stopped first
        self.de_client_request('--reaper-stop')

        output = self.de_client_request('--reaper-start', '--reaper-start-delay-secs=90')
        self.assertEqual('OK', output, msg="DE didn't say OK")

        # get status to be sure
        output = self.de_client_request('--reaper-status')
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('State.STARTING', output, msg="reaper state incorrect")

    def test_client_can_get_de_server_show_logger_level(self):
        output = self.de_client_request('--print-engine-loglevel')
        self.assertIn(output, _LOG_LEVELS, msg="DE didn't give a valid log level")

    def test_client_can_get_de_server_show_channel_logger_level(self):
        output = self.de_client_request('--get-channel-loglevel=UNITTEST')
        self.assertIn(output, _LOG_LEVELS, msg="DE didn't get channel logger level")

    def test_global_channel_log_level_in_config(self):
        output = self.de_client_request('--show-de-config')
        self.assertIn('global_channel_log_level',
                      output,
                      msg="Global channel log level not set in config file. Default value is INFO.")


if __name__ == '__main__':
    unittest.main()
