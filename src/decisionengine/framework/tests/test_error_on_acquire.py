import os

import pytest

from decisionengine.framework.tests.fixtures import (  # noqa: F401
    PG_DE_DB_WITH_SCHEMA,
    PG_DE_DB_WITHOUT_SCHEMA,
    PG_PROG,
    DEServer,
    TEST_CONFIG_PATH,
)

_channel_config_dir = os.path.join(TEST_CONFIG_PATH, "test-error-on-acquire")  # noqa: F405
deserver = DEServer(
    conf_path=TEST_CONFIG_PATH, channel_conf_path=_channel_config_dir
)  # pylint: disable=invalid-name


@pytest.mark.usefixtures("deserver")
def test_source_only_channel(deserver):
    # The following 'block-while' call will be unnecessary once the
    # deserver fixture can reliably block when no workers have yet
    # been constructed.
    deserver.de_client_run_cli("--block-while", "BOOT")
    output = deserver.de_client_run_cli('--stop-channel', 'error_on_acquire')
    assert "Channel error_on_acquire stopped cleanly." == output
