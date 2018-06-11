#ifndef ERROR_HANDLER_MA_BOOLEAN_ANDEXPR_H
#define ERROR_HANDLER_MA_BOOLEAN_ANDEXPR_H

#include <ErrorHandler/ma_boolean_cond.h>

#include <list>

namespace novadaq {
namespace errorhandler {

//-------------------------------------------------------------------
//
// boolean and-expression consists of a list of boolean elemental
// conditions connected with 'AND' operator 
//
//-------------------------------------------------------------------

class ma_boolean_andexpr
{
public:

  // c'tor
  ma_boolean_andexpr( ) { }

  // reset
  void reset( );

  // evaluateion
  bool evaluate( ma_domain & value
               , ma_domain & alarm
               , ma_domain const & domain ) const;

  // insert a boolean cond
  void insert( ma_boolean_cond const & cond )
    { conds.push_back(cond); }

private:

  boolean_conds_t  conds;

};

typedef std::list<ma_boolean_andexpr>  boolean_andexprs_t;

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
