#pylint: disable=no-name-in-module
from decisionengine.framework.logicengine.RE import RuleEngine
#pylint: enable=no-name-in-module
from decisionengine.framework.logicengine.NamedFact import NamedFact
from decisionengine.framework.modules.Module import Module
import json
from itertools import chain

class LogicEngine(Module, object):
    # Inheritance from object can be dropped if Module is modified to
    # inherit from object.
    def __init__(self, cfg):
        super(LogicEngine, self).__init__(cfg)
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
        print "LE: calling evaluate_facts"

        evaluated_facts = self.evaluate_facts(db)
        for key, val in evaluated_facts.items():
            print "Evaluated Fact: %s -> Value: %s -> TypeOf(Value): %s" % (key, val, type(val))

        # Process rules
        print "LE: calling execute"
        actions, newfacts = self.re.execute(evaluated_facts)
        return {"actions": actions, "newfacts": newfacts}
