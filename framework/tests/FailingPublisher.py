from decisionengine.framework.modules import Publisher

CONSUMES = ["bar"]


class FailingPublisher(Publisher.Publisher):

    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block):
        raise RuntimeError("Test error-handling")

    def consumes(self, name_list):
        return CONSUMES
