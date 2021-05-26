'''pytest defaults'''
import threading

import pytest

import decisionengine.framework.engine.de_client as de_client
import decisionengine.framework.engine.de_query_tool as de_query_tool

from decisionengine.framework.dataspace.datasources.tests.fixtures import (
    PG_DE_DB_WITH_SCHEMA,
    PG_PROG,
    DATABASES_TO_TEST,
)
from decisionengine.framework.engine.DecisionEngine import (
    _get_de_conf_manager,
    _create_de_server,
    parse_program_options,
)
from decisionengine.framework.util.sockets import get_random_port
from decisionengine.framework.taskmanager.TaskManager import State

__all__ = ["DATABASES_TO_TEST", "PG_DE_DB_WITH_SCHEMA", "PG_PROG", "DEServer"]

# Not all test hosts are IPv6, generally IPv4 works fine some test
# hosts use IPv6 for localhost by default, even when not configured!
# Python XML RPC Socket server is IPv4 only right now.
DE_HOST = '127.0.0.1'


class DETestWorker(threading.Thread):
    '''A DE Server process with our test config'''

    def __init__(
        self,
        conf_path,
        channel_conf_path,
        server_address,
        db_info,
        conf_override=None,
        channel_conf_override=None,
    ):
        '''format of args should match what you set in conf_mamanger'''
        super().__init__(name='DETestWorker')
        self.server_address = server_address

        global_config, channel_config_loader = _get_de_conf_manager(
            conf_path, channel_conf_path, parse_program_options([])
        )

        # Override global configuration for testing
        global_config['shutdown_timeout'] = 1
        global_config['server_address'] = self.server_address
        global_config['dataspace']['datasource']['config'] = db_info

        self.de_server = _create_de_server(global_config, channel_config_loader)
        self.reaper_start_delay_seconds = global_config['dataspace'].get(
            "reaper_start_delay_seconds", 1818
        )

    def run(self):
        self.de_server.reaper_start(delay=self.reaper_start_delay_seconds)
        self.de_server.start_channels()
        self.de_server.serve_forever()

    def de_client_run_cli(self, *args):
        '''
        Run the DE Client CLI with these args
        The DE Server host/port are automatically set for you
        '''
        return de_client.main(
            [
                "--host",
                self.server_address[0],
                "--port",
                str(self.server_address[1]),
                *args,
            ]
        )

    def de_query_tool_run_cli(self, *args):
        """
        Run the DE Query Tool CLI with these args.
        The DE Server host/port are automatically set for you.

        Returns:
            str: Query result
        """
        return de_query_tool.main(
            [
                "--host",
                self.server_address[0],
                "--port",
                str(self.server_address[1]),
                *args,
            ]
        )


# pylint: disable=invalid-name
def DEServer(
    conf_path=None,
    conf_override=None,
    channel_conf_path=None,
    channel_conf_override=None,
    host=DE_HOST,
    port=None,
):
    '''A DE Server using a private database'''

    @pytest.fixture(params=DATABASES_TO_TEST)
    def de_server_factory(request):
        '''
        This parameterized fixture will mock up various datasources.

        Add datasource objects to DATABASES_TO_TEST once they've got
        our basic schema loaded.  Pytest should take it from there and
        automatically run it throught all the below tests
        '''
        if port:
            host_port = (host, port)
        else:
            host_port = (host, get_random_port())

        conn_fixture = request.getfixturevalue(request.param)

        db_info = {}
        try:
            # SQL Alchemy
            db_info['url'] = conn_fixture.url
        except AttributeError:
            try:
                # psycopg2
                db_info['host'] = conn_fixture.info.host
                db_info['port'] = conn_fixture.info.port
                db_info['user'] = conn_fixture.info.user
                db_info['password'] = conn_fixture.info.password
                db_info['database'] = conn_fixture.info.dbname
            except AttributeError:
                # psycopg2cffi
                for element in conn_fixture.dsn.split():
                    (key, value) = element.split('=')
                    if value != "''" and value != '""':
                        db_info[key] = value

        server_proc = DETestWorker(
            conf_path,
            channel_conf_path,
            host_port,
            db_info,
            conf_override,
            channel_conf_override,
        )
        server_proc.start()
        # The following block only works if there are
        # active workers; if it is called before any workers
        # exist, then it will return and not block as requested.
        # so long as your config contains at least one worker,
        # this will work as you'd expect.
        server_proc.de_server.block_while(State.BOOT)

        if not server_proc.is_alive():
            raise RuntimeError('Could not start PrivateDEServer fixture')

        yield server_proc

        if server_proc.is_alive():
            server_proc.de_server.rpc_stop()

        server_proc.join()

    return de_server_factory
