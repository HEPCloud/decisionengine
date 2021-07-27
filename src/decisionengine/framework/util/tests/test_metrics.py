import pytest


@pytest.fixture(autouse=True)
def env_setup(tmp_path, monkeypatch):
    """Make sure we have a directory set for PROMETHEUS_MULTIPROC_DIR so that
    metric instantiation gives us multiprocess metrics"""
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


@pytest.fixture
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
@pytest.mark.usefixtures("Gauge")
def test_gauge_set_multiproc_mode(Gauge, test_params):
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


@pytest.mark.usefixtures("Gauge")
def test_gauge_multiproc_override_invalid(Gauge):
    """Test overriding the default gauge multiproc mode with something
    invalid"""
    new_multiprocess_mode = "foo"
    with pytest.raises(ValueError, match="Invalid multiprocess mode"):
        _ = Gauge(
            "test_gauge_multiproc_override_invalid",
            "test_gauge_multiproc_override_invalid",
            multiprocess_mode=new_multiprocess_mode,
        )


@pytest.mark.usefixtures("Gauge")
def test_gauge_set_value(Gauge):
    """Test setting a gauge value"""
    g = Gauge("test_gauge_set_value", "test_gauge_set_value")
    g.set(42)
    assert g._value.get() == 42


@pytest.mark.usefixtures("Gauge")
def test_gauge_set_invalid_value(Gauge):
    """Try to set a gauge to an invalid value"""
    g = Gauge(
        "test_gauge_set_invalid_value",
        "test_gauge_set_invalid_value",
    )
    with pytest.raises(ValueError):
        g.set("badstring")


@pytest.mark.usefixtures("Counter")
def test_counter_inc_value(Counter):
    """Increment the counter"""
    c = Counter("test_counter_inc_value", "test_counter_inc_value")
    c.inc()
    assert c._value.get() == 1


@pytest.mark.parametrize("other_metric_arg", ["histogram", "summary"])
@pytest.mark.usefixtures("OtherMetric")
def test_other_metric_observe_value(OtherMetric, other_metric_arg):
    """Observe a histogram or summary value and make sure it is stored properly"""
    _m = OtherMetric(other_metric_arg)
    test_metric_string = f"test_{other_metric_arg}_observe_value"
    m = _m(test_metric_string, test_metric_string)
    m.observe(42)
    assert m._sum.get() == 42
