#ifndef ERROR_HANDLER_MA_FUNCTION_COUNT_PERCENT_H
#define ERROR_HANDLER_MA_FUNCTION_COUNT_PERCENT_H

#include <ErrorHandler/ma_function.h>

namespace novadaq {
namespace errorhandler {

class ma_func_count_percent : public ma_function
{

public:

  // c'tor and d'tor
  ma_func_count_percent() : count_type(SOURCE), group()  { }
  virtual ~ma_func_count_percent() { }

  // evaluate function
  virtual boost::any 
    evaluate( ma_condition const & cond
            , ma_cond_domain dom );

  // parse arguments
  virtual bool
    parse_arguments( anys_t const & args );

private:

  arg_t       count_type;
  std::string group;

};


} // end of namespace errorhandler
} // end of namespace novadaq

#endif





