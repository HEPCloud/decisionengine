from decisionengine.framework.logicengine.LogicEngine import LogicEngine
import pytest

def test_default_construction():
    """LogicEngine is not default constructible."""
    with pytest.raises(TypeError):
        #pylint: disable=no-value-for-parameter
        engine = LogicEngine()
        #pylint: enable=no-value-for-parameter

def test_wrong_configuration():
    """LogicEngine construction requires rules and facts;
    if we don't supply them it is an error."""
    with pytest.raises(KeyError):
        engine = LogicEngine({})

def test_trivial_configuration():
    """Logic engine constructed with trivial rules and facts."""
    cfg = {"rules": {}, "facts": {}}
    le = LogicEngine(cfg)
    assert le.produces() == ["actions", "newfacts"]
    assert le.consumes() == []

def test_configuration_with_fact_using_function():
    facts = {"f1": "len(vals) == 10"}
    rules = {"r1": {"expression": "f1", "actions": ["launch"]}}
    le = LogicEngine({"rules": rules, "facts": facts})
    assert le.produces() == ["actions", "newfacts"]
    assert le.consumes() == ["vals"]

def test_configuration_with_numy_facts():
    facts = {"f1": "vals.sum() > blob.available"}
    rules = {"r1": {"expression": "f1", "actions": ["launch"]}}
    le = LogicEngine({"rules": rules, "facts": facts})
    assert le.produces() == ["actions", "newfacts"]
    assert set(le.consumes()) == set(["vals", "blob"])
    #cfg = { "rules": {}, "facts": {} }
