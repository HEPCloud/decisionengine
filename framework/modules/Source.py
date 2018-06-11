from decisionengine.framework.modules import Module

class Source(Module.Module):
    def __init__(self, set_of_parameters):
        Module.Module.__init__(self, set_of_parameters)

    # name_schema_id_list: a list of dictionaries containing
    # the data product name and a pointer to a schema
    def produces(self, name_schema_id_list):
        print "Called Source.produces"
        return None

    # acquire: The action function for a source. Will
    # retrieve data from external sources and issue a
    # DataBlock "put" transaction.
    def acquire(self):
        print "Called Source.acquires"
        return None
