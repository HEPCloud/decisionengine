#ifndef ERROR_HANDLER_MA_TEST_H
#define ERROR_HANDLER_MA_TEST_H

// ----------------------------------------------------------
//
//  Base class for custom condition test functions
//
// ----------------------------------------------------------

#include <boost/any.hpp>
#include <boost/function.hpp>

#include <vector>
#include <map>
#include <string>

namespace novadaq {
namespace errorhandler {

class ma_condition;

typedef std::vector<boost::any> anys_t;

class ma_test_function
{
public:

  ma_test_function( ) { }
  virtual ~ma_test_function() { }

  // evaluation function
  virtual boost::any 
    evaluate( ma_condition const & cond ) = 0;

  // parse aruments
  virtual bool 
    parse_arguments( anys_t const & args ) { return true; }

};


typedef boost::function<ma_test_function * ( )> gen_test_t;


struct ma_test_function_factory
{
  typedef std::map<std::string, gen_test_t> gen_map_t;

public:

  static void
    reg( std::string const & func_name, gen_test_t f );

  static ma_test_function *
    create_instance( std::string const & func_name );

private:

  ma_test_function_factory() { }

  static gen_map_t &
    get_map() { static gen_map_t map; return map; }

};


struct ma_test_function_maker
{
  ma_test_function_maker( std::string const & func_name, gen_test_t f )
    { ma_test_function_factory::reg( func_name, f ); }
};


} // end of namespace errorhandler
} // end of namespace novadaq


#define REG_MA_TEST_FUNCTION(func_name, class_name) \
ma_test_function * \
  class_name ## _maker_func( ) { return new class_name( ); } \
ma_test_function_maker \
  class_name ## _maker_func_global_var ( #func_name, class_name ## _maker_func );


#endif




