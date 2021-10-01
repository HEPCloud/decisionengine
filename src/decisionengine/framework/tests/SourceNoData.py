import pandas as pd

from decisionengine.framework.modules import Source


@Source.produces(foo=pd.DataFrame)
class SourceNoData(Source.Source):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        return None


Source.describe(SourceNoData)
