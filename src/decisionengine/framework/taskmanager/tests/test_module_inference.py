# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

from decisionengine.framework.modules.Source import Source
from decisionengine.framework.taskmanager.module_graph import _create_module_instance


def test_no_module():
    config = {"module": "decisionengine.framework.taskmanager.tests.NoSource", "parameters": {}}
    channelname = "test"
    with pytest.raises(RuntimeError, match="Could not find a decision-engine 'Source'"):
        _create_module_instance(config, Source, channelname)


def test_too_many_modules():
    config = {"module": "decisionengine.framework.taskmanager.tests.TwoSources", "parameters": {}}
    channelname = "test"
    with pytest.raises(RuntimeError, match="Found more than one decision-engine 'Source'"):
        _create_module_instance(config, Source, channelname)


def test_select_one_of_two_modules():
    config = {"module": "decisionengine.framework.taskmanager.tests.TwoSources", "name": "Source2", "parameters": {}}
    channelname = "test"
    _create_module_instance(config, Source, channelname)
