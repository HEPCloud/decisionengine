from decisionengine.framework.modules import Publisher

CONSUMES = ["bar"]


class PublisherNOP(Publisher.Publisher):

    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block=None):
        df_in = data_block[CONSUMES[0]] # nopep8

    def consumes(self, name_list=None):
        return CONSUMES
