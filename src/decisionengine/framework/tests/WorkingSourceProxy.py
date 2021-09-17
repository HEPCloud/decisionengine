from decisionengine.framework.modules import SourceProxy


class WorkingSourceProxy(SourceProxy.SourceProxy):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        return super().acquire()
