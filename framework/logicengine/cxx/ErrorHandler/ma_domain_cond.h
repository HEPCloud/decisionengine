#ifndef ERROR_HANDLER_MA_DOMAIN_COND_H
#define ERROR_HANDLER_MA_DOMAIN_COND_H

// from novadaq
#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_condition.h>

// from ups
#include <boost/shared_ptr.hpp>

// from system
#include <list>

namespace novadaq {
namespace errorhandler {

// An elemental domain condition could be one of the followings:
// 1. rule_cond_1.$[s|t] = rule_cond_2.$[s|t] ( = "string literal" )
// 2. '(' >> domain_expr >> ')'

class ma_rule;
class ma_domain_expr;

class ma_domain_cond
{
public:

  ma_domain_cond( );

  // evaluate domains of this ma_domain_cond, then merge the
  // result with passed in domains
  void evaluate(ma_domains & domains) const;

  // insert condition idx and $s/$t
  void insert_cond_arg( cond_idx_t ci, arg_t arg, size_t size )
    { conds.push_back(std::make_pair(ci, arg)); cond_size = size; }

  // insert string condition ( cond.$s = 'str_cond' )
  void insert_str_cond( string_t const & str ) 
    { str_cond = str; }

  // insert domain_expr ( cond_type = EXPR )
  void insert_expr( ma_domain_expr const & expr );

  // and-merge domains from worksheet into domains
  ma_domains & 
    and_merge( ma_domains & domains, ma_domains & worksheet ) const;

private:

  // type of this elemental condition
  cond_type_t           cond_type;  

  // case CONDS: rule_cond_args connected with '='
  cond_arg_list_t       conds;
  std::string           str_cond;
  size_t                cond_size;  // # of conds in the parent rule

  // case EXPR: an expression
  // it has to be a ptr to domain_expression to avoid circulic inclusion
  boost::shared_ptr<ma_domain_expr>  expr;

};

typedef std::list<ma_domain_cond>  domain_conds_t;

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
