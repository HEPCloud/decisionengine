from decisionengine.framework.logicengine.LogicEngine import LogicEngine
import pytest

@pytest.fixture
def myengine():
    facts = {"f1": "val > 10"}
    rules = {}
    rules["r1"] = {"expression": "f1", "actions": ["a1"], "facts": ["f2"]}
    rules["r2"] = {"expression": "f2", "actions": ["a2"], "facts": ["f3"]}
    rules["r3"] = {"expression": "f3", "facts": ["f4"]}
    rules["r4"] = {"expression": "f4", "actions": ["a4"], "false_actions": ["fa4"]}
    
    return LogicEngine({"facts": facts, "rules": rules})

def test_rule_that_fires():
    db = {"val": 20}
    ef = myengine().evaluate_facts(db)
    assert ef["f1"] is True
    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert len(actions) == 4
    assert actions["r1"] == ["a1"]
    assert actions["r2"] == ["a2"]
    assert actions["r3"] == []
    assert actions["r4"] == ["a4"]

    assert len(newfacts) == 4
    assert newfacts["r1"] == {"f2": True}
    assert newfacts["r2"] == {"f3": True}
    assert newfacts["r3"] == {"f4": True}
    assert newfacts["r4"] == {}

def test_rule_that_does_not_file():
    db = {"val": 5}
    ef = myengine().evaluate_facts(db)
    assert ef["f1"] is False
    result = myengine().evaluate(db)
    assert isinstance(result, dict)
    assert len(result) == 2
    actions = result["actions"]
    newfacts = result["newfacts"]
    assert isinstance(actions, dict)
    assert isinstance(newfacts, dict)
    assert len(actions) == 4
    assert actions["r1"] == []
    assert actions["r2"] == []
    assert actions["r3"] == []
    assert actions["r4"] == ["fa4"]

    assert len(newfacts) == 4
    assert newfacts["r1"] == {"f2": False}
    assert newfacts["r2"] == {"f3": False}
    assert newfacts["r3"] == {"f4": False}
    assert newfacts["r4"] == {}
