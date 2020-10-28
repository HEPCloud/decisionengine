#ifndef logicengine_cxx_Fact_h
#define logicengine_cxx_Fact_h

#include "ma_types.h"

#include <algorithm>
#include <map>
#include <vector>

namespace logic_engine {

  class Fact {
  public:
    void
    set_value(bool const value)
    {
      value_ = value;
    }

    bool
    value() const
    {
      return value_;
    }

    void
    push_rule(Rule* rule)
    {
      if (std::find(affected_rules_.begin(), affected_rules_.end(), rule) ==
          affected_rules_.end())
        affected_rules_.push_back(rule);
    }

    void
    sort_rules()
    {
      affected_rules_.sort();
    }

    rules_t
    get_rules() const
    {
      return affected_rules_;
    }

  private:
    bool value_{false};
    rules_t affected_rules_{};
  };

  using Facts = std::vector<Fact*>;
  using fact_map_t = std::map<string_t, Fact>;

} // end of namespace logic_engine

#endif /* logicengine_cxx_Fact_h */

// Local Variables:
// mode: c++
// End:
