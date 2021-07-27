import prometheus_client


class Gauge(prometheus_client.Gauge):
    """Override prometheus client Gauge so that muliproccess_mode 'liveall" is
    the default as opposed to 'all'"""

    _DEFAULT_MULTIPROC_MODE = "liveall"

    def __init__(self, *args, **kwargs):
        if self.__determine_multiprocess_mode_existence(*args, **kwargs):
            super().__init__(*args, **kwargs)
        else:
            super().__init__(multiprocess_mode=self._DEFAULT_MULTIPROC_MODE, *args, **kwargs)

    def __determine_multiprocess_mode_existence(self, *args, **kwargs):
        if "multiprocess_mode" in kwargs:
            return True
        for arg in args:
            if isinstance(arg, str) and arg in self._MULTIPROC_MODES:
                return True
        return False


class Counter(prometheus_client.Counter):
    pass


class Histogram(prometheus_client.Histogram):
    pass


class Summary(prometheus_client.Summary):
    pass
