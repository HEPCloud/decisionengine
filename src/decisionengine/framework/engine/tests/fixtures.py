# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""pytest defaults"""
import gc
import logging
import os
import random
import re
import tempfile
import threading

import pytest

import decisionengine.framework.engine.de_client as de_client
import decisionengine.framework.engine.de_query_tool as de_query_tool

from decisionengine.framework.dataspace.tests.fixtures import (
    DATABASES_TO_TEST,
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
        self.conf_path = conf_path
        self.channel_conf_path = channel_conf_path

        self.global_config, self.channel_config_loader = _get_de_conf_manager(
            conf_path, channel_conf_path, parse_program_options([])
        )

        # Because multiple DETestWorkers can be in use concurrently,
        # we assign different database numbers (from 0 through 15 by
        # redis default) where possible to avoid kombu messaging
        # collisions whenever routing keys are the same.

        # If pytest-xdist is being used, and 16 or fewer xdist workers
        # are being used, we can use the number in the worker ID as
        # the database ID.  Otherwise, we assign a random number
        # between 0 and 15 (inclusive).
        db_number = 0
        xdist_worker_count = os.environ.get("PYTEST_XDIST_WORKER_COUNT")
        if xdist_worker_count and int(xdist_worker_count) <= 16:
            worker_id = os.environ["PYTEST_XDIST_WORKER"]
            db_number = re.sub(r"^gw(\d{1,2})", r"\1", worker_id)  # Remove the gw prefix
            assert int(db_number) < 16
        else:
            db_number = random.randrange(0, 16)
        # Override global configuration for testing
        self.global_config["broker_url"] = f"redis://localhost:6379/{db_number}"
        self.global_config["shutdown_timeout"] = 1
        self.global_config["server_address"] = self.server_address
        self.global_config["dataspace"]["datasource"] = datasource
        self.global_config["no_webserver"] = False
        self.global_config["webserver"] = {}
        self.global_config["webserver"]["port"] = get_random_port()

        self.de_server = _create_de_server(self.global_config, self.channel_config_loader)
        self.stdout_at_setup = None

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
            ],
            logger_name=None,
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
            ],
            logger_name=None,
        )


# pylint: disable=invalid-name
def DEServer(
    conf_path=None,
    conf_override=None,
    channel_conf_path=None,
    channel_conf_override=None,
    host=DE_HOST,
    port=None,
    make_conf_dirs_if_missing=False,
    block_until_startup_complete=True,
):
    """A DE Server using a private database"""

    @pytest.fixture(params=DATABASES_TO_TEST)
    def de_server_factory(tmp_path, request, capsys, monkeypatch):
        """
        This parameterized fixture will mock up various datasources.

        Add datasource objects to DATABASES_TO_TEST once they've got
        our basic schema loaded.  Pytest should take it from there and
        automatically run it throughout all the below tests
        """
        logger = logging.getLogger()
        if port:
            host_port = (host, port)
        else:
            host_port = (host, get_random_port())

        conn_fixture = request.getfixturevalue(request.param)

        datasource = {}

        # SQL Alchemy
        datasource["config"] = {}
        datasource["module"] = "decisionengine.framework.dataspace.datasources.sqlalchemy_ds"
        datasource["name"] = "SQLAlchemyDS"
        datasource["config"]["url"] = conn_fixture["url"]
        datasource["config"]["echo"] = True

        logger.debug(f"DE Fixture has datasource config: {datasource}")

        # make it easy to give each fixture a unique private config path
        # for more flexible startup options
        with tempfile.TemporaryDirectory(dir=tmp_path) as tmppath:
            nonlocal conf_path
            nonlocal channel_conf_path
            if conf_path is None:
                conf_path = os.path.join(tmppath, "conf.d")
            if channel_conf_path is None:
                channel_conf_path = os.path.join(tmppath, "channel.conf.d")
            prometheus_multiproc_dir = str(os.path.join(tmppath, "PROMETHEUS_MULTIPROC_DIR"))

            if make_conf_dirs_if_missing and not os.path.exists(conf_path):
                logger.debug(f"DE Fixture making {conf_path}")
                os.makedirs(conf_path)
            if make_conf_dirs_if_missing and not os.path.exists(channel_conf_path):
                logger.debug(f"DE Fixture making {channel_conf_path}")
                os.makedirs(channel_conf_path)
            if not os.path.exists(prometheus_multiproc_dir):
                logger.debug(f"DE Fixture making {prometheus_multiproc_dir}")
                os.makedirs(prometheus_multiproc_dir)

            monkeypatch.setenv("PROMETHEUS_MULTIPROC_DIR", prometheus_multiproc_dir)
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

            if block_until_startup_complete:
                # Ensure the channels have started
                logger.debug(
                    f"DE Fixture: Wait on startup state: is_set={server_proc.de_server.startup_complete.is_set()}"
                )
                server_proc.de_server.startup_complete.wait()
                server_proc.stdout_at_setup = capsys.readouterr().out

                logger.debug(
                    f"DE Fixture: Done waiting for startup state: is_set={server_proc.de_server.startup_complete.is_set()}"
                )

            if not server_proc.is_alive():
                raise RuntimeError("Could not start PrivateDEServer fixture")

            yield server_proc

        logger.debug("DE Fixture: beginning cleanup")

        monkeypatch.delenv("PROMETHEUS_MULTIPROC_DIR")

        # does not error out even if the server is stopped
        # so this should be safe to call under all conditions
        logger.debug("DE Fixture: running rpc_stop()")
        server_proc.de_server.rpc_stop()

        logger.debug("DE Fixture: waiting for server_proc.join()")
        server_proc.join()

        del server_proc
        gc.collect()

    return de_server_factory
