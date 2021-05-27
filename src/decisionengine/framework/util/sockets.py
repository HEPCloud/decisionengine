import socket
import structlog

logger = structlog.getLogger("decision_engine")
logger = logger.bind(module=__name__.split(".")[-1])

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
