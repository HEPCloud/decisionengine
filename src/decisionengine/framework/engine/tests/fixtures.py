"""pytest defaults"""
import gc
import logging
import threading

import pytest

import decisionengine.framework.engine.de_client as de_client
import decisionengine.framework.engine.de_query_tool as de_query_tool

from decisionengine.framework.dataspace.tests.fixtures import (
    DATABASES_TO_TEST,
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
)
from decisionengine.framework.engine.DecisionEngine import (
    _create_de_server,
    _get_de_conf_manager,
    _start_de_server,
    parse_program_options,
)
from decisionengine.framework.util.sockets import get_random_port

__all__ = [
    "DATABASES_TO_TEST",
    "PG_DE_DB_WITH_SCHEMA",
    "PG_DE_DB_WITHOUT_SCHEMA",
    "SQLALCHEMY_PG_WITH_SCHEMA",
    "SQLALCHEMY_TEMPFILE_SQLITE",
    "PG_PROG",
    "DEServer",
]

# Not all test hosts are IPv6, generally IPv4 works fine some test
# hosts use IPv6 for localhost by default, even when not configured!
# Python XML RPC Socket server is IPv4 only right now.
DE_HOST = "127.0.0.1"


class DETestWorker(threading.Thread):
    """A DE Server process with our test config"""

    def __init__(
        self,
        conf_path,
        channel_conf_path,
        server_address,
        datasource,
        conf_override=None,
        channel_conf_override=None,
    ):
        """format of args should match what you set in conf_mamanger"""
        super().__init__(name="DETestWorker")
        self.server_address = server_address

        self.global_config, self.channel_config_loader = _get_de_conf_manager(
            conf_path, channel_conf_path, parse_program_options([])
        )

        # Override global configuration for testing
        self.global_config["shutdown_timeout"] = 1
        self.global_config["server_address"] = self.server_address
        self.global_config["dataspace"]["datasource"] = datasource

        self.de_server = _create_de_server(self.global_config, self.channel_config_loader)

    def run(self):
        _start_de_server(self.de_server)

    def de_client_run_cli(self, *args):
        """
        Run the DE Client CLI with these args
        The DE Server host/port are automatically set for you
        """
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
    """A DE Server using a private database"""

    @pytest.fixture(params=DATABASES_TO_TEST)
    def de_server_factory(request):
        """
        This parameterized fixture will mock up various datasources.

        Add datasource objects to DATABASES_TO_TEST once they've got
        our basic schema loaded.  Pytest should take it from there and
        automatically run it throught all the below tests
        """
        logger = logging.getLogger()
        if port:
            host_port = (host, port)
        else:
            host_port = (host, get_random_port())

        conn_fixture = request.getfixturevalue(request.param)

        datasource = {}
        try:
            # SQL Alchemy
            datasource["config"] = {}
            datasource["module"] = "decisionengine.framework.dataspace.datasources.sqlalchemy_ds"
            datasource["name"] = "SQLAlchemyDS"
            datasource["config"]["url"] = conn_fixture["url"]
            datasource["config"]["echo"] = True
        except TypeError:
            datasource["module"] = "decisionengine.framework.dataspace.datasources.postgresql"
            datasource["name"] = "Postgresql"
            datasource["config"] = {}
            try:
                # psycopg2
                datasource["config"]["host"] = conn_fixture.info.host
                datasource["config"]["port"] = conn_fixture.info.port
                datasource["config"]["user"] = conn_fixture.info.user
                datasource["config"]["password"] = conn_fixture.info.password
                datasource["config"]["database"] = conn_fixture.info.dbname
            except AttributeError:
                # psycopg2cffi
                for element in conn_fixture.dsn.split():
                    (key, value) = element.split("=")
                    if value != "''" and value != '""':
                        datasource["config"][key] = value

        logger.debug(f"DE Fixture has datasource config: {datasource}")

        server_proc = DETestWorker(
            conf_path,
            channel_conf_path,
            host_port,
            datasource,
            conf_override,
            channel_conf_override,
        )
        logger.debug("Starting DE Fixture")
        server_proc.start()

        # Ensure the channels have started
        logger.debug(f"DE Fixture: Wait on startup state: is_set={server_proc.de_server.startup_complete.is_set()}")
        server_proc.de_server.startup_complete.wait()
        logger.debug(
            f"DE Fixture: Done waiting for startup state: is_set={server_proc.de_server.startup_complete.is_set()}"
        )

        if not server_proc.is_alive():
            raise RuntimeError("Could not start PrivateDEServer fixture")

        yield server_proc

        logger.debug("DE Fixture: beginning cleanup")

        # does not error out even if the server is stopped
        # so this should be safe to call under all conditions
        logger.debug("DE Fixture: running rpc_stop()")
        server_proc.de_server.rpc_stop()

        logger.debug("DE Fixture: waiting for server_proc.join()")
        server_proc.join()

        del server_proc
        gc.collect()

    return de_server_factory
