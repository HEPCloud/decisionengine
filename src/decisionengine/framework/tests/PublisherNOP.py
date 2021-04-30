from decisionengine.framework.modules import Publisher

CONSUMES = ["foo"]


class PublisherNOP(Publisher.Publisher):

    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block=None):
        df_in = data_block[CONSUMES[0]] # noqa

    def consumes(self, name_list=None):
        return CONSUMES
