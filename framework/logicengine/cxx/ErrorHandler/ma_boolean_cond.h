#ifndef ERROR_HANDLER_MA_BOOLEAN_COND_H
#define ERROR_HANDLER_MA_BOOLEAN_COND_H

#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_types.h>

#include <list>
#include <memory>

namespace novadaq {
  namespace errorhandler {

    class ma_rule;
    class ma_boolean_expr;

    //-------------------------------------------------------------------
    //
    // elementary boolean condition has three possible cases:
    //   1. '(' + boolean_expr + ')'
    //   2. primitive elementary boolean condition Cn
    //   3. non-primitive boolean condition ( COUNT(Cn.$s|t) )
    //
    //-------------------------------------------------------------------

    class ma_boolean_cond {
    public:
      // c'tor
      ma_boolean_cond()
        : cond_type(COND)
        , neg_cond(false)
        , cond_arg(cond_arg_t(cond_idx_t(NULL, 0), NONE))
        , rhv_s()
        , expr()
      {}

      // reset boolean cond
      void reset();

      // evaluation
      bool evaluate(ma_domain& value,
                    ma_domain const& domain) const;

      // insert a boolean expression
      void insert_expr(ma_boolean_expr const& expr);
      void insert_expr_neg(ma_boolean_expr const& expr);

      // insert a primitive condition
      void
      insert_cond(cond_idx_t ci)
      {
        cond_arg.first = ci;
        cond_arg.second = NONE;
        neg_cond = false;
      }

      void
      insert_cond_neg(cond_idx_t ci)
      {
        cond_arg.first = ci;
        cond_arg.second = NONE;
        neg_cond = true;
      }

    private:
      // type of this element condition
      cond_type_t cond_type;

      // negtive condition ( !cond )
      bool neg_cond;

      // case COND: this boolean cond is the boolean value of a Fact
      //   a pointer to the condition in the one big condition container
      //   DOES NOT own the condition
      cond_arg_t cond_arg;

      // case EXT_FUNCTION:
      //   op:       compare operator, <, <=, ==, !=, >=, >
      //   rhv:      righ-hand value
      //   ext_func: ptr to a customized evaluation function. use ext_func->evaluate()
      //             to evaluate
      string_t rhv_s;

      // shared_ptr to an boolean expression
      //   a smart pointer to an boolean expression object
      //   DOES own the expression object
      std::shared_ptr<ma_boolean_expr> expr;
    };

    typedef std::list<ma_boolean_cond> boolean_conds_t;

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
