#include <ErrorHandler/ma_parse.h>
#include <ErrorHandler/ma_rule.h>

using namespace novadaq::errorhandler;

ma_rule::ma_rule(string_t const& rule_name)
  : name_{rule_name}
{}

void
ma_rule::parse(string_t const& fact_expr,
               strings_t const& actions,
               strings_t const& false_actions,
               strings_t const& facts,
               fact_map_t& fact_map)
{
  if (!parse_fact_expr(fact_expr, fact_map, this))
    throw std::runtime_error(std::string("rule parsing failed: ") + fact_expr);

  // actions
  str_actions = actions;
  str_false_actions = false_actions;
  str_facts = facts;

  // init
  domain_ = ma_domain_ctor_any(conditions.size());
}

cond_idx_t
ma_rule::insert_fact_ptr(string_t const& name, fact_map_t& cond_map)
{
  // the fact has already been added
  {
    idx_t::const_iterator it = conditions_idx.find(name);
    if (it != conditions_idx.end()) {
      return cond_idx_t(conditions[it->second], it->second);
    }
  }

  // look for the cond in the rule_engine container
  fact_map_t::iterator it = cond_map.find(name);

  if (it == cond_map.end()) // name not found
    throw std::runtime_error("insert_cond_ptr: condition " + name +
                             " not found");

  // put this rule to the status notification list of the condition
  it->second.push_notify_status(this);

  // register the condition in the rule
  conditions.push_back(&it->second);

  size_t idx = conditions.size() - 1;

  conditions_idx.emplace(name, idx);

  return cond_idx_t(&it->second, idx);
}

bool
ma_rule::recursive_evaluate(ma_domain& value,
                            size_t n)
{
  // get range
  ma_cond_range src(D_NIL, D_NIL);
  ma_cond_range target(D_NIL, D_NIL);

  conditions[n]->get_cond_range(domain_[n], src, target);

  value[n].first = 0;
  value[n].second = 0;

  if (n != 0) {
    if (recursive_evaluate(value, n + 1)) return true;
  }
  else {
    if (boolean_evaluate(value)) return true;
  }

  return false;
}

bool
ma_rule::evaluate()
{
  // holds the one possible set of value
  ma_domain value = ma_domain_ctor_null(1);
  return recursive_evaluate(value, 0);
}

bool
ma_rule::evaluable() const
{
  for (auto const fact : conditions)
    if (!fact->get_defined()) return false;

  return true;
}

bool
ma_rule::boolean_evaluate(ma_domain& value)
{
  // make sure all facts are defined
  for (auto const fact : conditions)
    if (!fact->get_defined()) return false;

  // evaluate as true with given set of values
  return boolean_expr.evaluate(value, domain_);
}

void
ma_rule::reset()
{
  // clear user function state
  boolean_expr.reset();

  for (auto* condition : conditions) {
    condition->reset();
  }
}

