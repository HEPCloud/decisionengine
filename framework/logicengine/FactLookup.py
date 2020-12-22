from decisionengine.framework.logicengine.Rule import Rule

from toposort import toposort_flatten

import logging

_TOP_LEVEL = ''  # Indicates facts not contained by rules


class FactLookup:
    '''
    Establishes a policy for looking up a fact based on the given name.

    To wit, the first fact with a given name is the one that is used
    in the evaluation of all subsequent facts.

    As an example, consider the following configuration:

      facts: {
        should_publish: "(True)",
      },
      rules: {
        publish_1: {
          expression: "should_publish",
          facts: ["should_publish"]
        },
        publish_2: {
          expression: "should_publish",
          actions: ["go_to_press"]
          facts: ["should_publish"]
        }
        retract: {
          expression: "not should_publish",
          facts: ["should_retract"]
      }

    In the above, the first fact to be evaluated will always be the
    top-level facts (i.e. those not encapsulated by the 'rules' table).
    The rules labeled 'publish_1' and 'publish_2' both rely on the
    'should_publish' fact in their expressions, and they in turn create
    their own facts with the same name.  FactLookup ensures that
    'publish_1' and 'publish_2' will both use the evaluated fact from
    the top-level 'facts' table.
    '''
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

        logging.getLogger().debug(f"Registered the following facts:\n{self.facts}")

    def sorted_rules(self, rules_cfg):
        initial_rules = {name: Rule(name, cfg) for name, cfg in rules_cfg.items()}
        dependencies = {}
        for name, rule in initial_rules.items():
            dependencies[name] = set()
            required_facts = rule.expr.required_names
            for fact in required_facts:
                rule_for_fact = self.rule_for(fact)
                if rule_for_fact:
                    dependencies[name].add(rule_for_fact)

        ordered_dependencies = toposort_flatten(dependencies)
        logging.getLogger().debug(f"Calculated the following order for evaluating rules:\n{ordered_dependencies}")
        return [initial_rules[rule] for rule in ordered_dependencies]

    def rule_for(self, fact_name):
        return self.facts[fact_name][0]
