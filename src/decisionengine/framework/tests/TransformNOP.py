# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd

from decisionengine.framework.modules import Transform


@Transform.consumes(foo=pd.DataFrame)
@Transform.produces(bar=pd.DataFrame)
class TransformNOP(Transform.Transform):
    def __init__(self, config):
        super().__init__(config)

    def transform(self, data_block):
        df_in = self.foo(data_block)  # pylint: disable=no-member
        return {"bar": pd.DataFrame(df_in["key2"])}


Transform.describe(TransformNOP)
