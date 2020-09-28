import multiprocessing
import os
import re
from shutil import copy
import tempfile
import time
import unittest

import pytest
from pytest_postgresql import factories

import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _start_de_server, parse_program_options
from decisionengine.framework.util.sockets import get_random_port

_CWD = os.path.dirname(os.path.abspath(__file__))
_DDL_FILE = "../dataspace/datasources/postgresql.sql"
_CONFIG_PATH = os.path.join(_CWD, "etc/decisionengine")
_CHANNEL_CONFIG_DIR = tempfile.TemporaryDirectory()

# Not all test hosts are IPv6, generally IPv4 works fine some test
# hosts use IPv6 for localhost by default, even when not configured!
# Python XML RPC Socket server is IPv4 only right now.
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
        global_config, conf_manager = _get_de_conf_manager(_CONFIG_PATH,
                                                           _CHANNEL_CONFIG_DIR.name,
                                                           parse_program_options([]))

        # Override config for testing
        global_config['server_address'] = [_HOST, self.port]
        global_config['dataspace']['datasource']['config'].update(
            port=self.db_parameters['port'],
            user=self.db_parameters['user'],
            database=self.db_parameters['dbname']
        )

        _start_de_server(global_config, conf_manager)


@pytest.mark.usefixtures("fixtures")
class TestChannel(unittest.TestCase):

    def setUp(self):
        self.port = get_random_port()
        self.worker = Worker(self.datasource.info.dsn_parameters,
                             self.port)
        self.worker.start()
        time.sleep(2)

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

    # Because pytest will reorder the tests based on the method name,
    # we implement the whole 'workflow' as one unit test.
    def test_start_from_nothing(self):
        # Verify that nothing is active
        output = self.de_client_request("--status")
        assert "No channels are currently active" in output

        output = self.de_client_request("--print-products")
        assert "No channels are currently active" in output

        # Add channel config to directory
        channel_config = os.path.join(_CWD, 'etc/decisionengine/config.d/test_channel.jsonnet')
        new_config_path = copy(channel_config, _CHANNEL_CONFIG_DIR.name)
        assert os.path.exists(new_config_path)

        # Activate channel and check for steady state
        output = self.de_client_request('--start-channel', 'test_channel')
        assert output == 'OK'
        time.sleep(5)
        output = self.de_client_request('--status')
        assert re.search('test_channel.*state = STEADY', output)

        # Take channel offline
        output = self.de_client_request('--stop-channel', 'test_channel')
        assert output == 'OK'

        # Verify no channels are active
        output = self.de_client_request("--status")
        assert "No channels are currently active" in output

        # Verify that the relevant configuration file still exists.
        assert os.path.exists(new_config_path)
