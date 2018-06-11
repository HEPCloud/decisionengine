
#include <ErrorHandler/ma_tf_grp_to_number.h>
#include <ErrorHandler/ma_condition.h>

#include <boost/lexical_cast.hpp>

#include <iostream>
#include <cstdlib>
using namespace novadaq::errorhandler;

REG_MA_TEST_FUNCTION( grp_to_number, ma_tf_grp_to_number )

boost::any ma_tf_grp_to_number::evaluate( ma_condition const & cond )
{
  std::string s = cond.get_msg_group( group );
  std::string lead = s.substr(0, 2);

  if (lead == "0x" || lead == "0X")
  {
    long int v = strtol(s.c_str(), NULL, 0);
    return boost::any((double)v);
  }
  else
  {
    double v = boost::lexical_cast<double>( s ); 
    return boost::any(v);
  }
}

bool ma_tf_grp_to_number::parse_arguments( anys_t const & args )
{
  if( args.size() < 1 ) return false;

  group = boost::any_cast<int>(args[0]);
  return true;
}
