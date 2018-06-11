
#include <ErrorHandler/ma_boolean_expr.h>

using namespace novadaq::errorhandler;

void ma_boolean_expr::reset( )
{
  boolean_andexprs_t::iterator it = andexprs.begin();
  for( ; it!=andexprs.end(); ++it ) it->reset();
}

bool ma_boolean_expr::evaluate( ma_domain & value
                              , ma_domain & alarm
                              , ma_domain const & domain ) const
{
  boolean_andexprs_t::const_iterator it = andexprs.begin();

  for( ; it!=andexprs.end(); ++it )
    if( it->evaluate(value, alarm, domain) == true )  return true;

  return false;
}


