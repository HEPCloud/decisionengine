# A NamedFact represents one fact known to the LogicEngine.

# The current intent is that user-supplied facts will be expressions
# that can make use of objects that are numpy arrays, or pandas
# dataframes, and can call methods on those obhjects. However, facts
# will not directly make use of functions from either numpy or pandas.
#
# Example expressions for facts:
#   "vals.sum() > 40"   # OK, vals can be a numpy.ndarray
#   "np.sum(vals) > 40" # WRONG, illegal call to np.sum

import ast

# If support for direct use of numpy and pandas functions becomes
# wanted, then uncomment the following two import statements, and
# switch the definition of facts_globals to the commented-out
# version.#

import numpy as np
import pandas as pd
facts_globals = {}
#facts_globals = {"np": np, "pd": pd}


class LogicError(TypeError):
    pass


def function_name_from_call(callnode):
    print "In name_from_call: ", callnode
    if (not isinstance(callnode, ast.Call)):
        raise LogicError("not a call node")
    if (isinstance(callnode.func, ast.Name)):
        # This really is a function name
        return callnode.func.id
    if (isinstance(callnode.func, ast.Attribute)):
        # This is the name of a function argument
        # not the name of a function.
        return None
    raise LogicError("unknown node type")

class NamedFact(object):
    def __init__(self, name, expr):
        self.name = name
        source = 'string'
        mode = 'eval'
        syntax_tree = ast.parse(expr, source, mode)
        all_names = [n.id for n in ast.walk(syntax_tree) if isinstance(n, ast.Name)]
        func_names = [function_name_from_call(n) for n in ast.walk(syntax_tree) if isinstance(n, ast.Call)]

        self.names = list(set(all_names) - set(func_names))
        self.expr = compile(syntax_tree, source, mode)

    def required_names(self):
        """Return a list of the names that must be in data passed to evaluate
        for the call to evaluate to work.
        """
        return self.names

    def evaluate(self, d):
        """Return the truth value of this fact, in the context
        of the given data 'd'."""
        return bool(eval(self.expr, facts_globals, d))

    def __str__(self):
        return "name: %s  expression: %s" % (self.name, self.expr)
