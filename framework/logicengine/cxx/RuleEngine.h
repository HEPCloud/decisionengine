#ifndef logicengine_cxx_RuleEngine_h
#define logicengine_cxx_RuleEngine_h

#include "Fact.h"
#include "Rule.h"
#include "ma_types.h"

namespace logic_engine {

  class RuleEngine {
  public:
    RuleEngine(boost::python::dict const& facts,
               boost::python::dict const& rules);

    void execute(std::map<std::string, bool> const& fact_vals,
                 std::map<std::string, strings_t>& actions,
                 std::map<std::string, std::map<string_t, bool>>& facts);

  private:
    rules_t merge_rules(facts_t const& facts);

    void evaluate_rules(rules_t rules,
                        std::map<string_t, strings_t>& actions,
                        std::map<string_t, std::map<string_t, bool>>& facts);

    fact_map_t facts_{};
    rule_map_t rules_{};
  };

} // end of namespace logic_engine

#endif /* logicengine_cxx_RuleEngine_h */

// Local Variables:
// mode: c++
// End:
