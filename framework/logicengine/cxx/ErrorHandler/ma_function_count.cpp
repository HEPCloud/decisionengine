
#include <ErrorHandler/ma_function_count.h>
#include <ErrorHandler/ma_condition.h>
#include <ErrorHandler/ma_participants.h>

#include <boost/algorithm/string.hpp>


using namespace novadaq::errorhandler;

REG_MA_FUNCTION( count, ma_func_count )

bool
  ma_func_count::parse_arguments( anys_t const & args )
{
  // override 1: int count(cond)
  if( args.empty() ) 
  {
    count_type = NONE;
    return true;
  }

  // override 2: double count(cond, 'type')
  // return the absolute value of count(cond) in the given type
  //   type = 'SOURCE'
  //   type = 'TARGET'
  //   type = 'MESSAGE'
  std::string type = boost::any_cast<std::string>(args[0]);
  boost::to_upper(type);

  if( type == "SOURCE" )       count_type = SOURCE;
  else if( type == "TARGET" )  count_type = TARGET;
  else if( type == "MESSAGE" ) count_type = NONE;
  else                         return false;

  return true;
}

boost::any
  ma_func_count::evaluate( ma_condition const & cond
                         , ma_cond_domain dom )
{
  // get triggering count from hitmap of the condition with give domain
  int count = cond.get_alarm_count( dom, count_type );

  std::cout << "count = " << count;

  return boost::any(count);
}











