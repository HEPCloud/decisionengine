
#include <ErrorHandler/ma_function.h>


using namespace novadaq::errorhandler;

// ma_function class



// ma_function_factory

void 
  ma_function_factory::reg( std::string const & func_name, gen_func_t f )
{
  get_map().insert( std::make_pair(func_name, f) );
}

ma_function *
  ma_function_factory::create_instance( std::string const & func_name )
{
  gen_map_t::iterator it = get_map().find(func_name);

  if( it!=get_map().end() )
    return it->second();

  throw std::runtime_error("unknown function name while creating instance of ma_function" );
}
