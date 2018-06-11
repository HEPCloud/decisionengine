#ifndef ERROR_HANDLER_MA_DOMAIN_EXPR_H
#define ERROR_HANDLER_MA_DOMAIN_EXPR_H

// from novadaq
#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_condition.h>
#include <ErrorHandler/ma_domain_andexpr.h>

// from ups

// from system

namespace novadaq {
namespace errorhandler {

// an domain expression is a collection of domain and-expressions
// connected with 'OR' operator
// e.g.: domain_expr = and_expr_1 OR and_expr_2 OR ...

class ma_domain_expr
{
public:

  ma_domain_expr( );

  void evaluate(ma_domains & domains) const;

  bool empty() const { return andexprs.empty(); }

  void insert_andexpr(ma_domain_andexpr const & andexpr)
    { andexprs.push_back(andexpr); }

private:

  // all conditions in the parent rule
  //cond_vec_t const &  conditions;

  // list of and-expressions
  domain_andexprs_t andexprs;

};

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
