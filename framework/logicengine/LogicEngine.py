import json
import pandas
from itertools import chain

#pylint: disable=no-name-in-module
from decisionengine.framework.modules import de_logger
from decisionengine.framework.logicengine.RE import RuleEngine
#pylint: enable=no-name-in-module
from decisionengine.framework.logicengine.NamedFact import NamedFact
from decisionengine.framework.modules.Module import Module

class LogicEngine(Module, object):
    # Inheritance from object can be dropped if Module is modified to
    # inherit from object.
    def __init__(self, cfg):
        super(LogicEngine, self).__init__(cfg)
        self.logger = de_logger.get_logger()
        self.facts = [NamedFact(name, expr) for name, expr in cfg["facts"].iteritems()]

        # Only the names of facts are really needed. We pass in the
        # JSON form of the whole facts dictionary until the C++ is
        # updated to take a list of strings.
        self.re = RuleEngine(json.dumps(cfg["facts"]),
                             json.dumps(cfg["rules"]))

    def produces(self):
        return ["actions", "newfacts"]

    def consumes(self):
        """Return the names of all the items that must be in the DataBlock for
        the rules to be evaluated.
        """
        list_of_lists = [f.required_names() for f in self.facts]
        return list(set(chain(*list_of_lists)))

    def evaluate_facts(self, db):
        return {f.name: f.evaluate(db) for f in self.facts}

    def evaluate(self, db):
        """evaluate our facts and rules, in the context of the given data.
        db can be any mappable, in particular a DataBlock or dictionary."""
        self.logger.info("LE: calling evaluate_facts")

        evaluated_facts = self.evaluate_facts(db)
        for key, val in evaluated_facts.items():
            self.logger.info("Evaluated Fact: %s -> Value: %s -> TypeOf(Value): %s" % (key, val, type(val)))

        # Process rules
        self.logger.info("LE: calling execute")
        actions, newfacts = self.re.execute(evaluated_facts)
        return {"actions": actions, "newfacts": self._create_facts_dataframe(newfacts)}

    def _create_facts_dataframe(self, newfacts):
        """
        Convert newfacts dict in format below to dataframe with columns
        ['rule_name', 'fact_name', fact_value']

        facts dict format:
        'newfacts': {
            'publish_glidein_requests': {
                'allow_hpc_new': True,
                'allow_foo': True
            },
            'dummy_rule': {
                'dummy_new_fact': True
            }
        }
        """
        # Extract new facts from le_result
        # Dataframe column values for Facts
        rule_name = []
        fact_name = []
        fact_value = []

        for rule in newfacts:
            for fact in newfacts[rule]:
                rule_name.append(rule)
                fact_name.append(fact)
                fact_value.append(newfacts[rule][fact])
        facts = {
            'rule_name': rule_name,
            'fact_name': fact_name,
            'fact_value': fact_value
        }
        return pandas.DataFrame(facts)
