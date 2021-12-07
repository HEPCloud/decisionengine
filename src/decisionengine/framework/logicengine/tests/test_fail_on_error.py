# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

from decisionengine.framework.logicengine.LogicEngine import LogicEngine


def logic_engine_with_fact(fact):
    facts = {"f1": fact}
    rules = {"r1": {"expression": "f1"}}
    return LogicEngine({"facts": facts, "rules": rules, "channel_name": "test"})


def test_true_literal_fact():
    engine = logic_engine_with_fact("fail_on_error(True)")
    facts = engine.evaluate_facts({})
    assert facts == {"f1": True}


def test_false_literal_fact():
    engine = logic_engine_with_fact("fail_on_error(False)")
    facts = engine.evaluate_facts({})
    assert facts == {"f1": False}


def test_true_fact():
    engine = logic_engine_with_fact("fail_on_error(1 < 2)")
    facts = engine.evaluate_facts({})
    assert facts == {"f1": True}


def test_false_fact_with_spaces():
    engine = logic_engine_with_fact(" fail_on_error ( 2 < 1 )")
    facts = engine.evaluate_facts({})
    assert facts == {"f1": False}


def test_misspecified_fact():
    engine = logic_engine_with_fact("val > 10")
    with pytest.raises(NameError, match="name 'val' is not defined"):
        engine.evaluate_facts({"var": 20})


def test_fact_with_misspecified_attribute():
    class MissingValue:
        pass

    engine = logic_engine_with_fact("val.does_not_exist()")
    with pytest.raises(Exception, match="'MissingValue' object has no attribute 'does_not_exist'"):
        engine.evaluate_facts({"val": MissingValue()})


def test_conditional_fact():
    engine = logic_engine_with_fact("val[0] if val else False")
    facts = engine.evaluate_facts({"val": []})
    assert facts == {"f1": False}


def test_index_error():
    engine = logic_engine_with_fact("val[0] == 42")
    with pytest.raises(IndexError, match="list index out of range"):
        engine.evaluate_facts({"val": []})


def test_fail_on_error(caplog):
    engine = logic_engine_with_fact("fail_on_error(val[0])")
    facts = engine.evaluate_facts({"val": []})
    assert facts == {"f1": False}
    assert "list index out of range" in caplog.text
