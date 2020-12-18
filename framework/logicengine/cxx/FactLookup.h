#ifndef logicengine_cxx_FactLookup_h
#define logicengine_cxx_FactLookup_h

// =====================================================================

// The FactLookup class establishes a policy for looking up fact based
// on the given name, such that an unambiguous fact can be chosen.  To
// wit, the first fact with a given name is the one that is used in
// the evaluation of all subsequent facts.
//
// As an example, consider the following configuration:
//
//   facts: {
//     should_publish: "(True)"
//   },
//   rules: {
//     publish_1: {
//       expression: "(should_publish)",
//       facts: ["should_publish"]
//     },
//     publish_2: {
//       expression: "(should_publish)",
//       facts: ["should_publish"]
//     }
//   }
//
// In the above, the first fact to be evaluated will always be the
// top-level facts (i.e. those not encapsulated by the 'rules' table).
// The rules labeled 'publish_1' and 'publish_2' both rely on the
// 'should_publish' fact in their expressions, and they in turn create
// their own facts with the same name.  FactLookup ensures that
// 'publish_1' and 'publish_2' will both use the evaluated fact from
// the top-level 'facts' table.

// =====================================================================

#include "Fact.h"

#include <cassert>
#include <map>

namespace logic_engine {

  class FactLookup {
    using list_entry_t = std::pair<std::string, Fact>;
    using fact_list_t = std::vector<list_entry_t>;
    using container_t = std::map<std::string, fact_list_t>;

  public:
    using iterator = fact_list_t::iterator;

    void add_facts(std::vector<std::string> const& fact_names,
                   std::string const& rule_name = {})
    {
      if (frozen_) {
        throw std::runtime_error("Fact lookup object is frozen and cannot be extended.");
      }

      for (auto const& fact_name : fact_names) {
        facts_[fact_name].emplace_back(rule_name, Fact{});
      }
    }

    void freeze()
    {
      frozen_ = true;
    }

    Fact* find_fact(std::string const& fact_name)
    {
      auto it = facts_.find(fact_name);
      if (it == facts_.end())
        throw std::runtime_error("fact '" + fact_name + "' not found");

      assert(not it->second.empty());
      return &it->second[0].second;
    }

    Fact* find_exact(std::string const& fact_name, std::string const& rule_name)
    {
      auto it = facts_.find(fact_name);
      if (it == facts_.end())
        throw std::runtime_error("fact '" + fact_name + "' not found");

      auto& facts_for_name = it->second;
      auto fit = std::find_if(facts_for_name.begin(),
                              facts_for_name.end(),
                              [&rule_name](list_entry_t const& t) { return t.first == rule_name; });
      if (fit == facts_for_name.end())
        throw std::runtime_error("fact '" + fact_name + "' for rule '" + rule_name + "' not found");

      return &fit->second;
    }

  private:
    container_t facts_;
    bool frozen_{false};
  };

} // end of namespace logic_engine

#endif /* logicengine_cxx_FactLookup_h */

// Local Variables:
// mode: c++
// End:
