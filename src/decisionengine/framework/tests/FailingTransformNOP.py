import pandas as pd

from decisionengine.framework.modules import Transform


class TransformWithMisingProducesConsumes(Transform.Transform):

    def __init__(self, config):
        super().__init__(config)

    def transform(self, data_block):
        df_in = data_block['foo']
        return {'bar': pd.DataFrame(df_in["key2"])}

    def consumes(self, name_list=None):
        return ['foo', ]

    def produces(self, name_schema_id_list=None):
        return ['bar', ]
