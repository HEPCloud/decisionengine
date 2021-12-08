# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd
import pytest

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


@pytest.fixture()
def myengine():
    facts = {"f1": "val > 10"}
    rules = {}
    rules["r1"] = {"expression": "not f1", "actions": ["a1"]}
    rules["r2"] = {"expression": "not (f1)", "actions": ["a2"]}
    yield LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})


def test_rule_that_fires(myengine):
    db = {"val": 5}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is False
    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert actions["r1"] == ["a1"]
    assert actions["r2"] == ["a2"]
    assert len(actions) == 2
    assert newfacts.empty


def test_rule_that_does_not_fire(myengine):
    """Rules that do not fire do not create entries in the returned
    actions and newfacts.
    """
    db = {"val": 20}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is True
    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 2
    assert actions["r1"] == []
    assert actions["r2"] == []
    assert newfacts.empty
