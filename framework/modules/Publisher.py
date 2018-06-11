from decisionengine.framework.modules import Module

class Publisher(Module.Module):
    def __init__(self, set_of_parameters):
        Module.Module.__init__(self, set_of_parameters)

    def consumes(self, name_list):
        print "Called Publisher.consumes"

    def publish(self, data_block=None):
        print "Called Publisher.publish"
