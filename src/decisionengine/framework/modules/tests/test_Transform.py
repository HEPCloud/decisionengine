from decisionengine.framework.modules.Transform import Transform

def test_transform_structure():
    """
    The module.Transform itself is a bit of a skeleton...
    """
    test_transform = Transform((1, 2, 3))
    assert test_transform.get_parameters() == (1, 2, 3)

    test_transform.set_data_block('example')
    assert test_transform.get_data_block() == 'example'

    assert test_transform._consumes == {}
    assert test_transform._produces == {}
    test_transform.transform()
