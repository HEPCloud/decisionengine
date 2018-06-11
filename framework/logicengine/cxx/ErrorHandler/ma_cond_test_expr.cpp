
#include <ErrorHandler/ma_cond_test_expr.h>

using namespace novadaq::errorhandler;

bool ma_cond_test_expr::evaluate( ma_condition const * cond ) const
{
  if( andexprs.empty() ) return true;

  test_andexprs_t::const_iterator it = andexprs.begin();

  for( ; it!=andexprs.end(); ++it )
    if( it->evaluate( cond ) == true ) return true;

  return false;
}


