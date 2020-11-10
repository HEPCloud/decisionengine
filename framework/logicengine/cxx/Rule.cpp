#include "Rule.h"
#include "ma_parse.h"

#include <stdexcept>

using namespace logic_engine;

Rule::Rule(string_t const& rule_name) : name_{rule_name} {}

void
Rule::parse(string_t const& fact_expr,
            strings_t const& actions,
            strings_t const& false_actions,
            strings_t const& facts,
            fact_map_t& fact_map)
{
  if (!parse_fact_expr(fact_expr, fact_map, this))
    throw std::runtime_error(std::string("rule parsing failed: ") + fact_expr);

  // actions
  str_actions_ = actions;
  str_false_actions_ = false_actions;
  str_facts_ = facts;
}

Fact*
Rule::insert_fact_ptr(string_t const& name, fact_map_t& cond_map)
{
  // the fact has already been added
  {
    auto it = facts_.find(name);
    if (it != facts_.end()) { return it->second; }
  }

  // look for the cond in the rule_engine container
  auto it = cond_map.find(name);
  if (it == cond_map.end()) // name not found
    throw std::runtime_error("insert_cond_ptr: condition " + name +
                             " not found");

  // put this rule to the status notification list of the condition
  it->second.push_rule(this);

  // register the condition in the rule
  facts_.emplace(name, &it->second);
  return &it->second;
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
