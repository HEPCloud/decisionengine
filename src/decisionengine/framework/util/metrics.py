import os

import prometheus_client
# from prometheus_client import CollectorRegistry, multiprocess, REGISTRY

# __all__ = [
#     'CHANNEL_STATE_GAUGE', 'SOURCE_ACQUIRE_GAUGE', 'LOGICENGINE_RUN_GAUGE',
#     'TRANSFORM_RUN_GAUGE', 'PUBLISHER_RUN_GAUGE'
# ]

# CHANNEL_STATE_GAUGE = Gauge('de_channel_state',
#                             'Channel state', [
#                                 'channel_name',
#                             ],
#                             multiprocess_mode='liveall')

# SOURCE_ACQUIRE_GAUGE = Gauge('de_source_last_acquire', "Last time a source "
#                              'successfully ran its acquire function', [
#                                  'channel_name',
#                                  'source_name',
#                              ],
#                              multiprocess_mode='liveall')

# LOGICENGINE_RUN_GAUGE = Gauge('de_logicengine_last_run', 'Last time '
#                               'a logicengine successfully ran', [
#                                   'channel_name',
#                                   'logicengine_name',
#                               ],
#                               multiprocess_mode='liveall')

# TRANSFORM_RUN_GAUGE = Gauge('de_transform_last_run', 'Last time a '
#                             'transform successfully ran', [
#                                 'channel_name',
#                                 'transform_name',
#                             ],
#                             multiprocess_mode='liveall')

# PUBLISHER_RUN_GAUGE = Gauge('de_publisher_last_run', 'Last time '
#                             'a publisher successfully ran', [
#                                 'channel_name',
#                                 'publisher_name',
#                             ],
#                             multiprocess_mode='liveall')

# def get_registry():
#     if 'prometheus_multiproc_dir' in os.environ:
#         registry = CollectorRegistry(auto_describe=True)
#         foo = multiprocess.MultiProcessCollector(registry)
#     else:
#         registry = REGISTRY
#     return registry


class Gauge(prometheus_client.Gauge):
    """Override prometheus client Gauge so that muliproccess_mode 'liveall" is
    the default as opposed to 'all'"""

    _DEFAULT_MULTIPROC_MODE = 'liveall'

    def __init__(self, *args, **kwargs):
        if self.__determine_multiprocess_mode_existence(*args, **kwargs):
            super().__init__(*args, **kwargs)
        else:
            super().__init__(multiprocess_mode=self._DEFAULT_MULTIPROC_MODE,
                             *args,
                             **kwargs)

    def __determine_multiprocess_mode_existence(self, *args, **kwargs):
        if 'multiprocess_mode' in kwargs:
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
