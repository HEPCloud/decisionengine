import pandas as pd

from decisionengine.framework.modules import Transform

CONSUMES = ["foo"]
PRODUCES = ["bar"]


class TransformNOP(Transform.Transform):

    def __init__(self, config):
        super().__init__(config):

    def transform(self, data_block):
        df_in = data_block[CONSUMES[0]]
        return {PRODUCES[0] : pd.DataFrame(df_in["key2"])}

    def consumes(self, name_list=None):
        return CONSUMES

    def produces(self, name_schema_id_list=None):
        return PRODUCES

