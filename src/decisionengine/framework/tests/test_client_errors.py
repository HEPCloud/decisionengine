'''Fixture based DE Server tests of the sample config'''
# pylint: disable=redefined-outer-name

import pytest

from decisionengine.framework.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA  # noqa: F401
from decisionengine.framework.tests.fixtures import DE_DB, DE_HOST, PG_PROG, DEServer, TEST_CONFIG_PATH, TEST_CHANNEL_CONFIG_PATH  # noqa: F401

deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=TEST_CHANNEL_CONFIG_PATH) # pylint: disable=invalid-name

@pytest.mark.usefixtures("deserver")
def test_client_cannot_wait_on_bad_state(deserver):
    '''Verify wait is for a valid state'''
    output = deserver.de_client_run_cli('--block-while=INVALID_STATE')
    assert output == 'INVALID_STATE is not a valid channel state.'
