#ifndef logicengine_cxx_RuleEngine_h
#define logicengine_cxx_RuleEngine_h

#include <pybind11/pybind11.h>

#include "Fact.h"
#include "FactLookup.h"
#include "Rule.h"
#include "ma_types.h"

namespace logic_engine {

  class RuleEngine {
  public:
    RuleEngine(pybind11::dict const& facts,
               pybind11::dict const& rules);

    void execute(std::pair<std::string, std::map<std::string, bool>> const& fact_vals_per_rule,
                 std::map<std::string, strings_t>& actions,
                 std::map<std::string, std::map<string_t, bool>>& facts);

  private:
    rules_t merge_rules(facts_t const& facts);

    void evaluate_rules(rules_t rules,
                        std::map<string_t, strings_t>& actions,
                        std::map<string_t, std::map<string_t, bool>>& facts);

    FactLookup facts_{};
    rule_map_t rules_{};
  };

} // end of namespace logic_engine

#endif /* logicengine_cxx_RuleEngine_h */

// Local Variables:
// mode: c++
// End:
