from decisionengine.framework.taskmanager.TaskManager import _create_module_instance
from decisionengine.framework.modules.Source import Source

import pytest


def test_no_module():
    config = {'module': 'decisionengine.framework.taskmanager.tests.NoSource',
              'parameters': {}}
    with pytest.raises(RuntimeError, match="Could not find a decision-engine 'Source'"):
        _create_module_instance(config, Source)

def test_too_many_modules():
    config = {'module': 'decisionengine.framework.taskmanager.tests.TwoSources',
              'parameters': {}}
    with pytest.raises(RuntimeError, match="Found more than one decision-engine 'Source'"):
        _create_module_instance(config, Source)

def test_select_one_of_two_modules():
    config = {'module': 'decisionengine.framework.taskmanager.tests.TwoSources',
              'name': 'Source2',
              'parameters': {}}
    _create_module_instance(config, Source)
