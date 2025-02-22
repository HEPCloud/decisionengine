# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import structlog

from toposort import toposort_flatten

from decisionengine.framework.logicengine.Rule import Rule
from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

_TOP_LEVEL = ""  # Indicates facts not contained by rules


class FactLookup:
    """
    Establishes a policy for looking up a fact based on the given name.

    To with, the first fact with a given name is the one that is used
    in the evaluation of all subsequent facts.

    As an example, consider the following configuration:

    .. code-block:: json

        {
            "facts": {
                "should_publish": "(True)"
            },
            "rules": {
                "publish_1": {
                    "expression": "should_publish",
                    "facts": ["should_publish"]
                },
                "publish_2": {
                    "expression": "should_publish",
                    "actions": ["go_to_press"],
                    "facts": ["should_publish"]
                },
                "retract": {
                    "expression": "not should_publish",
                    "facts": ["should_retract"]
                }
            }
        }

    In the above, the first fact to be evaluated will always be the
    top-level facts (i.e. those not encapsulated by the 'rules' table).
    The rules labeled 'publish_1' and 'publish_2' both rely on the
    'should_publish' fact in their expressions, and they in turn create
    their own facts with the same name.  FactLookup ensures that
    'publish_1' and 'publish_2' will both use the evaluated fact from
    the top-level 'facts' table.
    """

    def __init__(self, fact_names, rules_cfg):
        # For the above configuration, the 'self.facts' attribute is a dictionary of the form:
        # {
        #   'should_publish': ['', 'publish_1', 'publish_2'],
        #   'should_retract': ['retract']
        # }
        # We therefore seed the dictionary entries to contain a [_TOP_LEVEL] list for all initial facts.
        self.facts = dict.fromkeys(fact_names, [_TOP_LEVEL])

        # Add new facts from rules
        for rule_name, rule_cfg in rules_cfg.items():
            for fact_name in rule_cfg.get("facts", []):
                self.facts.setdefault(fact_name, []).append(rule_name)

        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)
        self.logger.debug(f"Registered the following facts:\n{self.facts}")

    def sorted_rules(self, rules_cfg):
        """
        Rules sorted according to rule dependencies.

        :type rules_cfg: dict
        :arg rules_cfg: rules as specified in logic-engine configuration
        :rtype: list
        :return: Rules to be evaluated by the rule engine.
        """
        initial_rules = {name: Rule(name, cfg) for name, cfg in rules_cfg.items()}
        dependencies = {}

        try:
            for name, rule in initial_rules.items():
                dependencies[name] = set()
                required_facts = rule.expr.required_names
                for fact in required_facts:
                    rule_for_fact = self.rule_for(fact)
                    if rule_for_fact:
                        dependencies[name].add(rule_for_fact)

            ordered_dependencies = toposort_flatten(dependencies)
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error!")
            raise

        self.logger.debug(f"Calculated the following order for evaluating rules:\n{ordered_dependencies}")
        return [initial_rules[rule] for rule in ordered_dependencies]

    def rule_for(self, fact_name):
        """
        Selects rule required to evaluate fact with the supplied name.

        :type fact_name: str
        :arg fact_name: Name of fact for which rule will be selected.
        :rtype: str
        :returns: Rule name
        """
        return self.facts[fact_name][0]
