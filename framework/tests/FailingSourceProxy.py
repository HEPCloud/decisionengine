from decisionengine.framework.modules import SourceProxy

PRODUCES = ["foo"]


class FailingSourceProxy(SourceProxy.SourceProxy):

    def __init__(self, config):
        super().__init__(config)

    def produces(self):
        return PRODUCES

    def acquire(self):
        raise RuntimeError("Failing source proxy test")
