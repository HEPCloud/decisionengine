# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Transform
from decisionengine.framework.modules.Transform import Parameter


@Transform.supports_config(Parameter("data_product_name", type=str), Parameter("consumes", type=list))
class DynamicTransform(Transform.Transform):
    def __init__(self, config):
        self.data_product_name = config["data_product_name"]
        self._consumes = dict.fromkeys(config["consumes"], int)
        self._produces = {self.data_product_name: int}

    def transform(self, data_block):
        all_values = [data_block[key] for key in self._consumes.keys()]
        return {self.data_product_name: sum(all_values, 0)}


Transform.describe(DynamicTransform)
