import unittest

from decisionengine.framework.engine.DecisionEngine import parse_program_options

class TestStartup(unittest.TestCase):

    def test_default_config(self):
        arguments = []
        self.assertEqual(parse_program_options(arguments), {'server_address': ['localhost', 8888]}, msg="default config incorrect")

    def test_change_port(self):
        arguments = ['--port=54321', ]
        self.assertEqual(parse_program_options(arguments), {'server_address': ['localhost', 54321]}, msg="port override fails")


if __name__ == "__main__":
    unittest.main()
