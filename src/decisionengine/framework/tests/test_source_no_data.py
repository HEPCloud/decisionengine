import os

import pytest

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    DEServer,
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    SQLALCHEMY_PG_WITH_SCHEMA,
    SQLALCHEMY_TEMPFILE_SQLITE,
    TEST_CONFIG_PATH,
)

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-source-no-data")  # noqa: F405
deserver = DEServer(conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_source_only_channel(deserver):
    # The following 'block-while' call will be unnecessary once the
    # deserver fixture can reliably block when no workers have yet
    # been constructed.
    deserver.de_client_run_cli("--block-while", "BOOT")
    output = deserver.de_client_run_cli("--status")
    assert "test-source-no-data" in output
    assert "state = OFFLINE" in output
