import ast
import pickle
import zlib
import unittest

from decisionengine.framework.dataspace import datablock


class TestDatablock(unittest.TestCase):

    def setUp(self):
        self.obj = {'a': {'b': 'c'}}

    def tearDown(self):
        pass

    def test_compress(self):
        zbytes = datablock.compress({'pickled': True,
                                     'value': pickle.dumps(self.obj,
                                                           protocol=pickle.HIGHEST_PROTOCOL)})
        value = ast.literal_eval(datablock.decompress(zbytes))
        value = datablock.zloads(value.get('value'))
        self.assertEqual(value, self.obj)

        zbytes = datablock.compress({'pickled': True,
                                     'value': zlib.compress(pickle.dumps(self.obj,
                                                                         protocol=pickle.HIGHEST_PROTOCOL), 9)})
        value = ast.literal_eval(datablock.decompress(zbytes))
        value = datablock.zloads(value.get('value'))
        self.assertEqual(value, self.obj)


if __name__ == "__main__":
    unittest.main()
