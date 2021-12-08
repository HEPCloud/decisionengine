# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.logicengine.BooleanExpression import BooleanExpression


class Rule:
    """
    In-memory representation of logic-engine rule, relying on parsing utilities in BooleanExpression.
    """

    def __init__(self, rule_name, rule_cfg):
        self.name = rule_name
        self.expr = BooleanExpression(rule_cfg["expression"])
        self.actions = rule_cfg.get("actions")
        self.false_actions = rule_cfg.get("false_actions")
        self.new_facts = rule_cfg.get("facts")

    def evaluate(self, evaluated_facts):
        """
        Evaluates a compiled expression given the supplied facts.

        :type evaluated_facts: dict
        :arg evaluated_facts: Initial fact values (e.g. True or False) for each fact name.
        :rtype: bool
        """
        return self.expr.evaluate(evaluated_facts)

    def __str__(self):  # pragma: no cover
        return (
            f"name: {self.name}\n"
            f"expression: '{self.expr}'\n"
            f"actions: {self.actions}\n"
            f"false_actions: {self.false_actions}\n"
            f"facts: {self.new_facts}"
        )
