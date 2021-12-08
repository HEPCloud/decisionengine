# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# A test for testing test modules [sigh]

from .DynamicPublisher import DynamicPublisher
from .DynamicSource import DynamicSource
from .DynamicTransform import DynamicTransform


def test_dynamic_source():
    dyn = DynamicSource({"data_product_name": "a"})
    rc = dyn.acquire()
    assert rc == {"a": 1}


def test_dynamic_transform():
    dyn = DynamicTransform({"data_product_name": "b", "consumes": ["a1", "a2"]})
    rc = dyn.transform({"a1": 4, "a2": 3})
    assert rc == {"b": 7}


def test_dynamic_publisher():
    dyn = DynamicPublisher({"consumes": ["a1", "a2"], "expects": 7})
    dyn.publish({"a1": 4, "a2": 3})
