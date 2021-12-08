# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import ast
import pickle
import zlib

from decisionengine.framework.dataspace import datablock


def test_zdumps():
    zbytes = datablock.zdumps({"a": {"b": "c"}})
    value = pickle.loads(zlib.decompress(zbytes))

    assert value == {"a": {"b": "c"}}


def test_zloads():
    zbytes = zlib.compress(pickle.dumps({"a": {"b": "c"}}))
    value = datablock.zloads(zbytes)
    assert value == {"a": {"b": "c"}}

    zbytes = pickle.dumps({"a": {"b": "c"}})
    value = datablock.zloads(zbytes.decode("latin1"))
    assert value == {"a": {"b": "c"}}

    zbytes = pickle.dumps({"a": {"b": "c"}})
    value = datablock.zloads(zbytes)
    assert value == {"a": {"b": "c"}}


def test_compress():
    zbytes = datablock.compress(
        {
            "pickled": True,
            "value": pickle.dumps({"a": {"b": "c"}}, protocol=pickle.HIGHEST_PROTOCOL),
        }
    )
    value = ast.literal_eval(datablock.decompress(zbytes))
    value = datablock.zloads(value.get("value"))
    assert value == {"a": {"b": "c"}}

    zbytes = datablock.compress(
        {
            "pickled": True,
            "value": zlib.compress(pickle.dumps({"a": {"b": "c"}}, protocol=pickle.HIGHEST_PROTOCOL), 9),
        }
    )
    value = ast.literal_eval(datablock.decompress(zbytes))
    value = datablock.zloads(value.get("value"))
    assert value == {"a": {"b": "c"}}

    value = str({"a": {"b": "c"}}).encode("latin1")
    value = ast.literal_eval(datablock.decompress(value))
    assert value == {"a": {"b": "c"}}
