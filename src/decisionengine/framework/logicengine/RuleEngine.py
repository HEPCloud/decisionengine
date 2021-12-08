# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import structlog

from decisionengine.framework.logicengine.FactLookup import FactLookup
from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME


class RuleEngine:
    """
    Engine responsible for evaluating logic-engine rules.

    This class is responsible for (a) forming a sorted set of rules
    that supports dependencies between them, and (b) evaluating the
    rules according to a specified fact-lookup policy.
    """

    def __init__(self, fact_names, rules_cfg):
        self.fact_lookup = FactLookup(fact_names, rules_cfg)
        self.rules = self.fact_lookup.sorted_rules(rules_cfg)
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)

    def execute(self, evaluated_facts):
        """
        Evaluates all rules given the supplied facts.

        :type evaluated_facts: dict
        :arg evaluated_facts: Initial fact values (e.g. True or False) for each fact name.
        :rtype: tuple
        :returns: Actions to be taken based on rule evaluation; new facts produced during that evaluation.
        """
        facts = evaluated_facts
        actions = {rule.name: [] for rule in self.rules}
        new_facts = {}

        try:
            for rule in self.rules:
                rc = rule.evaluate(facts)
                if rc and rule.actions:
                    actions[rule.name] = rule.actions
                if not rc and rule.false_actions:
                    actions[rule.name] = rule.false_actions
                if rule.new_facts:
                    new_facts_for_rule = {fact_name: rc for fact_name in rule.new_facts}
                    new_facts[rule.name] = new_facts_for_rule
                    # First instance of a fact with a given name receives precedence
                    facts = {**new_facts_for_rule, **facts}
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise
        return actions, new_facts
