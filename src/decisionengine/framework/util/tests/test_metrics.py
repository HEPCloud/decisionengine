# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Fixture based tests for the metrics interfaces"""
# pylint: disable=redefined-outer-name

import pytest

from decisionengine.framework.util.metrics import display_metrics
from decisionengine.framework.util.tests.fixtures import Counter, Gauge, OtherMetric, prometheus_env_setup  # noqa: F401


@pytest.mark.parametrize(
    "test_params",
    [
        {
            "metric_args": ["test_gauge_default_multiproc_par", "test_gauge_default_multiproc_par"],
            "wanted_multiprocess_mode": "liveall",
        },
        {
            "metric_args": ["test_gauge_multiproc_override_par", "test_gauge_multiproc_override_par"],
            "metric_kwargs": {"multiprocess_mode": "all"},
            "wanted_multiprocess_mode": "all",
        },
        {
            "metric_args": ["test_gauge_multiproc_override_with_arg", "test_gauge_multiproc_override_with_arg", "all"],
            "wanted_multiprocess_mode": "all",
        },
    ],
)
def test_gauge_set_multiproc_mode(Gauge, test_params):  # noqa: F811
    """
    Test setting the gauge multiproc mode

    test_params is a list of dicts that support three keys:
        'metric_args': list of arguments to pass to Gauge
        'metric_kwargs': dict of keyword arguments to pass to Gauge
        'wanted_multiprocess_mode': Intended multiprocess mode of Gauge after
            instantiation
    """
    g = Gauge(*test_params["metric_args"], **test_params.get("metric_kwargs", {}))
    assert g._multiprocess_mode == test_params.get("wanted_multiprocess_mode", pytest.gauge_default_multiproc_mode)


def test_gauge_multiproc_override_invalid(Gauge):  # noqa: F811
    """Test overriding the default gauge multiproc mode with something
    invalid"""
    new_multiprocess_mode = "foo"
    with pytest.raises(ValueError, match="Invalid multiprocess mode"):
        _ = Gauge(
            "test_gauge_multiproc_override_invalid",
            "test_gauge_multiproc_override_invalid",
            multiprocess_mode=new_multiprocess_mode,
        )


def test_gauge_set_value(Gauge):  # noqa: F811
    """Test setting a gauge value"""
    g = Gauge("test_gauge_set_value", "test_gauge_set_value")
    g.set(42)
    assert g._value.get() == 42


def test_gauge_set_invalid_value(Gauge):  # noqa: F811
    """Try to set a gauge to an invalid value"""
    g = Gauge(
        "test_gauge_set_invalid_value",
        "test_gauge_set_invalid_value",
    )
    with pytest.raises(ValueError):
        g.set("badstring")


def test_counter_inc_value(Counter):  # noqa: F811
    """Increment the counter"""
    c = Counter("test_counter_inc_value", "test_counter_inc_value")
    c.inc()
    assert c._value.get() == 1


@pytest.mark.parametrize("other_metric_arg", ["histogram", "summary"])
def test_other_metric_observe_value(OtherMetric, other_metric_arg):  # noqa: F811
    """Observe a histogram or summary value and make sure it is stored properly"""
    _m = OtherMetric(other_metric_arg)
    test_metric_string = f"test_{other_metric_arg}_observe_value"
    m = _m(test_metric_string, test_metric_string)
    m.observe(42)
    assert m._sum.get() == 42


def test_noop_display_metrics():
    """Just ensure the function runs without error"""
    display_metrics()
