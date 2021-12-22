# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules.Source import Source


def test_source_structure():
    """
    The module.Source itself is a bit of a skeleton...
    """
    params = {"1": 1, "2": 2, "channel_name": "test"}
    test_source = Source(params)
    assert test_source.get_parameters() == {"1": 1, "2": 2, "channel_name": "test"}

    test_source.set_data_block("example")
    assert test_source.get_data_block() == "example"

    assert test_source._produces == {}
    test_source.acquire()
