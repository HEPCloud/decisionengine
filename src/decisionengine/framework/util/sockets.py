import socket
import structlog

from decisionengine.framework.modules.logging_configDict import LOGGERNAME, DELOGGER_CHANNEL_NAME

logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)

def get_random_port():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    except OSError:  # pragma: no cover
        logger.exception("problem with get_random_port")
        raise
    except Exception:  # pragma: no cover
        logger.exception("Unexpected error!")
        raise
