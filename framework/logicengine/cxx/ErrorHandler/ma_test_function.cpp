#include <ErrorHandler/ma_test_function.h>

using namespace novadaq::errorhandler;

void
  ma_test_function_factory::reg( std::string const & func_name, gen_test_t f )
{
  get_map().insert( std::make_pair(func_name, f) );
}

ma_test_function *
  ma_test_function_factory::create_instance( std::string  const & func_name )
{
  gen_map_t::iterator it = get_map().find(func_name);

  if( it!=get_map().end() )
    return it->second( );

  throw std::runtime_error("unknown test function name");
}
