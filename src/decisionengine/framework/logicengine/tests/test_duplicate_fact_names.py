# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


def test_duplicate_fact_names():
    facts = {"should_publish": "(True)"}
    rules = {}
    rules["publish_1"] = {"expression": "(should_publish)", "facts": ["should_publish"]}
    rules["publish_2"] = {"expression": "(should_publish)", "facts": ["should_publish"]}
    le = LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})
    ef = le.evaluate_facts({})
    assert ef["should_publish"]
    actions, newfacts = le.evaluate({})
    assert len(newfacts) == 2
