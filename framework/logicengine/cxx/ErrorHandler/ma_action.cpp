
#include <ErrorHandler/ma_action.h>


using namespace novadaq::errorhandler;

// ma_function class



// ma_function_factory

void 
  ma_action_factory::reg( std::string const & func_name, gen_act_t f )
{
  get_map().insert( std::make_pair(func_name, f) );
}

ma_action *
  ma_action_factory::create_instance( std::string const & func_name
                                    , ma_rule     const * rule
                                    , pset_t      const & pset )
{
  gen_map_t::iterator it = get_map().find(func_name);

  if( it!=get_map().end() )
    return it->second(rule, pset);

  throw std::runtime_error("unknown action name while creating instance of ma_action" );
}
