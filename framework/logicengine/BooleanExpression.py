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

# If support for direct use of numpy and pandas functions becomes
# wanted, then uncomment the following two import statements, and
# switch the definition of facts_globals to the commented-out
# version.#

facts_globals = {}
# facts_globals = {"np": np, "pd": pd}


class LogicError(TypeError):
    pass


def function_name_from_call(callnode):
    if not isinstance(callnode, ast.Call):
        raise LogicError("not a call node")
    if isinstance(callnode.func, ast.Name):
        # This really is a function name
        return callnode.func.id
    if isinstance(callnode.func, ast.Attribute):
        # This is the name of a function argument, not the name of a function.
        return None
    raise LogicError("unknown node type")


class BooleanExpression:
    def __init__(self, expr):
        self.expr_str = expr
        source = 'string'
        mode = 'eval'
        syntax_tree = ast.parse(expr, source, mode)
        all_names = [n.id for n in ast.walk(syntax_tree) if isinstance(n, ast.Name)]
        func_names = [function_name_from_call(n) for n in ast.walk(syntax_tree) if isinstance(n, ast.Call)]

        self.required_names = list(set(all_names) - set(func_names))
        self.expr = compile(syntax_tree, source, mode)

    def evaluate(self, d):
        """Return the evaluated Boolen value of this expression in the context
        of the given data 'd'."""
        return bool(eval(self.expr, facts_globals, d))

    def __str__(self):
        return f"{self.expr_str}"
