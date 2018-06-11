#ifndef ERROR_HANDLER_MA_ACTION_H
#define ERROR_HANDLER_MA_ACTION_H

#include <string>
#include <vector>
#include <map>

#include <ErrorHandler/ma_types.h>

//#include <fhiclcpp/ParameterSet.h>

#include <boost/any.hpp>
#include <boost/function.hpp>

namespace novadaq {
namespace errorhandler {

class ma_condition;
class ma_rule;

typedef std::vector<boost::any>  anys_t;
typedef fhicl::ParameterSet      pset_t;

// base class - all customized fucntions are inherited from it
class ma_action
{
public:

  ma_action(ma_rule const * rule, pset_t const & pset = pset_t()) 
    : parent_rule(*rule), parameter(pset) {}
  virtual ~ma_action() {}

  virtual bool exec( ) = 0;

protected:

  ma_rule const & parent_rule;
  pset_t parameter;

private:

};

typedef std::vector<ma_action *> ma_actions;

typedef boost::function<ma_action * (ma_rule const *, pset_t const &)> gen_act_t;

struct ma_action_factory
{
  typedef std::map<std::string, gen_act_t> gen_map_t;

public:

  static void 
    reg( std::string const & action_name, gen_act_t f );

  static ma_action *
    create_instance( std::string const & act_name, ma_rule const * rule, pset_t const & pset );

private:

  ma_action_factory() {};

  static gen_map_t & 
    get_map() { static gen_map_t map; return map; }

};

struct ma_action_maker
{
  ma_action_maker( std::string const & act_name, gen_act_t f )
    { ma_action_factory::reg( act_name, f ); }
};


} // end of namespace errorhandler
} // end of namespace novadaq


// -------------------------------------------------
// Macro for registering the custom function

#define REG_MA_ACTION(act_name, class_name) \
ma_action * \
  class_name ## _maker_func( ma_rule const * r, fhicl::ParameterSet const & p ) \
  { return new class_name( r, p ); } \
ma_action_maker \
  class_name ## _maker_func_global_var ( #act_name, class_name ## _maker_func );


#endif












