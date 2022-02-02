# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

__all__ = ["prometheus_env_setup", "Gauge", "Counter", "OtherMetric"]


@pytest.fixture(autouse=True)
def prometheus_env_setup(tmp_path, monkeypatch):
    """Make sure we have a directory set for PROMETHEUS_MULTIPROC_DIR so that
    metric instantiation gives us multiprocess metrics"""
    # Get a fixed dir
    d = tmp_path
    monkeypatch.setenv("PROMETHEUS_MULTIPROC_DIR", str(d))
    yield
    monkeypatch.delenv("PROMETHEUS_MULTIPROC_DIR")


# Put these metrics declarations in fixtures because we need the env_setup
# fixture to be set before importing any of the metrics
@pytest.fixture()
def Gauge():
    from decisionengine.framework.util.metrics import Gauge

    pytest.gauge_default_multiproc_mode = Gauge._DEFAULT_MULTIPROC_MODE

    def _gauge(*args, **kwargs):
        return Gauge(*args, **kwargs)

    yield _gauge


@pytest.fixture()
def Counter():
    from decisionengine.framework.util.metrics import Counter

    def _counter(*args, **kwargs):
        return Counter(*args, **kwargs)

    yield _counter


@pytest.fixture()
def OtherMetric():
    from decisionengine.framework.util.metrics import Histogram, Summary

    def _decider(metric_type):
        if metric_type == "histogram":

            def _histogram(*args, **kwargs):
                return Histogram(*args, **kwargs)

            return _histogram
        elif metric_type == "summary":

            def _summary(*args, **kwargs):
                return Summary(*args, **kwargs)

            return _summary

    yield _decider
