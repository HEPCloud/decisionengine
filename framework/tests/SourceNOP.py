import pandas as pd

from decisionengine.framework.modules import Source

PRODUCES = ["foo"]


class SourceNOP(Source.Source):

    def __init__(self, config):
        super().__init__(config)

    def produces(self):
        return PRODUCES

    def acquire(self):
        return {PRODUCES[0]: pd.DataFrame([{'key1': 'value', 'key2': 0.1}, ])}
