
class Module(object):


    def __init__(self, set_of_parameters):
        self.parameters = set_of_parameters

    def get_paramaters(self):
        return self.parameters

    def get_data_bock(self):
        return self.data_block

    def set_data_bock(self, data_block):
        self.data_block = data_block
