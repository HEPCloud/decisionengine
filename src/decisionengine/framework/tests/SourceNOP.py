import pandas as pd

from decisionengine.framework.modules import Source
from prometheus_client import Gauge



@Source.produces(foo=pd.DataFrame)
class SourceNOP(Source.Source):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        return {
            "foo": pd.DataFrame(
                [
                    {"key1": "value1", "key2": 0.1},
                    {"key1": "value2", "key2": 2},
                    {"key1": "value3", "key2": "Test"},
                ]
            )
        }


Source.describe(SourceNOP)
