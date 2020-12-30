#include "Rule.h"

#include "FactLookup.h"
#include "ma_parse.h"

#include <stdexcept>

using namespace logic_engine;

Rule::Rule(string_t const& rule_name) : name_{rule_name} {}

void
Rule::parse(string_t const& fact_expr,
            strings_t const& actions,
            strings_t const& false_actions,
            strings_t const& facts,
            FactLookup& fact_map)
{
  if (!parse_fact_expr(fact_expr, fact_map, this))
    throw std::runtime_error(std::string("rule parsing failed: ") + fact_expr);

  // actions
  str_actions_ = actions;
  str_false_actions_ = false_actions;
  str_facts_ = facts;
}

Fact*
Rule::insert_fact_ptr(string_t const& fact_name, FactLookup& fact_lookup)
{
  // the fact has already been added
  {
    auto it = facts_.find(fact_name);
    if (it != facts_.end()) { return it->second; }
  }

  // look for the fact in the rule_engine's fact-lookup manager
  auto fact = fact_lookup.find_fact(fact_name);

  // put this rule to the status notification list of the condition
  fact->push_rule(this);

  // register the condition in the rule
  facts_.emplace(fact_name, fact);
  return fact;
}

bool
Rule::recursive_evaluate(size_t n)
{
  if (n != 0) {
    if (recursive_evaluate(n + 1)) return true;
  }
  else {
    if (boolean_evaluate()) return true;
  }

  return false;
}

bool
Rule::evaluate()
{
  return recursive_evaluate(0);
}

bool
Rule::boolean_evaluate()
{
  return boolean_expr.evaluate();
}
