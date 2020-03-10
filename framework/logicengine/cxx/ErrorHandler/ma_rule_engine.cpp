#include <ErrorHandler/ma_rule_engine.h>

using fhicl::ParameterSet;

using namespace novadaq::errorhandler;

ma_rule_engine::ma_rule_engine(Json::Value const& facts,
                               Json::Value const& rules)
{
  auto fact_names = facts.getMemberNames();
  auto const rule_names = rules.getMemberNames();

  // find all facts from the rule's actions
  for (std::string const& name : rule_names) {
    ParameterSet rule = rules[name];

    if (rule.isMember("facts")) {
      for (auto const& f : rule["facts"]) {
        fact_names.emplace_back(f.asString());
      }
    }

    // FIXME: What happens if a fact is specified that doesn't exist?
  }

  // create all facts
  for (auto const& name : fact_names) {
    Fact const c{name};

    // push the condition to the container, and parse the test function
    auto it = cmap.emplace(name, c).first;

    // init after the condition has been inserted into the map
    it->second.init();
  }

  for (std::string const& rule_name : rule_names) {
    // construct the rule object
    ma_rule const r{rule_name};

    // push the rule to the container
    auto it = rmap.emplace(rule_name, r).first;

    // Parse the fact expression.  This is done in a two-step method
    // (init the object, push into container then parse) because the
    // parse process involves updating the factss notification list
    // which needs the pointer to the ma_rule object. Therefore we
    // push the ma_rule object into the container first, then do the
    // parse.

    ParameterSet rule = rules[rule_name];

    std::vector<std::string> actions;
    std::vector<std::string> false_actions;
    std::vector<std::string> facts;

    for (auto const& action : rule["actions"])
      actions.emplace_back(action.asString());

    for (auto const& action : rule["false_actions"])
      false_actions.emplace_back(action.asString());

    for (auto const& fact : rule["facts"])
      facts.emplace_back(fact.asString());

    it->second.parse(rule["expression"].asString(),
                     actions,
                     false_actions,
                     facts,
                     cmap);
  }

  for (auto& pr : cmap)
    pr.second.sort_notify_lists();
}

void
ma_rule_engine::execute(std::map<std::string, bool> const& fact_vals,
                        std::map<std::string, strings_t>& actions,
                        std::map<std::string, std::map<string_t, bool>>& facts)
{
  // reaction starters
  conds_t status;

  // loop through facts
  for (auto const& pr : fact_vals) {
    fact_map_t::iterator cit = cmap.find(pr.first);

    if (cit == cmap.end()) throw std::runtime_error("invalid fact name");

    cit->second.force(pr.second, status);
  }

  // merge notification lists from reaction starters
  auto notify_status = merge_notify_list(status);

  // prepare for the new facts
  std::map<string_t, std::map<string_t, bool>>
    new_facts;                            // rule -> { f1 : true, f2 : false }
  std::map<string_t, bool> new_fact_vals; // fact -> bool

  // loop to update status, and store the new facts into the new_facts map
  evaluate_rules(notify_status, actions, new_facts);

  // exam the new facts
  for (auto const& rfs : new_facts) {
    for (auto const& f : rfs.second) {
      new_fact_vals.emplace(f.first, f.second);
    }
  }

  // insert the new facts into the facts map
  facts.insert(new_facts.begin(), new_facts.end());

  // if there's any new fact values, we should call the execute again
  if (!new_fact_vals.empty()) { execute(new_fact_vals, actions, facts); }

  // Reset the rules
  for (auto& pr : rmap)
    pr.second.reset();
}

void
ma_rule_engine::evaluate_rules(
  notify_list_t& notify_status,
  std::map<string_t, strings_t>& actions,
  std::map<string_t, std::map<string_t, bool>>& facts)
{
  notify_list_t::iterator it = notify_status.begin();

  for (; it != notify_status.end(); ++it) {
    if (!(*it)->evaluable()) continue;

    if ((*it)->evaluate()) {
      // form the actions
      actions.emplace((*it)->name(), (*it)->get_action_names());

      // for the new facts
      std::map<string_t, bool> rule_facts;
      auto const& rule_fact_names = (*it)->get_chained_fact_names();

      for (auto const& name : rule_fact_names)
        rule_facts.emplace(name, true);

      facts.emplace((*it)->name(), rule_facts);
    }
    else {
      // form the actions from rule's false actions
      actions.emplace((*it)->name(), (*it)->get_false_action_names());

      // still need to form the facts, but with false values
      std::map<string_t, bool> rule_facts;
      auto const& rule_fact_names = (*it)->get_chained_fact_names();

      for (auto const& name : rule_fact_names)
        rule_facts.emplace(name, false);

      facts.emplace((*it)->name(), rule_facts);
    }
  }
}

notify_list_t
ma_rule_engine::merge_notify_list(conds_t const& c_list)
{
  notify_list_t result;
  conds_t::const_iterator it = c_list.begin();
  for (; it != c_list.end(); ++it) {
    notify_list_t notify((*it)->get_notify_list());
    result.merge(notify);
    result.unique();
  }
  return result;
}
