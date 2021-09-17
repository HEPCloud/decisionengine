import pandas as pd
import pytest

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


@pytest.fixture()
def myengine():
    facts = {"f1": "val > 10"}
    rules = {"r1": {"expression": "f1", "actions": ["a1", "a2"]}}
    yield LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})


def test_rule_that_fires(myengine):
    db = {"val": 20}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is True

    result = myengine.evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert actions["r1"] == ["a1", "a2"]
    assert len(actions) == 1
    assert newfacts.empty

    result = myengine.evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert actions["r1"] == ["a1", "a2"]
    assert len(actions) == 1
    assert newfacts.empty


def test_rule_that_does_not_fire(myengine):
    """Rules that do not fire do not create entries in the returned
    actions and newfacts.
    """
    db = {"val": 3}
    ef = myengine.evaluate_facts(db)
    assert ef["f1"] is False

    result = myengine.evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert newfacts.empty

    result = myengine.evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, pd.DataFrame)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert newfacts.empty
