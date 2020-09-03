import multiprocessing
import os
import time
import unittest

import pytest
from pytest_postgresql import factories

import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.configmanager.ConfigManager import ConfigManager
from decisionengine.framework.engine.DecisionEngine import DecisionEngine
from decisionengine.framework.util.sockets import get_random_port

_CWD = os.path.dirname(os.path.abspath(__file__))
_DDL_FILE = "../dataspace/datasources/postgresql.sql"
_CONFIG_PATH = os.path.join(_CWD, "etc/decisionengine")

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
        conf_manager = ConfigManager()
        conf_manager.load()
        #
        # Override config for testing
        #
        conf_manager.global_config['server_address'] = ['localhost', self.port]
        conf_manager.global_config['dataspace']['datasource']['config']['port'] \
            = self.db_parameters['port']
        conf_manager.global_config['dataspace']['datasource']['config']['user'] \
            = self.db_parameters['user']
        conf_manager.global_config['dataspace']['datasource']['config']['database'] \
            = self.db_parameters['dbname']

        global_config = conf_manager.get_global_config()
        server_address = tuple(global_config.get('server_address'))
        server = DecisionEngine(conf_manager, server_address)
        server.reaper_start(delay=global_config['dataspace'].
                            get('reaper_start_delay_seconds', 1818))
        server.start_channels()
        server.serve_forever()


@pytest.mark.usefixtures("fixtures")
class TestChannel(unittest.TestCase):

    def setUp(self):
        #self.port = get_random_port()
        self.port = 9999
        self.worker = Worker(self.datasource.info.dsn_parameters,
                             self.port)
        self.worker.start()
        #
        # config used by this test uses 1 second schedule, run few cycles
        #
        time.sleep(5)

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
        return de_client.main(["--host=localhost",
                               "--port",
                               str(self.port),
                               *args])

    def test_client_can_get_de_server_status(self):
        output = self.de_client_request("--status")
        self.assertIn("STEADY",
                      output,
                      msg="Channel not in STEADY state")


if __name__ == "__main__":
    unittest.main()
