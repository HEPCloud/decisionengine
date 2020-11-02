#ifndef logicengine_cxx_Rule_h
#define logicengine_cxx_Rule_h

// from novadaq
#include "Fact.h"
#include "ma_boolean_expr.h"
#include "ma_types.h"

#include <map>
#include <memory>
#include <sys/time.h>

namespace logic_engine {

  // MsgAnalyzer Rule
  class Rule {
  public:
    explicit Rule(string_t const& name);

    void parse(string_t const& cond_expr,
               strings_t const& actions,
               strings_t const& false_actions,
               strings_t const& facts,
               fact_map_t& cond_map_ptr);

    strings_t const&
    get_action_names(bool const result) const
    {
      return result ? str_actions_ : str_false_actions_;
    }

    strings_t const&
    get_chained_fact_names() const
    {
      return str_facts_;
    }

    // public method, call to evaluate the boolean expression
    bool evaluate();

    // get fields
    const string_t&
    name() const
    {
      return name_;
    }

    // ----------------------------------------------------------------
    //

    // called by the parser to set the boolean expression
    void
    set_boolean_expr(ma_boolean_expr const& expr)
    {
      boolean_expr = expr;
    }

    // called by the parser to push a cond_ptr to the container
    Fact* insert_fact_ptr(string_t const& name, fact_map_t& cond_map);

  private:
    // recursive evaluation function
    //   n:      depth of the recursion
    //   return: true if new alarm found
    bool recursive_evaluate(size_t n);

    bool boolean_evaluate();

    std::map<string_t, Fact*> facts_{};

    string_t name_;
    ma_boolean_expr boolean_expr{};

    strings_t str_actions_{};
    strings_t str_false_actions_{};
    strings_t str_facts_{};
  };

  typedef std::map<string_t, Rule> rule_map_t;

} // end of namespace logic_engine

#endif /* logicengine_cxx_Rule_h */

// Local Variables:
// mode: c++
// End:
