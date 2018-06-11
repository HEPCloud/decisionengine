
#include <ErrorHandler/ma_function_countpercent.h>
#include <ErrorHandler/ma_condition.h>
#include <ErrorHandler/ma_participants.h>

#include <boost/algorithm/string.hpp>

using namespace novadaq::errorhandler;

REG_MA_FUNCTION( count_percent, ma_func_count_percent )

bool
  ma_func_count_percent::parse_arguments( anys_t const & args )
{
  if( args.empty() || args.size()<2 ) 
    return false;

  // double count_percent(cond, 'type', 'group')
  // return the ratio of count(cond, 'type') to the # participant in 'group'
  //   type = 'SOURCE'
  //   type = 'TARGET'
  //   group : arbitary string

  std::string type = boost::any_cast<std::string>(args[0]);
  boost::to_upper(type);

  if( type == "SOURCE" )       count_type = SOURCE;
  else if( type == "TARGET" )  count_type = TARGET;
  else                         return false;

  group = boost::any_cast<std::string>(args[1]);

  return true;
}

boost::any
  ma_func_count_percent::evaluate( ma_condition const & cond
                                 , ma_cond_domain dom )
{
  // get triggering count from hitmap of the condition with give domain
  int count = cond.get_alarm_count( dom, count_type );
  int total = ma_participants::instance().get_group_participant_count( group );

  std::cout << "count = " << count << ", participants = " << total;

  return boost::any( (double)count/total );
}











