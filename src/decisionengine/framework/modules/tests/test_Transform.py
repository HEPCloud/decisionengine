# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules.Transform import Transform


def test_transform_structure():
    """
    The module.Transform itself is a bit of a skeleton...
    """
    params = {"1": 1, "2": 2, "channel_name": "test"}
    test_transform = Transform(params)
    assert test_transform.get_parameters() == {"1": 1, "2": 2, "channel_name": "test"}

    test_transform.set_data_block("example")
    assert test_transform.get_data_block() == "example"

    assert test_transform._consumes == {}
    assert test_transform._produces == {}
    test_transform.transform()
