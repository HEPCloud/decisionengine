#ifndef ERROR_HANDLER_MA_RULE_H
#define ERROR_HANDLER_MA_RULE_H

// from novadaq
#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_boolean_expr.h>
#include <ErrorHandler/ma_types.h>

#include <map>
#include <memory>
#include <sys/time.h>

namespace novadaq {
  namespace errorhandler {

    // MsgAnalyzer Rule
    class ma_rule {
    public:
      explicit ma_rule(string_t const& name);

      void parse(string_t const& cond_expr,
                 strings_t const& actions,
                 strings_t const& false_actions,
                 strings_t const& facts,
                 fact_map_t& cond_map_ptr);

      strings_t const&
      get_action_names() const
      {
        return str_actions;
      }

      /*!*/ strings_t const&
      get_false_action_names() const
      {
        return str_false_actions;
      }

      /*!*/ strings_t const&
      get_chained_fact_names() const
      {
        return str_facts;
      }

      // public method, call to check if all the dependent facts(conditions) are defined
      // note, only applicable when all the facts are non-parameterized (per_source/target = false)
      /*!*/ bool evaluable() const;

      // public method, call to evaluate the boolean expression
      /*!*/ bool evaluate();

      // get fields
      const string_t&
      name() const
      {
        return name_;
      }

      // reset the rule to its ground state ( reset domains )
      void reset();

      // ----------------------------------------------------------------
      //

      // called by the parser to set the boolean expression
      void
      set_boolean_expr(ma_boolean_expr const& expr)
      {
        boolean_expr = expr;
      }

      // called by the parser to push a cond_ptr to the container
      cond_idx_t insert_fact_ptr(string_t const& name, fact_map_t& cond_map);

    private:
      // recursive evaluation function
      //   value:  specific value set in the given domain
      //   domain: the input domain where values are allowed
      //   n:      depth of the recursion
      //   return: true if new alarm found
      bool recursive_evaluate(ma_domain& value, size_t n);

      // evaluate the boolean expression with a given set of inputs
      //   value:  the input values for each condition
      bool boolean_evaluate(ma_domain& value);

      Facts conditions{};
      idx_t conditions_idx{};

      string_t name_;
      string_t condition_expr{};

      ma_boolean_expr boolean_expr{};

      ma_domain domain_{};

      strings_t str_actions{};
      strings_t str_false_actions{};
      strings_t str_facts{};
    };

    typedef std::shared_ptr<ma_rule> rule_sp;
    typedef std::map<string_t, ma_rule> rule_map_t;

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
