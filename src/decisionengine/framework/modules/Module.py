class Module(object):
    """
    A skelaton of a module
    """

    def __init__(self, set_of_parameters):
        self.parameters = set_of_parameters
        self.data_block = None

    def get_parameters(self):
        return self.parameters

    def get_data_block(self):
        return self.data_block

    def set_data_block(self, data_block):
        self.data_block = data_block
