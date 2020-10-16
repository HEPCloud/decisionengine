#ifndef logicengine_cxx_ma_boolean_andexpr_h
#define logicengine_cxx_ma_boolean_andexpr_h

#include "ma_boolean_cond.h"

#include <list>

namespace logic_engine {

  //-------------------------------------------------------------------
  //
  // boolean and-expression consists of a list of boolean elemental
  // conditions connected with 'AND' operator
  //
  //-------------------------------------------------------------------

  class ma_boolean_andexpr {
  public:
    bool evaluate() const;
    void
    insert(ma_boolean_cond const& cond)
    {
      conds.push_back(cond);
    }

  private:
    boolean_conds_t conds;
  };

  typedef std::list<ma_boolean_andexpr> boolean_andexprs_t;

} // end of namespace logic_engine

#endif /* logicengine_cxx_ma_boolean_andexpr_h */

// Local Variables:
// mode: c++
// End:
