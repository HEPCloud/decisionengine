# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from itertools import chain

import pandas

from decisionengine.framework.logicengine.BooleanExpression import BooleanExpression
from decisionengine.framework.logicengine.RuleEngine import RuleEngine
from decisionengine.framework.modules.Module import Module


def passthrough_configuration(publisher_names):
    """Assembles logic-engine configuration to unconditionally execute all publishers."""
    if len(publisher_names) == 0:
        return {}
    return {
        "logic_engine": {
            "module": "decisionengine.framework.logicengine.LogicEngine",
            "parameters": {
                "facts": {},
                "rules": {"r1": {"expression": "True", "actions": list(publisher_names)}},
            },
        }
    }


class LogicEngine(Module):
    def __init__(self, cfg):
        super().__init__(cfg)
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
        return (actions, self._create_facts_dataframe(newfacts))

    def _create_facts_dataframe(self, newfacts):
        """
        Convert newfacts dict in format below to dataframe with columns
        ['rule_name', 'fact_name', fact_value']

        facts dict format:

        .. code-block:: json

            {
                "newfacts": {
                    "publish_glidein_requests": {
                        "allow_hpc_new": true,
                        "allow_foo": true
                    },
                    "dummy_rule": {
                        "dummy_new_fact": true
                    }
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
        facts = {"rule_name": rule_name, "fact_name": fact_name, "fact_value": fact_value}
        return pandas.DataFrame(facts)
