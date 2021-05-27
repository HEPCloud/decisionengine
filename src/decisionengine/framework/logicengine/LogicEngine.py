import structlog
import pandas
from itertools import chain

from decisionengine.framework.logicengine.RuleEngine import RuleEngine
from decisionengine.framework.logicengine.BooleanExpression import BooleanExpression
from decisionengine.framework.modules.Module import Module


class LogicEngine(Module):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.logger = structlog.getLogger("decision_engine")
        self.logger = self.logger.bind(module=__name__.split(".")[-1])
        self.facts = {name: BooleanExpression(expr) for name, expr in cfg["facts"].items()}
        self.rule_engine = RuleEngine(cfg["facts"].keys(), cfg["rules"])

    def produces(self):
        self.logger.debug("in LE::produces()")
        return ["actions", "newfacts"]

    def consumes(self):
        """Return the names of all the items that must be in the DataBlock for
        the rules to be evaluated.
        """
        self.logger.debug("in LE::consumes()")
        list_of_lists = [f.required_names for f in self.facts.values()]
        return list(set(chain(*list_of_lists)))

    def evaluate_facts(self, db):
        """
        :type db: :obj:`DataBlock`
        :arg db: Products used to evaluate facts.
        :rtype: dict
        :returns: Evaluated fact values (e.g. True or False) for each fact name.
        """
        try:
            return {name: f.evaluate(db) for name, f in self.facts.items()}
        except NameError as e:
            msg = f"The following error was encountered: {e}\n"
            if len(db) == 0:
                msg += "No fact names are available."
            else:
                msg += "Allowed fact names are:\n"
                for key in db:
                    msg += "  '" + key + "'\n"
            self.logger.error(msg)
            raise e
        except Exception as e:
            self.logger.exception("Unexpected exception while evaluating facts.")
            raise e

    def evaluate(self, db):
        """
        Evaluate our facts and rules, in the context of the given data.
        db can be any mappable, in particular a DataBlock or dictionary.

        :type db: :obj:`DataBlock`
        :arg db: Products used to evaluate facts.
        """
        self.logger.info("LE: calling evaluate_facts")

        evaluated_facts = self.evaluate_facts(db)
        for key, val in evaluated_facts.items():
            self.logger.info(f"Evaluated Fact: {key} -> Value: {val} -> TypeOf(Value): {type(val)}")

        # Process rules
        self.logger.info("LE: calling execute")
        actions, newfacts = self.rule_engine.execute(evaluated_facts)
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
        self.logger.debug("in LE::_create_facts_dataframe")
        # Extract new facts from le_result
        # Dataframe column values for Facts
        rule_name = []
        fact_name = []
        fact_value = []

        for rule in newfacts:
            facts = newfacts[rule]
            rule_name += [rule] * len(facts)
            fact_name += facts.keys()
            fact_value += facts.values()
        facts = {
            'rule_name': rule_name,
            'fact_name': fact_name,
            'fact_value': fact_value
        }
        return pandas.DataFrame(facts)
