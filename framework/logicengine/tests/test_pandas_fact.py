from decisionengine.framework.logicengine.LogicEngine import LogicEngine
import pytest
import pandas as pd


@pytest.fixture
def myengine():
    facts = {"f1": "y > 10", "f2": "vals.one.sum() > 10"}
    rules = {"r1": {"expression":"f1 && f2", "actions": ["a1", "a2"]}}
    return LogicEngine({"facts": facts, "rules": rules})

@pytest.fixture
def mydata(y):
    """Return a 'datablock' surrogate carrying a Pandas DataFrame, and a
    parameter named 'y' with value y.
    """
    data = {'one': pd.Series([1., 5., 3., 10.], index=['a', 'b', 'c', 'd']),
            'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    db = {}
    db["vals"] = pd.DataFrame(data)
    db["y"] = y
    return db

def test_rule_that_fires():
    db = mydata(20)
    ef = myengine().evaluate_facts(db)
    assert ef["f1"] is True
    assert ef["f2"] is True

    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert actions["r1"] == ["a1", "a2"]
    assert len(actions) == 1
    assert newfacts["r1"] == {}
    assert len(newfacts) == 1

    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert actions["r1"] == ["a1", "a2"]
    assert len(actions) == 1
    assert newfacts["r1"] == {}
    assert len(newfacts) == 1


def test_rule_that_does_not_fire():
    """Rules that do not fire do not create entries in the returned
    actions and newfacts.
    """
    db = mydata(3)
    ef = myengine().evaluate_facts(db)
    assert ef["f1"] is False
    assert ef["f2"] is True

    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert len(newfacts) == 1
    assert newfacts["r1"] == {}

    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert len(actions) == 1
    assert actions["r1"] == []
    assert len(newfacts) == 1
    assert newfacts["r1"] == {}
