#ifndef ERROR_HANDLER_MA_BOOLEAN_EXPR_H
#define ERROR_HANDLER_MA_BOOLEAN_EXPR_H

#include <ErrorHandler/ma_boolean_andexpr.h>

namespace novadaq {
namespace errorhandler {

//-------------------------------------------------------------------
//
// boolean expression consists of a list of boolean and-expression
// connected with 'OR' operator
//
//-------------------------------------------------------------------

class ma_boolean_expr
{
public:

  // c'tor
  ma_boolean_expr( ) { }

  // reset
  void reset( );

  // evaluation
  bool evaluate( ma_domain & value
               , ma_domain & alarm
               , ma_domain const & domain ) const;

  // insert an boolean and-expression
  void insert( ma_boolean_andexpr const & andexpr )
    { andexprs.push_back(andexpr); }

private:

  boolean_andexprs_t  andexprs;

};

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
