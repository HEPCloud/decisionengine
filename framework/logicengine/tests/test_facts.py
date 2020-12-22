from decisionengine.framework.logicengine.BooleanExpression import BooleanExpression
import pytest


def test_simple_fact():
    fact = BooleanExpression("z < 100")
    assert fact.required_names == ["z"]
    assert fact.evaluate({"z": 50}) is True
    assert fact.evaluate({"z": 100}) is False
    assert fact.evaluate({"z": 200}) is False


def test_compound_fact():
    fact = BooleanExpression("z < 100 and a == 4")
    assert set(fact.required_names) == {"z", "a"}
    assert fact.evaluate({"z": 50, "a": 4}) is True
    assert fact.evaluate({"z": 100, "a": 4}) is False
    assert fact.evaluate({"z": 200, "a": 4}) is False
    assert fact.evaluate({"z": 200, "a": 5}) is False
    assert fact.evaluate({"z": 100, "a": 5}) is False
    assert fact.evaluate({"z": 50, "a": 5}) is False


def test_fact_with_nested_names():
    fact = BooleanExpression("z > 100 and b.c == 10")
    assert set(fact.required_names) == {"z", "b"}


# We need to use this helper function to make sure the name np is not
# seen in the context of the use of the facts.
def make_db(maximum):
    import numpy as np
    return {"vals": np.arange(maximum)}


def test_fact_using_numpy_array():
    fact = BooleanExpression("vals.sum() > 40")
    assert fact.required_names == ["vals"]
    assert fact.evaluate(make_db(3)) is False
    assert fact.evaluate(make_db(10)) is True


def test_fact_using_numpy_function():
    fact = BooleanExpression("np.sum(vals) > 40")
    assert set(fact.required_names) == {"vals", "np"}
    with pytest.raises(Exception, match="name 'np' is not defined"):
        fact.evaluate(make_db(3))
