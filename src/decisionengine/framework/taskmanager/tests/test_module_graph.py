# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import patch

from decisionengine.framework.taskmanager.module_graph import ensure_no_circularities


def produces_from_dict(*configs):
    result = {}
    for config in configs:
        for name, module_config in config.items():
            result.update(dict.fromkeys(module_config.get("produces"), name))
    return result, []


def consumes_from_dict(*configs):
    result = {}
    for config in configs:
        for name, module_config in config.items():
            result[name] = set(module_config.get("consumes"))
    return result, []


@patch.multiple(
    "decisionengine.framework.taskmanager.module_graph",
    _produced_products=produces_from_dict,
    _consumed_products=consumes_from_dict,
)
def test_ensure_no_circularities_correct_order():
    sources = {"source": {"produces": ["a", "b"]}}
    transforms = {
        "b_do_first": {"consumes": ["a"], "produces": ["c"]},
        "a_do_second": {"consumes": ["b", "c"], "produces": ["d"]},
    }
    publishers = {"pub": {"consumes": ["d"]}}

    sorted_transforms = ensure_no_circularities(sources, transforms, publishers)
    assert list(sorted_transforms.keys()) == ["b_do_first", "a_do_second"]
