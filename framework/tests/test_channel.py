import pytest_postgresql
import psycopg2
import multiprocessing
import pytest
import unittest
import os
import time
import socket 

from decisionengine.framework.engine.DecisionEngine import DecisionEngine
import decisionengine.framework.engine.de_client 
from  decisionengine.framework.configmanager.ConfigManager import ConfigManager

_CWD  =  os.path.dirname(os.path.abspath(__file__))
_DDL_FILE = "../dataspace/datasources/postgresql.sql"
_CONFIG_PATH = os.path.join(_CWD, "etc/decisionengine")

def get_random_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

from pytest_postgresql import factories

postgresql_my_proc = factories.postgresql_proc(port=None)
postgresql = factories.postgresql('postgresql_my_proc', db_name='decisionengine')

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
        os.environ['CONFIG_PATH'] = _CONFIG_PATH        
        conf_manager = ConfigManager()
        conf_manager.load()
        # 
        # Override config for testibg
        # 
        conf_manager.global_config['server_address'] = ['localhost', self.port]
        conf_manager.global_config['dataspace']['datasource']['config']['port'] = self.db_parameters["port"]
        conf_manager.global_config['dataspace']['datasource']['config']['user'] = self.db_parameters["user"]
        conf_manager.global_config['dataspace']['datasource']['config']['database'] = self.db_parameters["dbname"]

        global_config = conf_manager.get_global_config()
        server_address = tuple(global_config.get('server_address'))
        server = DecisionEngine(conf_manager, server_address)
        server.reaper_start(delay=global_config['dataspace'].get('reaper_start_delay_seconds', 1818))
        server.start_channels()
        server.serve_forever()


@pytest.mark.usefixtures("fixtures")
class TestDatablock(unittest.TestCase):

    def setUp(self):
        self.port = get_random_port()
        self.worker  = Worker(self.datasource.info.dsn_parameters,
                              self.port)
        self.worker.start()

    def testSome(self):
        con = psycopg2.connect(self.datasource.dsn)
        cursor = con.cursor()
        cursor.execute("select * from dataproduct")
        res = cursor.fetchall()
        print(res)

    def tearDown(self):
        self.worker.join()
        
if __name__ == "__main__":
    unittest.main()
    
