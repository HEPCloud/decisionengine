
#include <ErrorHandler/ma_boolean_andexpr.h>

using namespace novadaq::errorhandler;

void ma_boolean_andexpr::reset( )
{
  boolean_conds_t::iterator it = conds.begin();
  for( ; it!=conds.end(); ++it ) it->reset();
}

bool ma_boolean_andexpr::evaluate( ma_domain & value
                                 , ma_domain & alarm
                                 , ma_domain const & domain ) const
{
  boolean_conds_t::const_iterator it = conds.begin();

  for( ; it!=conds.end(); ++it )
    if( it->evaluate(value, alarm, domain) == false )  return false;

  return true;
}
