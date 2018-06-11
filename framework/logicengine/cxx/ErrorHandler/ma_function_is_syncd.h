#ifndef ERROR_HANDLER_MA_FUNCTION_IS_SYNCD_H
#define ERROR_HANDLER_MA_FUNCTION_IS_SYNCD_H

#include <ErrorHandler/ma_function.h>

namespace novadaq {
namespace errorhandler {

class ma_func_is_syncd : public ma_function
{

public:

  ma_func_is_syncd() : sync_time(), min(0), max(0) { }
  virtual ~ma_func_is_syncd() { }

  virtual boost::any 
    evaluate ( ma_condition const & cond
             , ma_cond_domain );

  virtual bool
    grouped_alarm( );

private:

  std::map<std::string, uint64_t> sync_time;
  uint64_t min;
  uint64_t max;

};


} // end of namespace errorhandler
} // end of namespace novadaq

#endif











