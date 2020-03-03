#include <ErrorHandler/ma_rule_engine.h>

using fhicl::ParameterSet;

using namespace novadaq::errorhandler;

ma_rule_engine::ma_rule_engine(Json::Value const& facts,
                               Json::Value const& rules)
{
  // fact names and rule names
  cnames = facts.getMemberNames();
  rnames = rules.getMemberNames();

  // find all facts from the rule's actions
  for (size_t i = 0; i < rnames.size(); ++i) {
    ParameterSet rule = rules[rnames[i]];

    if (rule.isMember("facts")) {
      for (auto const& f : rule["facts"]) {
        cnames.emplace_back(f.asString());
      }
    }
  }

  // create all facts
  for (size_t i = 0; i < cnames.size(); ++i) {
    // construct the condition object
    ma_condition c(cnames[i]);

    // push the condition to the container, and parse the test function
    auto it = cmap.emplace(cnames[i], c).first;

    // init after the condition has been inserted into the map
    it->second.init();
  }

  // go through all rules
  for (size_t i = 0; i < rnames.size(); ++i) {
    ParameterSet rule = rules[rnames[i]];

    // construct the rule object
    ma_rule r(rnames[i],
              rnames[i],
              false //, rule["repeat_alarm"].asBool()
              ,
              0 //, rule["holdoff"].asInt()
    );

    // push the rule to the container
    auto it = rmap.emplace(rnames[i], r).first;

    // parse the condition expression and alarm message
    // this is done in a two-step method (init the object, push into container
    // then parse) because the parse process involves updating the conditions
    // notification list which needs the pointer to the ma_rule object. There-
    // fore we push the ma_rule object into the container first, then do the
    // parse

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
                     rule["message"].asString(),
                     actions,
                     false_actions,
                     facts,
                     &cmap);
  }

  // for all conditions sort their notification lists
  cond_map_t::iterator it = cmap.begin();
  for (; it != cmap.end(); ++it)
    it->second.sort_notify_lists();
}

void
ma_rule_engine::execute(std::map<std::string, bool> const& fact_vals,
                        std::map<std::string, strings_t>& actions,
                        std::map<std::string, std::map<string_t, bool>>& facts)
{
  // reaction starters
  conds_t status;
  conds_t source;
  conds_t target;

  // loop through conditions
  for (std::map<std::string, bool>::const_iterator it = fact_vals.begin();
       it != fact_vals.end();
       ++it) {
    cond_map_t::iterator cit = cmap.find(it->first);

    if (cit == cmap.end()) throw std::runtime_error("invalid fact name");

    cit->second.force(it->second, status, source, target);
  }

  // notification mechanism

  // merge notification lists from reaction starters
  notify_list_t notify_status;
  notify_list_t notify_domain;

  merge_notify_list(notify_status, status, STATUS_NOTIFY);
  merge_notify_list(notify_domain, source, SOURCE_NOTIFY);
  merge_notify_list(notify_domain, target, TARGET_NOTIFY);

  // update domains
  evaluate_rules_domain(notify_domain);

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
}

void
ma_rule_engine::evaluate_rules_domain(notify_list_t& notify_domain)
{
  notify_list_t::iterator it = notify_domain.begin();
  for (; it != notify_domain.end(); ++it)
    (*it)->evaluate_domain();
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

void
ma_rule_engine::merge_notify_list(notify_list_t& n_list,
                                  conds_t const& c_list,
                                  notify_t type)
{
  conds_t::const_iterator it = c_list.begin();
  for (; it != c_list.end(); ++it) {
    notify_list_t notify((*it)->get_notify_list(type));
    n_list.merge(notify);
    n_list.unique();
  }
}
