# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules.Module import Module


def test_module_structure():
    """
    The module.Module itself is a bit of a skeleton...
    """
    params = {"1": 1, "2": 2, "channel_name": "test"}
    test_module = Module(params)
    assert test_module.get_parameters() == {"1": 1, "2": 2, "channel_name": "test"}

    test_module.set_data_block("example")
    assert test_module.get_data_block() == "example"
