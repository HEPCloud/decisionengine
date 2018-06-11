#ifndef ERROR_HANDLER_MA_DOMAIN_ANDEXPR_H
#define ERROR_HANDLER_MA_DOMAIN_ANDEXPR_H

// from novadaq
#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_domain_cond.h>

// from ups

// from system
#include <list>

namespace novadaq {
namespace errorhandler {

// A domain and-expression is a collection of elemental domain conditions
// connected with 'AND' operator
// e.g.: and-expression = domain_cond_1 AND domain_cond_2 AND ...

class ma_domain_andexpr
{
public:

  ma_domain_andexpr( );

  void evaluate(ma_domains & domains) const;

  void insert_cond(ma_domain_cond const & cond)
    { conds.push_back(cond); }

private:

  // all conditions in the parent rule
  //cond_vec_t const &  conditions;
 
  // list of domain conditions
  domain_conds_t conds;

};

typedef std::list<ma_domain_andexpr> domain_andexprs_t;

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
