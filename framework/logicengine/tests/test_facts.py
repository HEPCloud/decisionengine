from decisionengine.framework.logicengine.NamedFact import NamedFact
import pytest

def test_simple_fact():
    fact = NamedFact("f1", "z < 100")
    assert fact.name == "f1"
    assert fact.evaluate({"z": 50}) is True
    assert fact.evaluate({"z": 100}) is False
    assert fact.evaluate({"z": 200}) is False
    assert set(fact.required_names()) is set(["z"])
    assert fact.required_names() == ["z"]

def test_compound_fact():
    fact = NamedFact("f2", "z < 100 and a == 4")
    assert fact.name == "f2"
    assert fact.evaluate({"z": 50, "a": 4}) is True
    assert fact.evaluate({"z": 100, "a": 4}) is False
    assert fact.evaluate({"z": 200, "a": 4}) is False
    assert fact.evaluate({"z": 200, "a": 5}) is False
    assert fact.evaluate({"z": 100, "a": 5}) is False
    assert fact.evaluate({"z": 50, "a": 5}) is False
    assert set(fact.required_names()) == set(["z", "a"])


def test_fact_with_nested_names():
    fact = NamedFact("f", "z > 100 and b.c == 10")
    assert fact.name == "f"
    assert set(fact.required_names()) == set(["z", "b"])

# We need to use this helper function to make sure the name np is not
# seen in the context of the use of the facts.
def make_db(maximum):
    import numpy as np
    return {"vals": np.arange(maximum)}

def test_fact_using_numpy_array():
    fact = NamedFact("f3", "vals.sum() > 40")
    assert fact.name == "f3"
    #fact = NamedFact("f3", "np.sum(vals) > 40")
    assert fact.evaluate(make_db(3)) is False
    assert fact.evaluate(make_db(10)) is True
    assert fact.required_names() == ["vals"]

def test_fact_using_numpy_function():
    fact = NamedFact("f3", "np.sum(vals) > 40")
    assert fact.name == "f3"
    assert set(fact.required_names()) == set(["vals", "np"])
    with pytest.raises(BaseException):
        fact.evaluate(make_db(3))

def test_no_numpy_found():
    with pytest.raises(NameError):
        import numpy as np
        dummy = np.arange(10)
