# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd
import pytest

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


@pytest.fixture()
def myengine():
    facts = {"f1": "y > 10", "f2": "vals.one.sum() > 10"}
    rules = {"r1": {"expression": "f1 and f2", "actions": ["a1", "a2"]}}
    yield LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})


def mydata(y):
    """Return a 'datablock' surrogate carrying a Pandas DataFrame, and a
    parameter named 'y' with value y.
    """
    data = {
        "one": pd.Series([1.0, 5.0, 3.0, 10.0], index=["a", "b", "c", "d"]),
        "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
    }
    db = {}
    db["vals"] = pd.DataFrame(data)
    db["y"] = y
    return db


def test_rule_that_fires(myengine):
    db = mydata(20)
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is True
    assert ef["f2"] is True

    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert actions["r1"] == ["a1", "a2"]
    assert len(actions) == 1
    assert newfacts.empty

    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert newfacts.empty


def test_rule_that_does_not_fire(myengine):
    """Rules that do not fire do not create entries in the returned
    actions and newfacts.
    """
    db = mydata(3)
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is False
    assert ef["f2"] is True

    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert newfacts.empty

    actions, newfacts = myengine.evaluate(db)
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert newfacts.empty
