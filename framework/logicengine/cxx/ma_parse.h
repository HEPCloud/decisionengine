#ifndef logicengine_cxx_ma_parse_h
#define logicengine_cxx_ma_parse_h

#include "Fact.h"
#include "ma_types.h"

namespace logic_engine {

  class Rule;

  bool parse_fact_expr(string_t const& s, fact_map_t& fact_map, Rule* rule);

} // end of namespace logic_engine

#endif /* logicengine_cxx_ma_parse_h */

// Local Variables:
// mode: c++
// End:
