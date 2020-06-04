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

class TestClientServerPython(unittest.TestCase):

    def setUp(self):
        self.port = str(get_random_port())

        os.environ['CONFIG_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/etc/decisionengine/'

        os.environ['DECISIONENGINE_NO_CHANNELS'] = "1"

        self.server_proc = multiprocessing.Process(target=de_server.main, args=([('--port', self.port)]), name='de-server')
        self.server_proc.start()

        time.sleep(1)
        if not self.server_proc.is_alive():
            raise RuntimeError('Unable to start test DE Server')

        time.sleep(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect(('127.0.0.1', int(self.port)))

        if self.server_proc.exitcode:
            raise RuntimeError('DE Server terminated too early')

        if len(multiprocessing.active_children()) < 1:
            raise RuntimeError('DE Server child process not found')

        elif len(multiprocessing.active_children()) > 1:
            raise RuntimeError('DE Server old child process not terminated')

    def tearDown(self):
        del os.environ['DECISIONENGINE_NO_CHANNELS']

        try:
            de_client.main(args_to_parse=['--host=127.0.0.1', '--port=' + self.port, '--stop'])
            time.sleep(5)
        except ConnectionRefusedError:
            # server already shutdown
            pass

        if self.server_proc.is_alive():
            self.server_proc.terminate()

    def test_client_can_get_de_server_show_config(self):
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--show-config'])
        self.assertEqual('{}', output, msg="DE didn't share empty config")

    def test_client_can_get_de_server_reload_config(self):
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reload-config'])
        self.assertEqual('OK', output, msg="DE didn't say OK")

    def test_client_can_get_de_server_reaper_status(self):
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-status'])
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('retention_interval:', output, msg="Couldn't find reaper interval")

    def test_client_can_get_de_server_reaper_stop(self):
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-stop'])
        self.assertEqual('OK', output, msg="DE didn't say OK")

        # get status to be sure
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-status'])
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('State.STOPPED', output, msg="reaper state incorrect")

    def test_client_can_get_de_server_reaper_start_delay(self):
        # make sure the reaper is stopped first
        de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-stop'])

        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-start', '--reaper-start-delay-secs=90'])
        self.assertEqual('OK', output, msg="DE didn't say OK")

        # get status to be sure
        output = de_client.main(['--host=127.0.0.1', '--port', self.port, '--reaper-status'])
        self.assertIn('reaper:', output, msg="Couldn't find reaper section")
        self.assertIn('state:', output, msg="Couldn't find reaper state")
        self.assertIn('State.STARTING', output, msg="reaper state incorrect")


if __name__ == '__main__':
    unittest.main()
