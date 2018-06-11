
#include <ErrorHandler/ma_function_is_syncd.h>
#include <ErrorHandler/ma_condition.h>

#include <boost/lexical_cast.hpp>

using namespace novadaq::errorhandler;

// class registeration
REG_MA_FUNCTION( is_syncd /*function name*/, ma_func_is_syncd  /*class name*/ )

bool
  ma_func_is_syncd::grouped_alarm( )
{
  return false;
}

boost::any
  ma_func_is_syncd::evaluate( ma_condition const & cond
                            , ma_cond_domain )
{
  std::string time_str = cond.get_msg_group(1);
  std::string source   = cond.get_msg_source();

  uint64_t time = 0;

  try
  {
    time = boost::lexical_cast<uint64_t>(time_str);
  }
  catch( boost::bad_lexical_cast & )
  {
    return boost::any(true);
  }
  
  //std::map<std::string, uint64_t>::const_iterator it = sync_time.find(source);

  if( sync_time.empty() || sync_time.find(source)!=sync_time.end() )
  {
    // a new round if the table is empty, or the key already exists
    sync_time.clear();
    min = time;
    max = time;

    sync_time.insert(std::make_pair(source, time));
    return boost::any(false);
  }
  else
  {
    // check if in-sync
    sync_time.insert(std::make_pair(source, time));

    if( time<min ) min = time;
    if( time>max ) max = time;

    if( max-min > 5 ) return boost::any(true);
    else              return boost::any(false);
  }

}


