from decisionengine.framework.modules import SourceProxy

PRODUCES = ["foo"]


class WorkingSourceProxy(SourceProxy.SourceProxy):

    def __init__(self, config):
        super().__init__(config)

    def produces(self):
        return PRODUCES

    def acquire(self):
        data = super(WorkingSourceProxy, self).acquire()
        return data
