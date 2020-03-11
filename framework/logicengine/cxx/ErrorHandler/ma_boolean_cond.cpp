#include <ErrorHandler/ma_boolean_cond.h>
#include <ErrorHandler/ma_boolean_expr.h>

using namespace novadaq::errorhandler;

template <typename T>
bool
compare(compare_op_t op, T v, T rhv)
{
  switch (op) {
  case CO_L: return (v < rhv);
  case CO_LE: return (v <= rhv);
  case CO_E: return (v == rhv);
  case CO_NE: return (v != rhv);
  case CO_GE: return (v >= rhv);
  case CO_G: return (v > rhv);
  default: return false;
  }
}

void
ma_boolean_cond::reset()
{
  neg_cond = false;

  if (cond_type == EXPR) {
    // expression must not be null
    assert(expr.get() != NULL);
    return expr->reset();
  }

  if (cond_type == COND) { return; }

  throw std::runtime_error("ma_boolean_cond::reset(): unknow cond_type");
}

bool
ma_boolean_cond::evaluate(ma_domain& value, ma_domain const& domain) const
{
  if (cond_type == EXPR) {
    // expression must not be null
    assert(expr.get() != NULL);

    // evaluate from the expr
    bool v = expr->evaluate(value, domain);
    return neg_cond ? (!v) : (v);
  }

  if (cond_type == COND) {
    cond_idx_t cond_idx = cond_arg.first;

    // condition ptr must not be null
    assert(cond_idx.first != NULL);

    // get status from hitmap of the condition
    bool v = cond_idx.first->get_status(value[cond_idx.second]);
    return neg_cond ? (!v) : (v);
  }

  throw std::runtime_error("ma_boolean_cond::evaluate(): unknow cond_type");
}

void
ma_boolean_cond::insert_expr(ma_boolean_expr const& b_expr)
{
  expr.reset(new ma_boolean_expr(b_expr));
  cond_type = EXPR;
  neg_cond = false;
}

void
ma_boolean_cond::insert_expr_neg(ma_boolean_expr const& b_expr)
{
  expr.reset(new ma_boolean_expr(b_expr));
  cond_type = EXPR;
  neg_cond = true;
}
