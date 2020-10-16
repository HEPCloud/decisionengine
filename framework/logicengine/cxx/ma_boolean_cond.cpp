#include "ma_boolean_cond.h"
#include "ma_boolean_expr.h"

#include <cassert>

using namespace logic_engine;

bool
ma_boolean_cond::evaluate() const
{
  if (cond_type == EXPR) {
    assert(expr.get() != nullptr);
    bool const v = expr->evaluate();
    return neg_cond ? !v : v;
  }

  if (cond_type == COND) {
    assert(fact != nullptr);
    bool const v = fact->value();
    return neg_cond ? !v : v;
  }

  throw std::runtime_error("ma_boolean_cond::evaluate(): unknow cond_type");
}

void
ma_boolean_cond::insert_expr(ma_boolean_expr const& b_expr)
{
  expr = std::make_shared<ma_boolean_expr>(b_expr);
  cond_type = EXPR;
  neg_cond = false;
}

void
ma_boolean_cond::insert_expr_neg(ma_boolean_expr const& b_expr)
{
  expr = std::make_shared<ma_boolean_expr>(b_expr);
  cond_type = EXPR;
  neg_cond = true;
}
