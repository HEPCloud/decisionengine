#ifndef logicengine_cxx_ma_types_h
#define logicengine_cxx_ma_types_h

/*
 * ma_types.h has all typedefs and enums needed in the
 * message analyzer package
 */

// system includes
#include <list>
#include <map>
#include <memory>
#include <string>
#include <vector>

namespace logic_engine {

  // forward declaration
  class Fact;
  class Rule;

  // typdefs used in errorhandler
  typedef std::string string_t;
  typedef std::vector<std::string> strings_t;

  // type for elemental domain/boolean cond
  enum cond_type_t { COND, EXPR };

  // compare operators, <, <=, =, >=, >
  enum compare_op_t { CO_L, CO_LE, CO_E, CO_NE, CO_GE, CO_G };

  // notification list
  typedef std::list<Rule*> rules_t;
  typedef std::list<Fact*> facts_t;

  const unsigned int STATUS_CHANGE = 0x01;
} // end of namespace logic_engine

#endif /* logicengine_cxx_ma_types_h */

// Local Variables:
// mode: c++
// End:
