# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Publisher
from decisionengine.framework.taskmanager.PublisherStatus import PublisherStatus


@Publisher.consumes(bar=None, publisher_status=PublisherStatus)
class FailingPublisher(Publisher.Publisher):
    def __init__(self, config):
        super().__init__(config)
        self.module_key = config["module_key"]
        self.enabled = True

    def publish(self, data_block):
        assert self.publisher_status(data_block).is_enabled(self.module_key) == self.enabled
        self.enabled = False
        return self.enabled
