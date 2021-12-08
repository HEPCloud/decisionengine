# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules.Publisher import Publisher


def test_publisher_structure():
    """
    The module.publisher itself is a bit of a skeleton...
    """
    params = {"1": 1, "2": 2, "channel_name": "test"}
    test_publisher = Publisher(params)
    assert test_publisher.get_parameters() == {"1": 1, "2": 2, "channel_name": "test"}

    test_publisher.set_data_block("example")
    assert test_publisher.get_data_block() == "example"

    assert test_publisher._consumes == {}
    test_publisher.publish()
    test_publisher.publish(data_block="asdf")
    test_publisher.shutdown()
