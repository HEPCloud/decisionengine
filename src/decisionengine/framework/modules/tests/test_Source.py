from decisionengine.framework.modules.Source import Source

def test_source_structure():
    """
    The module.Source itself is a bit of a skeleton...
    """
    test_source = Source((1, 2, 3))
    assert test_source.get_parameters() == (1, 2, 3)

    test_source.set_data_block('example')
    assert test_source.get_data_block() == 'example'

    test_source.produces('asdf')
    test_source.acquire()
    test_source.post_create('asdf')
