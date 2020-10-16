#ifndef logicengine_cxx_ma_boolean_cond_h
#define logicengine_cxx_ma_boolean_cond_h

#include "Fact.h"
#include "ma_types.h"

#include <list>
#include <memory>

namespace logic_engine {

  class Rule;
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
    bool evaluate() const;

    void insert_expr(ma_boolean_expr const& expr);
    void insert_expr_neg(ma_boolean_expr const& expr);

    // insert a primitive fact
    void
    insert(Fact* ci)
    {
      fact = ci;
      neg_cond = false;
    }

    void
    insert_neg(Fact* ci)
    {
      fact = ci;
      neg_cond = true;
    }

  private:
    // type of this element condition
    cond_type_t cond_type{COND};

    // negtive condition ( !cond )
    bool neg_cond{false};

    // case COND: this boolean cond is the boolean value of a Fact
    //   a pointer to the condition in the one big condition container
    //   DOES NOT own the condition
    Fact* fact{nullptr};

    // shared_ptr to an boolean expression
    //   a smart pointer to an boolean expression object
    //   DOES own the expression object
    std::shared_ptr<ma_boolean_expr> expr{};
  };

  typedef std::list<ma_boolean_cond> boolean_conds_t;

} // end of namespace logic_engine

#endif /* logicengine_cxx_ma_boolean_cond_h */

// Local Variables:
// mode: c++
// End:
