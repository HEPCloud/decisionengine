#ifndef ERROR_HANDLER_MA_TEST_FUNCTION_GRP_TO_NUMBER_H
#define ERROR_HANDLER_MA_TEST_FUNCTION_GRP_TO_NUMBER_H


#include <ErrorHandler/ma_test_function.h>

namespace novadaq {
namespace errorhandler {

class ma_tf_grp_to_number : public ma_test_function
{

public:

  ma_tf_grp_to_number( ) : group(0) { } 

  virtual boost::any
    evaluate( ma_condition const & cond );

  virtual bool 
    parse_arguments( anys_t const & args );

private:

  int group;

};


} // end of namespace errorhandler
} // end of namespace novadaq




#endif
