from decisionengine.framework.logicengine.Rule import Rule

from toposort import toposort_flatten


class FactLookup:
    '''
    Establishes a policy for looking up a fact based on the given name.

    To wit, the first fact with a given name is the one that is used
    in the evaluation of all subsequent facts.

    As an example, consider the following configuration:

      facts: {
        should_publish: "(True)"
      },
      rules: {
        publish_1: {
          expression: "(should_publish)",
          facts: ["should_publish"]
        },
        publish_2: {
          expression: "(should_publish)",
          facts: ["should_publish"]
        }
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
        self.facts = {}
        for fact_name in fact_names:
            self.facts[fact_name] = ['']

        # Add new facts from rules
        for rule_name, rule_cfg in rules_cfg.items():
            for fact_name in rule_cfg.get("facts", []):
                if fact_name in self.facts:
                    self.facts[fact_name].append(rule_name)
                else:
                    self.facts[fact_name] = [rule_name]

    def sorted_rules(self, rules_cfg):
        initial_rules = {name: Rule(name, cfg) for name, cfg in rules_cfg.items()}
        dependencies = {}
        for name, rule in initial_rules.items():
            dependencies[name] = set()
            required_facts = rule.expr.names
            for fact in required_facts:
                rule_for_fact = self.rule_for(fact)
                if rule_for_fact:
                    dependencies[name].add(rule_for_fact)

        ordered_dependencies = toposort_flatten(dependencies)
        sorted_rules = []
        for rule in ordered_dependencies:
            sorted_rules.append(initial_rules[rule])
        return sorted_rules


    def rule_for(self, fact_name):
        return self.facts[fact_name][0]
