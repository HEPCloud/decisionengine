#include "ma_boolean_andexpr.h"

using namespace logic_engine;

bool
ma_boolean_andexpr::evaluate() const
{
  for (auto& cond : conds)
    if (cond.evaluate() == false) return false;

  return true;
}
