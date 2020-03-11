#ifndef ERROR_HANDLER_MA_PARSE_H
#define ERROR_HANDLER_MA_PARSE_H

#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_types.h>

namespace novadaq {
  namespace errorhandler {

    class ma_rule;

    bool parse_fact_expr(string_t const& s,
                         fact_map_t& conditions,
                         ma_rule* rule);

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
