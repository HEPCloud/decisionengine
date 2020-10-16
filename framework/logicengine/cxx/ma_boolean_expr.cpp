#include "ma_boolean_expr.h"

using namespace logic_engine;

bool
ma_boolean_expr::evaluate() const
{
  for (auto& andexpr : andexprs)
    if (andexpr.evaluate() == true) return true;

  return false;
}
