import multiprocessing
import os
import socket
import time

import unittest

import decisionengine.framework.engine.DecisionEngine as de_server
import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.util.sockets import get_random_port

# Insulate from parent environments

_HOME = '127.0.0.1'
_LOG_LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
_PORT = str(get_random_port())


class TestClientServerPython(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['CONFIG_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/etc/decisionengine/'
        os.environ['DECISIONENGINE_NO_CHANNELS'] = "1"
        cls.server_proc = multiprocessing.Process(target=de_server.main,
                                                  args=([('--port', _PORT)]),
                                                  name='de-server')
        cls.server_proc.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()

    def de_client_request(self, *args):
        return de_client.main([f'--host={_HOME}', '--port', _PORT, *args])

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
