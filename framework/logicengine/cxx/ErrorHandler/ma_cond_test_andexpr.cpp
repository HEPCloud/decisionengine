
#include <ErrorHandler/ma_cond_test_andexpr.h>


using namespace novadaq::errorhandler;

bool ma_cond_test_andexpr::evaluate( ma_condition const * cond ) const
{
  test_primaries_t::const_iterator it = primaries.begin();
  
  for( ; it!=primaries.end(); ++it )
    if( it->evaluate( cond ) == false ) return false;

  return true;
}
