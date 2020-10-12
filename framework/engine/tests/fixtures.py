'''pytest defaults'''
import threading

import psycopg2
import pytest
from pytest_postgresql.factories import DatabaseJanitor

import decisionengine.framework.engine.de_client as de_client

from decisionengine.framework.dataspace.datasources.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA, PG_PROG, DE_DB
from decisionengine.framework.engine.DecisionEngine import _get_de_conf_manager, _create_de_server, parse_program_options
from decisionengine.framework.util.sockets import get_random_port
from decisionengine.framework.taskmanager.TaskManager import State

__all__ = ['DE_DB_HOST', 'DE_DB_USER', 'DE_DB_PASS', 'DE_DB_NAME', 'DE_SCHEMA',
           'PG_PROG', 'DE_DB', 'DE_HOST', 'DEServer']

# Not all test hosts are IPv6, generally IPv4 works fine some test
# hosts use IPv6 for localhost by default, even when not configured!
# Python XML RPC Socket server is IPv4 only right now.
DE_HOST = '127.0.0.1'

class DETestWorker(threading.Thread):
    '''A DE Server process with our test config'''

    def __init__(self, conf_path, channel_conf_path, server_address, db_info, conf_override=None, channel_conf_override=None):
        '''format of args should match what you set in conf_mamanger'''
        super().__init__()
        self.db_info = db_info
        self.server_address = server_address

        global_config, channel_config_loader = _get_de_conf_manager(conf_path, channel_conf_path, parse_program_options([]))

        # Override global configuration for testing
        db_info['database'] = db_info.pop('dbname')  # Replace key to conform with datasource config. specification

        global_config['shutdown_timeout'] = 1
        global_config['server_address'] = self.server_address
        global_config['dataspace']['datasource']['config'] = db_info

        self.de_server = _create_de_server(global_config, channel_config_loader)
        self.reaper_start_delay_seconds = global_config['dataspace'].get('reaper_start_delay_seconds', 1818)

    def run(self):
        self.de_server.reaper_start(delay=self.reaper_start_delay_seconds)
        self.de_server.start_channels()
        self.de_server.serve_forever()

    def de_client_run_cli(self, *args):
        '''
        Run the DE Client CLI with these args
        The DE Server host/port are automatically set for you
        '''
        return de_client.main(["--host", self.server_address[0],
                               "--port", str(self.server_address[1]),
                               *args])


# pylint: disable=invalid-name
def DEServer(conf_path=None, conf_override=None,
             channel_conf_path=None, channel_conf_override=None,
             host=DE_HOST, port=None,
             pg_prog_name='PG_PROG', pg_db_conn_name='DE_DB'):
    '''A DE Server using our private database'''

    @pytest.fixture(scope='function')
    def de_server_factory(request):
        '''
        actually make the fixture
        '''
        if port:
            host_port = (host, port)
        else:
            host_port = (host, get_random_port())

        db_info = {}

        proc_fixture = request.getfixturevalue(pg_prog_name)
        db_info['host'] = proc_fixture.host
        db_info['port'] = proc_fixture.port
        db_info['user'] = proc_fixture.user
        db_info['password'] = proc_fixture.password

        conn_fixture = request.getfixturevalue(pg_db_conn_name)
        db_info['dbname'] = conn_fixture.get_dsn_parameters()['dbname'] + '_private'

        # for reasons I've yet to determine
        #  the schema isn't populated by the DE_DB fixture here...
        #  but the tablespace is locked by the fixture...
        #  so we just do it manually for now in a slightly different DB

        # DatabaseJanitor will create and drop the tablespace for us
        with DatabaseJanitor(user=db_info['user'], password=db_info['password'],
                             host=db_info['host'], port=db_info['port'],
                             db_name=db_info['dbname'], version=conn_fixture.server_version):

            with psycopg2.connect(**db_info) as connection:
                for filename in DE_SCHEMA: # noqa: F405
                    with open(filename, 'r') as _fd, \
                         connection.cursor() as cur:
                        cur.execute(_fd.read())

            server_proc = DETestWorker(conf_path, channel_conf_path, host_port, db_info, conf_override, channel_conf_override)
            server_proc.start()
            server_proc.de_server.block_while(State.BOOT)

            if not server_proc.is_alive():
                raise RuntimeError('Could not start PrivateDEServer fixture')

            yield server_proc

            if server_proc.is_alive():
                server_proc.de_server.rpc_stop()

            server_proc.join()

    return de_server_factory
