from decisionengine.framework.modules import Module

class Transform(Module.Module):
    def __init__(self, set_of_parameters):
        Module.Module.__init__(self, set_of_parameters)

    """
    name_list: A list of the data product names that
    the Transform will consume
    """
    def consumes(self,name_list):
        print "Called Transform.consumes"
        self.name_list = name_list

    """
    name_schema_id_list: a list of dictionariescontaining
    the data product name and a pointer to a schema
    """
    def produces(self, name_schema_id_list):
        print "Called Transform.produces"
        return None

    """
    decide: The action function for a Transform. Will
    retrieve from the DataBlock the data products
    listed by consumes and performs algorithmic
    operation on them. The Transform will issue a
    DataBlock "put" transaction for each of the data
    products promised in the produces list
    """
    def transform(self):
        print "Called Transform.transform"
        return True
