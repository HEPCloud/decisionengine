#include "RuleEngine.h"

#include <pybind11/stl.h>

using namespace logic_engine;
namespace py = pybind11;

namespace {
  std::vector<std::string>
  to_strings(py::list const& py_list)
  {
    return py::cast<std::vector<std::string>>(py_list);
//      py::stl_input_iterator<std::string>{py_list},
//      py::stl_input_iterator<std::string>{});
  }

  std::vector<std::string>
  to_strings_or_empty(py::dict const& rule, std::string const& key)
  {
    if (rule.contains(key)) {
      py::list tmp_list = rule[key.c_str()];
      return to_strings(tmp_list);
    }
    return {};
  }
}

RuleEngine::RuleEngine(py::dict const& facts_dict,
                       py::dict const& rules)
{
  auto fact_names = to_strings(facts_dict.attr("keys")());
  auto const rule_names = to_strings(rules.attr("keys")());

  // find all facts from the rule's actions
  for (std::string const& name : rule_names) {
    py::dict const rule = rules[name.c_str()];

    if (rule.contains("facts")) {
      py::list const fact_list = rule["facts"];
      auto const facts_from_rule = to_strings(fact_list);
      for (std::string const& f : facts_from_rule) {
        fact_names.emplace_back(f);
      }
    }

    // FIXME: What happens if a fact is specified that doesn't exist?
  }

  // create all facts
  for (auto const& name : fact_names) {
    facts_.emplace(name, Fact{});
  }

  for (std::string const& rule_name : rule_names) {
    Rule const r{rule_name};
    auto it = rules_.emplace(rule_name, r).first;

    // Parse the fact expression.  This is done in a two-step method
    // (init the object, push into container then parse) because the
    // parse process involves updating the facts notification list
    // which needs the pointer to the Rule object. Therefore we
    // push the Rule object into the container first, then do the
    // parse.

    py::dict rule = rules[rule_name.c_str()];

    it->second.parse(py::cast<std::string>(rule["expression"]),
                     to_strings_or_empty(rule, "actions"),
                     to_strings_or_empty(rule, "false_actions"),
                     to_strings_or_empty(rule, "facts"),
                     facts_);
  }

  for (auto& pr : facts_)
    pr.second.sort_rules();
}

void
RuleEngine::execute(std::map<std::string, bool> const& fact_vals,
                    std::map<std::string, strings_t>& actions,
                    std::map<std::string, std::map<string_t, bool>>& facts)
{
  // Prepare initial facts
  facts_t initial_facts;
  for (auto const& pr : fact_vals) {
    auto cit = facts_.find(pr.first);
    if (cit == facts_.end()) throw std::runtime_error("invalid fact name");

    cit->second.set_value(pr.second);
    initial_facts.push_back(&cit->second);
  }

  // Rules may generate new facts; we prepare for that here.
  std::map<string_t, std::map<string_t, bool>>
    new_facts;                            // rule name -> { f1 : true, f2 : false }
  std::map<string_t, bool> new_fact_vals; // fact name -> bool

  evaluate_rules(merge_rules(initial_facts), actions, new_facts);

  facts.insert(new_facts.begin(), new_facts.end());

  // Recursively call execute for any new facts
  for (auto const& rfs : new_facts) {
    new_fact_vals.insert(rfs.second.cbegin(), rfs.second.cend());
  }

  if (!new_fact_vals.empty()) {
    execute(new_fact_vals, actions, facts);
  }
}

void
RuleEngine::evaluate_rules(rules_t rules,
                           std::map<string_t, strings_t>& actions,
                           std::map<string_t, std::map<string_t, bool>>& facts)
{
  for (Rule* rule : rules) {
    std::map<string_t, bool> rule_facts;
    auto const result = rule->evaluate();
    actions.emplace(rule->name(), rule->get_action_names(result));
    auto const& rule_fact_names = rule->get_chained_fact_names();

    for (auto const& name : rule_fact_names)
      rule_facts.emplace(name, result);

    facts.emplace(rule->name(), rule_facts);
  }
}

rules_t
RuleEngine::merge_rules(facts_t const& facts)
{
  rules_t result;
  for (auto* fact : facts) {
    result.merge(fact->get_rules());
    result.unique();
  }
  return result;
}
