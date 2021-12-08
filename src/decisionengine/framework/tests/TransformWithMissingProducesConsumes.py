# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd

from decisionengine.framework.modules import Transform


class TransformWithMissingProducesConsumes(Transform.Transform):
    def __init__(self, config):
        super().__init__(config)

    def transform(self, data_block):
        df_in = data_block["foo"]
        return {"bar": pd.DataFrame(df_in["key2"])}
