#ifndef ERROR_HANDLER_MA_PARSE_H
#define ERROR_HANDLER_MA_PARSE_H

#include <ErrorHandler/ma_types.h>

namespace novadaq {
namespace errorhandler {

  class ma_rule;
  class ma_cond_test_expr;

  bool parse_condition_expr ( string_t const & s
                            , ma_rule * rule );

  bool parse_condition_test ( string_t const & s
                            , ma_cond_test_expr & expr );

} // end of namespace errorhandler
} // end of namespace novadaq


#endif
