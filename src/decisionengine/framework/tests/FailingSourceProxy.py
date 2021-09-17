from decisionengine.framework.modules import SourceProxy


class FailingSourceProxy(SourceProxy.SourceProxy):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        raise RuntimeError("Failing source proxy test")
