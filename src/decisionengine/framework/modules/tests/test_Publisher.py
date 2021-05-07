from decisionengine.framework.modules.Publisher import Publisher

def test_publisher_structure():
    """
    The module.publisher itself is a bit of a skeleton...
    """
    test_publisher = Publisher((1, 2, 3))
    assert test_publisher.get_parameters() == (1, 2, 3)

    test_publisher.set_data_block('example')
    assert test_publisher.get_data_block() == 'example'

    assert test_publisher._consumes == {}
    test_publisher.publish()
    test_publisher.publish(data_block='asdf')
    test_publisher.shutdown()
