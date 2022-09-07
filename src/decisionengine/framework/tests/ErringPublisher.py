# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Publisher


@Publisher.consumes(bar=None)
class ErringPublisher(Publisher.Publisher):
    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block):
        raise RuntimeError("Test error-handling")
