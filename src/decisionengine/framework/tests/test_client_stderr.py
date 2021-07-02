'''Fixture based DE Server for the de-client tests'''
# pylint: disable=redefined-outer-name

import io
import sys

import pytest

import decisionengine.framework.engine.de_client as de_client
from decisionengine.framework.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_PROG,
    DEServer,
    TEST_CONFIG_PATH,
    TEST_CHANNEL_CONFIG_PATH,
)

deserver = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_client_status_msg_to_stdout(deserver):
    """Make sure the actuall client console call goes to stdout"""

    myoutput = io.StringIO()
    sys.stdout = myoutput
    de_client.console_scripts_main(['--host', deserver.server_address[0],
                                    '--port', str(deserver.server_address[1]),
                                    '--status'])
    sys.stdout = sys.__stdout__
    assert 'channel: test_channel' in myoutput.getvalue()
