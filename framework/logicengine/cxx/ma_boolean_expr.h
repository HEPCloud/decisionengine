#ifndef logicengine_cxx_ma_boolean_expr_h
#define logicengine_cxx_ma_boolean_expr_h

#include "ma_boolean_andexpr.h"

namespace logic_engine {

  //-------------------------------------------------------------------
  //
  // boolean expression consists of a list of boolean and-expression
  // connected with 'OR' operator
  //
  //-------------------------------------------------------------------

  class ma_boolean_expr {
  public:
    bool evaluate() const;
    void
    insert(ma_boolean_andexpr const& andexpr)
    {
      andexprs.push_back(andexpr);
    }

  private:
    boolean_andexprs_t andexprs;
  };

} // end of namespace logic_engine

#endif /* logicengine_cxx_ma_boolean_expr_h */

// Local Variables:
// mode: c++
// End:
