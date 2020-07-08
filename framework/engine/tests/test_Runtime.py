#!/usr/bin/env python3

import os
import socket
import subprocess
import sys
import time

import unittest

_DE_SERVER = "./DecisionEngine.py"
_DE_CLIENT = "./de_client.py"
_DE_CLIENT_ARGS = {
    'cwd': os.path.dirname(__file__) + '/../',
    'stdout': subprocess.PIPE,
    'stderr': subprocess.PIPE,
    'universal_newlines': True,
    'check': True
}


def get_random_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class TestCanRunAtAll(unittest.TestCase):

    def setUp(self):
        self.port = str(get_random_port())

        os.environ['CONFIG_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/etc/decisionengine/'

    def tearDown(self):
        del os.environ['CONFIG_PATH']


    def test_can_run_de_server(self):
        ''' Am I syntax valid '''
        os.environ['DECISIONENGINE_NO_CHANNELS'] = "1"
        try:
            proc = subprocess.run([_DE_SERVER, '--port=' + self.port],
                                  cwd=os.path.dirname(__file__) + '/../',
                                  timeout=4,
                                  check=True)
        except subprocess.TimeoutExpired:
            # ran for a few seconds, probably means I'm syntax valid
            #     which is the only thing we are testing in this test
            pass
        finally:
            try:
                # unconditionally kill the process, don't worry if it is already dead
                proc.kill()
            except Exception:
                pass
        del os.environ['DECISIONENGINE_NO_CHANNELS']

    def test_can_run_de_client(self):
        ''' Am I syntax valid '''
        subprocess.run([_DE_CLIENT], cwd=os.path.dirname(__file__) + '/../', check=True)

class TestClientServerBehaviors(unittest.TestCase):

    def setUp(self):
        self.port = str(get_random_port())

        os.environ['CONFIG_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/../../tests/etc/decisionengine/'

        os.environ['DECISIONENGINE_NO_CHANNELS'] = "1"

        self.server_proc = subprocess.Popen([_DE_SERVER, '--port=' + self.port],
                                            cwd=os.path.dirname(__file__) + '/../',
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            universal_newlines=True)
        time.sleep(2)

        if self.server_proc.poll() is not None:
            print("Using port:" + self.port, file=sys.stderr)
            print(''.join(self.server_proc.stdout.readlines()), file=sys.stderr)
            print(''.join(self.server_proc.stderr.readlines()), file=sys.stderr)
            raise RuntimeError('Unable to start test DE Server')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect(('localhost', int(self.port)))

    def tearDown(self):
        del os.environ['DECISIONENGINE_NO_CHANNELS']

        try:
            subprocess.run([_DE_CLIENT, '--port=' + self.port, '--stop'],
                           cwd=os.path.dirname(__file__) + '/../',
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           timeout=4)
        except subprocess.TimeoutExpired:
            pass

        self.server_proc.kill()
        time.sleep(1)

    def test_client_can_stop_de_server(self):
        if self.server_proc.poll() is not None:
            raise RuntimeError('DE Server not running, cannot try to stop it')

        try:
            subprocess.run([_DE_CLIENT, '--port=' + self.port, '--stop'],
                           **_DE_CLIENT_ARGS,
                           timeout=4)
            self.server_proc.wait(3)
        except subprocess.TimeoutExpired:
            pass

        self.assertEqual(0, self.server_proc.returncode, msg="DE didn't stop")

    def test_client_can_get_de_server_show_config(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--show-config'], **_DE_CLIENT_ARGS)
        self.assertNotEqual('{}\n', output.stdout, msg="DE didn't get channel configuration.")

    def test_client_can_get_de_server_reload_config(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reload'], **_DE_CLIENT_ARGS)
        self.assertEqual('OK\n', output.stdout, msg="DE didn't say OK")

    def test_client_can_get_de_server_reaper_status(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-status'], **_DE_CLIENT_ARGS)
        self.assertIn('reaper:', output.stdout, msg="Couldn't find reaper section")
        self.assertIn('state:', output.stdout, msg="Couldn't find reaper state")
        self.assertIn('retention_interval:', output.stdout, msg="Couldn't find reaper interval")

    def test_client_can_get_de_server_reaper_stop(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-stop'], **_DE_CLIENT_ARGS)
        self.assertEqual('OK\n', output.stdout, msg="DE didn't say OK")

        # get status to be sure
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-status'], **_DE_CLIENT_ARGS)
        self.assertIn('reaper:', output.stdout, msg="Couldn't find reaper section")
        self.assertIn('state:', output.stdout, msg="Couldn't find reaper state")
        self.assertIn('State.STOPPED', output.stdout, msg="reaper state incorrect")

    def test_client_can_get_de_server_reaper_start_delay(self):
        # make sure the reaper is stopped first
        subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-stop'], **_DE_CLIENT_ARGS)

        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-start', '--reaper-start-delay-secs=90'],
                                **_DE_CLIENT_ARGS)
        self.assertEqual('OK\n', output.stdout, msg="DE didn't say OK")

        # get status to be sure
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--reaper-status'], **_DE_CLIENT_ARGS)
        self.assertIn('reaper:', output.stdout, msg="Couldn't find reaper section")
        self.assertIn('state:', output.stdout, msg="Couldn't find reaper state")
        self.assertIn('State.STARTING', output.stdout, msg="reaper state incorrect")

    def test_client_can_get_de_server_show_logger_level(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--print-engine-loglevel'], **_DE_CLIENT_ARGS)
        self.assertIn(output.stdout, ['NOTSET\n', 'DEBUG\n', 'INFO\n', 'WARNING\n', 'ERROR\n', 'CRITICAL\n'], msg="DE didn't give a valid log level")

    def test_client_can_get_de_server_show_channel_logger_level(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--get-channel-loglevel=UNITTEST'], **_DE_CLIENT_ARGS)
        self.assertIn(output.stdout, ['NOTSET\n', 'DEBUG\n', 'INFO\n', 'WARNING\n', 'ERROR\n', 'CRITICAL\n'], msg="DE didn't get channel logger level")

    def test_global_channel_log_level_in_config(self):
        output = subprocess.run([_DE_CLIENT, '--port=' + self.port, '--show-de-config'], **_DE_CLIENT_ARGS)
        self.assertIn('global_channel_log_level', output.stdout, msg="Global channel log level not set in config file. Default value is INFO.")


if __name__ == '__main__':
    unittest.main()
