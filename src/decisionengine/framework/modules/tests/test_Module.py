from decisionengine.framework.modules.Module import Module

def test_module_structure():
    """
    The module.Module itself is a bit of a skeleton...
    """
    test_module = Module((1, 2, 3))
    assert test_module.get_parameters() == (1, 2, 3)

    test_module.set_data_block('example')
    assert test_module.get_data_block() == 'example'
