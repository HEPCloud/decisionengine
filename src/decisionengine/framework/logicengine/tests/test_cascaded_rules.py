# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd
import pytest

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


@pytest.fixture()
def myengine():
    facts = {"f1": "val > 10"}
    rules = {}
    rules["r1"] = {"expression": "f1", "actions": ["a1"], "facts": ["f2"]}
    rules["r2"] = {"expression": "f2", "actions": ["a2"], "facts": ["f3"]}
    rules["r3"] = {"expression": "f3", "facts": ["f4"]}
    rules["r4"] = {"expression": "f4", "actions": ["a4"], "false_actions": ["fa4"]}

    yield LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})


def test_rule_that_fires(myengine):
    db = {"val": 20}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is True
    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 4
    assert actions["r1"] == ["a1"]
    assert actions["r2"] == ["a2"]
    assert actions["r3"] == []
    assert actions["r4"] == ["a4"]
    assert len(newfacts) == 3
    newfacts_d = newfacts.set_index("rule_name").T.to_dict("list")

    assert newfacts_d["r1"] == ["f2", True]
    assert newfacts_d["r2"] == ["f3", True]
    assert newfacts_d["r3"] == ["f4", True]


def test_rule_that_does_not_fire(myengine):
    db = {"val": 5}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is False
    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 4
    assert actions["r1"] == []
    assert actions["r2"] == []
    assert actions["r3"] == []
    assert actions["r4"] == ["fa4"]
    assert len(newfacts) == 3
    newfacts_d = newfacts.set_index("rule_name").T.to_dict("list")

    assert newfacts_d["r1"] == ["f2", False]
    assert newfacts_d["r2"] == ["f3", False]
    assert newfacts_d["r3"] == ["f4", False]
