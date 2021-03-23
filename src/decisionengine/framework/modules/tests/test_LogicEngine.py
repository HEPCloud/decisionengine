from decisionengine.framework.modules.LogicEngine import LogicEngine

def test_logicengine_structure():
    """
    The module.Module itself is a bit of a skeleton...
    """
    test_logicengine = LogicEngine((1, 2, 3))
    assert test_logicengine.get_parameters() == (1, 2, 3)

    test_logicengine.set_data_block('example')
    assert test_logicengine.get_data_block() == 'example'

    test_logicengine.evaluate('asdf')
