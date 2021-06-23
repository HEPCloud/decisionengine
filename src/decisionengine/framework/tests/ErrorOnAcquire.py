from decisionengine.framework.modules import Source

@Source.produces(_placeholder=None)
class ErrorOnAcquire(Source.Source):

    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        raise RuntimeError("Test error-handling")


Source.describe(ErrorOnAcquire)
