from decisionengine.framework.logicengine.LogicEngine import LogicEngine


def test_duplicate_fact_names():
    facts = {"should_publish": "(True)"}
    rules = {}
    rules["publish_1"] = {"expression": "(should_publish)",
                          "facts": ["should_publish"]}
    rules["publish_2"] = {"expression": "(should_publish)",
                          "facts": ["should_publish"]}
    channelname = "test"
    le = LogicEngine({"facts": facts, "rules": rules}, channelname)
    ef = le.evaluate_facts({})
    assert ef["should_publish"]
    result = le.evaluate({})
    newfacts = result["newfacts"]
    assert len(newfacts) == 2
