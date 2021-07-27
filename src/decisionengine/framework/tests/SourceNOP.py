import pandas as pd

from decisionengine.framework.modules import Source


@Source.produces(foo=pd.DataFrame)
class SourceNOP(Source.Source):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        result = {
            'foo':
            pd.DataFrame([
                {
                    'key1': 'value1',
                    'key2': 0.1
                },
                {
                    'key1': 'value2',
                    'key2': 2
                },
            ])
        }
        return result


Source.describe(SourceNOP)
