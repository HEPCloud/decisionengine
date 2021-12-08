# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
This dummy source takes the name of a source datablock
from config file as parameter "data_product_name" and produces
an empty pandas DataFrame as a datablock with that name
"""
import pandas as pd

from decisionengine.framework.modules import Source
from decisionengine.framework.modules.Source import Parameter


@Source.supports_config(
    Parameter("data_product_name", default=""),
)
class EmptySource(Source.Source):
    def __init__(self, config):
        super().__init__(config)

        self.data_product_name = config.get("data_product_name")
        if not self.data_product_name:
            raise RuntimeError("No data_product_name found in configuration")

        self._produces = {self.data_product_name: pd.DataFrame}

    def acquire(self):
        self.logger.debug(f"in EmptySource: {self.data_product_name} acquire")
        return {self.data_product_name: pd.DataFrame()}


Source.describe(EmptySource)
