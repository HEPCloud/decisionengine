# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Source
from decisionengine.framework.modules.Source import Parameter


@Source.supports_config(Parameter("data_product_name", type=str))
class DynamicSource(Source.Source):
    def __init__(self, config):
        self.data_product_name = config["data_product_name"]
        self._produces = {self.data_product_name: int}

    def acquire(self):
        return {self.data_product_name: 1}


Source.describe(DynamicSource)
