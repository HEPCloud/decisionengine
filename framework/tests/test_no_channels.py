import multiprocessing
import os
import tempfile
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
_CHANNEL_CONFIG_DIR = tempfile.TemporaryDirectory()
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
        os.environ["CHANNEL_CONFIG_PATH"] = _CHANNEL_CONFIG_DIR.name
        conf_manager = _get_de_conf_manager([])

        #
        # Override config for testing
        #
        conf_manager.global_config['server_address'] = [_HOST, self.port]
        conf_manager.global_config['dataspace']['datasource']['config'].update(
            port=self.db_parameters['port'],
            user=self.db_parameters['user'],
            database=self.db_parameters['dbname']
        )

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
        self.assertIn("No channels are currently active", output)

    def test_client_can_print_products(self):
        # make sure channels have a chance to get into state
        time.sleep(5)
        output = self.de_client_request("--print-products")
        self.assertIn("No channels are currently active", output)


if __name__ == "__main__":
    unittest.main()
