from decisionengine.framework.modules import Publisher
import pandas as pd


@Publisher.consumes(bar=pd.DataFrame)
class PublisherNOP(Publisher.Publisher):

    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block):
        self.bar(data_block) # noqa


Publisher.describe(PublisherNOP)
