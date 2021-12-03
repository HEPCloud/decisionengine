import pytest

from decisionengine.framework.engine.DecisionEngine import _verify_redis_server, _verify_redis_url


def test_verify_bad_url():
    bad_url = "Garbage"
    expected = (
        f"Unsupported broker URL format '{bad_url}'\n"
        "See https://docs.celeryproject.org/projects/kombu/en/stable/userguide/connections.html#urls"
    )
    with pytest.raises(RuntimeError, match=expected):
        _verify_redis_url(bad_url)


def test_verify_bad_broker():
    amqp_backend = "amqp://localhost:6379/0"
    expected = "Unsupported data-broker backend 'amqp'; only 'redis' is currently supported."
    with pytest.raises(RuntimeError, match=expected):
        _verify_redis_url(amqp_backend)


def test_verify_redis_url():
    _verify_redis_url("redis://localhost:6379/0")
    _verify_redis_url("redis://127.0.0.1:6379/0")


def test_verify_redis_server():
    _verify_redis_server("redis://localhost:6379/0")


def test_verify_bad_redis_server():
    url = "redis://localhost:1234/5"
    expected = f"A server with broker URL {url} is not responding."
    with pytest.raises(RuntimeError, match=expected):
        _verify_redis_server(url)
