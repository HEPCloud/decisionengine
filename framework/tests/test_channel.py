import multiprocessing
import os
import time
import unittest

import pytest
from pytest_postgresql import factories

import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _start_de_server
from decisionengine.framework.util.sockets import get_random_port

_CWD = os.path.dirname(os.path.abspath(__file__))
_DDL_FILE = "../dataspace/datasources/postgresql.sql"
_CONFIG_PATH = os.path.join(_CWD, "etc/decisionengine")
_LOG_LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
# Not all test hosts are IPv6, generally IPv4 works fine
#  some test hosts use IPv6 for localhost by default, even when not configured!
#  Python XML RPC Socket server is IPv4 only right now.
_HOST = '127.0.0.1'

postgresql_my_proc = factories.postgresql_proc(port=None)
postgresql = factories.postgresql("postgresql_my_proc",
                                  db_name="decisionengine")

@pytest.fixture()
def datasource(request, postgresql):
    with postgresql.cursor() as cursor:
        cursor.execute(open(os.path.join(_CWD, _DDL_FILE), "r").read())
    postgresql.commit()
    return postgresql

@pytest.fixture()
def fixtures(request, datasource):
    request.cls.datasource = datasource


class Worker(multiprocessing.Process):

    def __init__(self, db_parameters, port):
        super().__init__()
        self.db_parameters = db_parameters
        self.port = port

    def run(self):
        os.environ["CONFIG_PATH"] = _CONFIG_PATH
        conf_manager = _get_de_conf_manager([])

        #
        # Override config for testing
        #
        conf_manager.global_config['server_address'] = [_HOST, self.port]
        conf_manager.global_config['dataspace']['datasource']['config']['port'] \
            = self.db_parameters['port']
        conf_manager.global_config['dataspace']['datasource']['config']['user'] \
            = self.db_parameters['user']
        conf_manager.global_config['dataspace']['datasource']['config']['database'] \
            = self.db_parameters['dbname']

        _start_de_server(conf_manager)


@pytest.mark.usefixtures("fixtures")
class TestChannel(unittest.TestCase):

    def setUp(self):
        self.port = get_random_port()
        self.worker = Worker(self.datasource.info.dsn_parameters,
                             self.port)
        self.worker.start()
        #
        # config used by this test uses 1 second schedule, make sure one completes
        #
        time.sleep(1)

    def tearDown(self):
        try:
            self.de_client_request("--stop")
        except ConnectionRefusedError:
            # server already shutdown
            pass
        finally:
            if self.worker.is_alive():
                self.worker.terminate()

    def de_client_request(self, *args):
        return de_client.main(["--host",
                               _HOST,
                               "--port",
                               str(self.port),
                               *args])

    def test_client_can_get_de_server_status(self):
        # make sure channels have a chance to get into state
        time.sleep(5)
        output = self.de_client_request("--status")
        self.assertIn("STEADY", output, msg="Channel not in STEADY state")

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


if __name__ == "__main__":
    unittest.main()
