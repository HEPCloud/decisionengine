#ifndef ERROR_HANDLER_MA_FUNCTION_H
#define ERROR_HANDLER_MA_FUNCTION_H

#include <string>
#include <vector>
#include <map>

#include <ErrorHandler/ma_types.h>

#include <boost/any.hpp>
#include <boost/function.hpp>

namespace novadaq {
namespace errorhandler {

class ma_condition;

typedef std::vector<boost::any>  anys_t;

// base class - all customized fucntions are inherited from it
class ma_function
{
public:

  ma_function() {}
  virtual ~ma_function() {}

  // evaluate() function gets called when the boolean expression
  // of the rule is being evaluated.
  //
  // param 'cond': 
  //        'cond' is the reference to the basic condition to which
  //        this user defined function is related. Though this object
  //        the function can have access to the most recent message
  //        that triggeres the condition, as well as other historical
  //        information
  //
  // param 'dom':
  //        when using complex conditions and domain selection clauses
  //        in the rule expression, a user define function might get
  //        evaluated multiple times each for a possible source/targets
  //        domain when a new message comes in. 'dom' contains the domain
  //        of possible source/target combinations in this evaluation.
  //        an example would be, cond.get_alarm_count(dom, cond_type)
  //        returns with the number of triggered source/target pairs
  //        WITHIN the given domain of a condition.
  //
  // return value:
  //        the return value could be a boolean, an integer, a double,
  //        or a string object. all of them need to be wrapped in a
  //        boost::any object before returning to the caller
  virtual boost::any 
    evaluate( ma_condition const & cond
            , ma_cond_domain dom ) = 0;

  // a user function is internally implemented by a class, which allows
  // the function to have states. not surprisingly would the funciton 
  // writers also like to implement a reset method for the purpose of
  // resetting the state of the user-defined function into its ground 
  // state
  virtual void
    reset( ) { }

  // a user function is allowed to take multiple arguments
  // other than the condition name that it applies on
  virtual bool
    parse_arguments( anys_t const & args ) { return true; }

  // whether the funciton triggers a grouped alarm or
  // individual alarms with respect to the condition's 
  // source / targets.
  //
  // e.g.: a user function COUNT() usually triggers a grouped
  //       alarm, as we dont necessary need to make distinguish
  //       between whether it was source 1,2,5, or source 3,7,8
  //       who trigger the alarm
  //       
  //       an example of non-grouped alarm is the function of
  //       OUT_OF_SYNC(). we are interested in who was out of 
  //       sync, and raises alarms for each source
  virtual bool
    grouped_alarm( ) { return true; }

protected:

private:

};

typedef boost::function<ma_function * ()> gen_func_t;

struct ma_function_factory
{
  typedef std::map<std::string, gen_func_t> gen_map_t;

public:

  static void 
    reg( std::string const & func_name, gen_func_t f );

  static ma_function *
    create_instance( std::string const & func_name );

private:

  ma_function_factory() {};

  static gen_map_t & 
    get_map() { static gen_map_t map; return map; }

};

struct ma_function_maker
{
  ma_function_maker( std::string const & func_name, gen_func_t f )
    { ma_function_factory::reg( func_name, f ); }
};


} // end of namespace errorhandler
} // end of namespace novadaq


// -------------------------------------------------
// Macro for registering the custom function

#define REG_MA_FUNCTION(func_name, class_name) \
ma_function * \
  class_name ## _maker_func( ) { return new class_name( ); } \
ma_function_maker \
  class_name ## _maker_func_global_var ( #func_name, class_name ## _maker_func );


#endif












