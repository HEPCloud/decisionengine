import os

from prometheus_client import CollectorRegistry, multiprocess, REGISTRY, Gauge

__all__ = [
    'CHANNEL_STATE_GAUGE', 'SOURCE_ACQUIRE_GAUGE', 'LOGICENGINE_RUN_GAUGE',
    'TRANSFORM_RUN_GAUGE', 'PUBLISHER_RUN_GAUGE'
]

CHANNEL_STATE_GAUGE = Gauge('de_channel_state',
                            'Channel state', [
                                'channel_name',
                            ],
                            multiprocess_mode='liveall')

SOURCE_ACQUIRE_GAUGE = Gauge('de_source_last_acquire', "Last time a source "
                             'successfully ran its acquire function', [
                                 'channel_name',
                                 'source_name',
                             ],
                             multiprocess_mode='liveall')

LOGICENGINE_RUN_GAUGE = Gauge('de_logicengine_last_run', 'Last time '
                              'a logicengine successfully ran', [
                                  'channel_name',
                                  'logicengine_name',
                              ],
                              multiprocess_mode='liveall')

TRANSFORM_RUN_GAUGE = Gauge('de_transform_last_run', 'Last time a '
                            'transform successfully ran', [
                                'channel_name',
                                'transform_name',
                            ],
                            multiprocess_mode='liveall')

PUBLISHER_RUN_GAUGE = Gauge('de_publisher_last_run', 'Last time '
                            'a publisher successfully ran', [
                                'channel_name',
                                'publisher_name',
                            ],
                            multiprocess_mode='liveall')


def get_registry():
    if 'prometheus_multiproc_dir' in os.environ:
        registry = CollectorRegistry(auto_describe=True)
        foo = multiprocess.MultiProcessCollector(registry)
    else:
        registry = REGISTRY
    return registry
