# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import ast

import pytest

from decisionengine.framework.logicengine.BooleanExpression import function_name_from_call, LogicError


def test_error_conditions():
    with pytest.raises(LogicError, match=r"not a call node"):
        function_name_from_call("asdf")
    with pytest.raises(LogicError, match=r"unknown node type"):
        function_name_from_call(ast.Call("print", "", ""))
