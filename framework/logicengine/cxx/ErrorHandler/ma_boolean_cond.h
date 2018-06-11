#ifndef ERROR_HANDLER_MA_BOOLEAN_COND_H
#define ERROR_HANDLER_MA_BOOLEAN_COND_H

#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_condition.h>
#include <ErrorHandler/ma_function.h>

#include <boost/shared_ptr.hpp>
#include <boost/any.hpp>

#include <list>

namespace novadaq {
namespace errorhandler {

class ma_rule;
class ma_boolean_expr;

//-------------------------------------------------------------------
//
// elementary boolean condition has three possible cases:
//   1. '(' + boolean_expr + ')'
//   2. primitive elementary boolean condition Cn
//   3. non-primitive boolean condition ( COUNT(Cn.$s|t) )
//
//-------------------------------------------------------------------

class ma_boolean_cond
{
public:

  // c'tor
  ma_boolean_cond( ) 
    : cond_type ( COND )
    , neg_cond  ( false )
    , cond_arg  ( cond_arg_t(cond_idx_t(NULL, 0), NONE) )
    , op        ( CO_L )
    , rhv_b     ( false )
    , rhv_d     ( 0.0  )
    , rhv_s     (      )
    , ext_func  (      )
    , expr      (      ) 
  { }

  // reset boolean cond
  void reset( );

  // evaluation
  bool evaluate( ma_domain & value
               , ma_domain & alarm
               , ma_domain const & domain ) const;

  // insert a boolean expression
  void insert_expr( ma_boolean_expr const & expr );
  void insert_expr_neg( ma_boolean_expr const & expr );

  // insert a primitive condition
  void insert_cond( cond_idx_t ci ) 
    { cond_arg.first = ci; cond_arg.second = NONE; neg_cond = false; }

  void insert_cond_neg( cond_idx_t ci ) 
    { cond_arg.first = ci; cond_arg.second = NONE; neg_cond = true; }

  void insert_ext_func( cond_idx_t ci
                      , arg_t arg
                      , std::vector<boost::any> const & func_args
                      , string_t const & function );

  void insert_compare_op_bool  ( compare_op_t cop, bool v )
    { op = cop; rhv_b = v; cond_type = FUNCTION_BOOL; }
    
  void insert_compare_op_double( compare_op_t cop, double v )
    { op = cop; rhv_d = v; cond_type = FUNCTION_DOUBLE; }

  void insert_compare_op_string( compare_op_t cop, string_t const & v )
    { op = cop; rhv_s = v; cond_type = FUNCTION_STRING; }
    

private:

  // type of this element condition
  cond_type_t    cond_type;

  // negtive condition ( !cond )
  bool           neg_cond;

  // case COND: this boolean cond is the boolean value of a ma_condition
  //   a pointer to the condition in the one big condition container
  //   DOES NOT own the condition
  cond_arg_t     cond_arg;

  // case EXT_FUNCTION:
  //   op:       compare operator, <, <=, ==, !=, >=, >
  //   rhv:      righ-hand value
  //   ext_func: ptr to a customized evaluation function. use ext_func->evaluate() 
  //             to evaluate
  compare_op_t   op;
  bool           rhv_b;
  double         rhv_d;
  string_t       rhv_s;
  boost::shared_ptr<ma_function> ext_func;

  // shared_ptr to an boolean expression
  //   a smart pointer to an boolean expression object
  //   DOES own the expression object 
  boost::shared_ptr<ma_boolean_expr> expr;

};

typedef std::list<ma_boolean_cond>   boolean_conds_t;

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
