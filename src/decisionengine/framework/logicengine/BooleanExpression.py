# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# A BooleanExpression represents one expression known to the LogicEngine.

# The intent is that user-supplied expressions can make use of objects
# that are numpy arrays, or pandas dataframes, and can call methods on
# those objects. However, expressions will not directly make use of
# functions from either numpy or pandas.
#
# Example expressions:
#   "vals.sum() > 40"   # OK, vals can be a numpy.ndarray
#   "np.sum(vals) > 40" # WRONG, illegal call to np.sum

import ast
import re

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

# If support for direct use of numpy and pandas functions is desired,
# import the numpy and pandas modules and adjust the facts_globals:
#   facts_globals.update(np=np, pd=pd)


_facts_globals = {}
_re = re.compile(r"fail_on_error\s*\(\s*(.*)\s*\)")

logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


def maybe_fail_on_error(expr):
    match = re.fullmatch(_re, expr)
    if match is None:
        return expr, False
    return match.group(1), True


class LogicError(TypeError):
    pass


def function_name_from_call(callnode):
    try:
        if not isinstance(callnode, ast.Call):
            raise LogicError("not a call node")
        if isinstance(callnode.func, ast.Name):
            # This really is a function name
            return callnode.func.id
        if isinstance(callnode.func, ast.Attribute):
            # This is the name of a function argument, not the name of a function.
            return None
        else:
            raise LogicError("unknown node type")
    except Exception:  # pragma: no cover
        logger.exception("Unexpected error!")
        raise


class BooleanExpression:
    def __init__(self, expr):
        self.expr_str, self.fail_on_error = maybe_fail_on_error(str.strip(expr))
        source = "string"
        mode = "eval"
        syntax_tree = None
        try:
            syntax_tree = ast.parse(self.expr_str, source, mode)
        except Exception:
            logger.exception("The following expression string could not be parsed:\n" f"'{self.expr_str}'")
            raise
        all_names = [n.id for n in ast.walk(syntax_tree) if isinstance(n, ast.Name)]
        func_names = [function_name_from_call(n) for n in ast.walk(syntax_tree) if isinstance(n, ast.Call)]

        self.required_names = list(set(all_names) - set(func_names))
        self.expr = compile(syntax_tree, source, mode)

    def evaluate(self, d):
        """Return the evaluated Boolean value of this expression in the context
        of the given data 'd'."""
        logger.debug("calling BooleanExpression::evaluate()")
        try:
            return bool(eval(self.expr, _facts_globals, d))
        except Exception:
            if self.fail_on_error:
                logger.exception(
                    "The following exception was suppressed, and the " "Boolean expression will evaluate to False."
                )
                return False
            raise

    def __str__(self):  # pragma: no cover
        return f"{self.expr_str}"
