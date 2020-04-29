import ast
import pickle
import zlib

from decisionengine.framework.dataspace import datablock


class TestDatablock:

    def __init__(self):
        self.obj = {'a': {'b': 'c'}}
        pass

    def test_compress(self):
        zstring = datablock.compress({'pickled': True,
                                      'value': pickle.dumps(self.obj,
                                                            protocol=pickle.HIGHEST_PROTOCOL)})
        value = ast.literal_eval(datablock.decompress(zstring))
        value = datablock.zloads(value.get('value'))
        assert value, self.obj

        zstring = datablock.compress({'pickled': True,
                                      'value': zlib.compress(pickle.dumps(self.obj,
                                                                          protocol=pickle.HIGHEST_PROTOCOL), 9)})
        value = ast.literal_eval(datablock.decompress(zstring))
        value = datablock.zloads(value.get('value'))
        assert value, self.obj
