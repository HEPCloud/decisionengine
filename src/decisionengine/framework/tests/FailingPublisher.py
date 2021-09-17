from decisionengine.framework.modules import Publisher


@Publisher.consumes(bar=None)
class FailingPublisher(Publisher.Publisher):
    def __init__(self, config):
        super().__init__(config)

    def publish(self, data_block):
        raise RuntimeError("Test error-handling")
