from decisionengine.framework.logicengine.NamedFact import NamedFact


class Rule:
    '''
    In-memory representation of logic-engine rule, relying on parsing utilities in NamedFact.
    '''
    def __init__(self, rule_name, rule_cfg):
        self.name = rule_name
        self.expr = NamedFact(rule_name, rule_cfg["expression"])
        self.actions = rule_cfg.get("actions")
        self.false_actions = rule_cfg.get("false_actions")
        self.new_facts = rule_cfg.get("facts")

    def evaluate(self, evaluated_facts):
        return self.expr.evaluate(evaluated_facts)
