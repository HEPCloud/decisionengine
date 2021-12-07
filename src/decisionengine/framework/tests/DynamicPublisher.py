# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Publisher
from decisionengine.framework.modules.Publisher import Parameter


@Publisher.supports_config(Parameter("consumes", type=list), Parameter("expects", type=int))
class DynamicPublisher(Publisher.Publisher):
    def __init__(self, config):
        self.expects = config["expects"]
        self._consumes = dict.fromkeys(config["consumes"], int)

    def publisher(self, data_block):
        all_values = [data_block[key] for key in self._consumes.keys()]
        assert self.expects == sum(all_values, 0)


Publisher.describe(DynamicPublisher)
