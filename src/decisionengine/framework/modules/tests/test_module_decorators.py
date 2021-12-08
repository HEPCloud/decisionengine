# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

from decisionengine.framework.modules import Publisher, Source
from decisionengine.framework.modules.Module import verify_products
from decisionengine.framework.modules.Source import Parameter


def test_multiple_consumes_declarations():
    with pytest.raises(Exception, match="@consumes has already been called"):

        @Publisher.consumes(a=int)
        @Publisher.consumes(b=float)
        class _(Publisher.Publisher):
            pass


def test_multiple_produces_declarations():
    with pytest.raises(Exception, match="@produces has already been called"):

        @Source.produces(c=str)
        @Source.produces(d=bool)
        class _(Source.Source):
            pass


def test_wrong_product_names():
    @Source.produces(a=str)
    class BMaker(Source.Source):
        def __init__(self, config):
            super().__init__(config)

        def acquire(self):
            return {"b": ""}

    maker = BMaker({"channel_name": "test"})
    expected_err_msg = (
        "The following products were not produced:\n"
        + " - 'a' of type 'str'\n\n"
        + "The following products were not declared:\n"
        + " - 'b' of type 'str'"
    )
    with pytest.raises(Exception, match=expected_err_msg):
        verify_products(maker, maker.acquire())


def test_wrong_product_types():
    @Source.produces(a=str, b=int)
    class AMaker(Source.Source):
        def __init__(self, config):
            super().__init__(config)

        def acquire(self):
            return {"a": 42, "b": 17}

    maker = AMaker({"channel_name": "test"})
    expected_err_msg = "The following products have the wrong types:\n" + r" - 'a' \(expected 'str', got 'int'\)"
    with pytest.raises(Exception, match=expected_err_msg):
        verify_products(maker, maker.acquire())


def test_supports_config():
    expected_err_msg = (
        "An error occurred while processing the parameter 'conflicting_types':\n"
        + "The specified type 'int' conflicts with the type of the default value "
        + r"'hello' \(type 'str'\)"
    )
    with pytest.raises(Exception, match=expected_err_msg):

        @Source.supports_config(Parameter("conflicting_types", type=int, default="hello"))
        class _(Source.Source):
            pass
