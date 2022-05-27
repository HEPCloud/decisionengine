# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd

from decisionengine.framework.modules import Publisher


@Publisher.consumes(bar=pd.DataFrame)
class PublisherNOP(Publisher.Publisher):
    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block):
        self.bar(data_block)  # pylint: disable=no-member


Publisher.describe(PublisherNOP)
