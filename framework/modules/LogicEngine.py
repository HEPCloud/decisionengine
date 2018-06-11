from decisionengine.framework.modules import Module

class LogicEngine(Module.Module):
    def __init__(self, set_of_parameters):
        Module.Module.__init__(self, set_of_parameters)

    def evaluate(self, data_block):
        print "Called LogicEngine.evaluate"
        return True
