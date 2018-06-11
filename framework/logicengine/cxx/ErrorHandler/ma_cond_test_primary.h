#ifndef ERROR_HANDLER_MA_COND_TEST_PRIMARY_H
#define ERROR_HANDLER_MA_COND_TEST_PRIMARY_H

#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_test_function.h>

#include <boost/shared_ptr.hpp>
#include <boost/any.hpp>

#include <list>

namespace novadaq {
namespace errorhandler {

typedef boost::any              any_t;
typedef std::vector<boost::any> anys_t;

class ma_cond_test_expr;

class ma_cond_test_primary
{
public:

  ma_cond_test_primary( )
    : cond_type ( EXPR )
    , op        ( CO_L )
    , rhv_b     ( false )
    , rhv_d     ( 0.0  )
    , rhv_s     (      )
  { }

  bool evaluate( ma_condition const * cond ) const;

  void insert_expr      ( ma_cond_test_expr const & expr );
  void insert_func      ( string_t     const & name
                        , anys_t       const & args );
  void insert_compare_op( compare_op_t cop, any_t const & v );

private:

  cond_type_t   cond_type;

  boost::shared_ptr<ma_test_function> func;

  compare_op_t  op;
  bool          rhv_b;
  double        rhv_d;
  string_t      rhv_s;

  // shared_ptr to a test expression
  boost::shared_ptr<ma_cond_test_expr> expr;

};

typedef std::list< ma_cond_test_primary > test_primaries_t;


} // end of namespace errorhandler
} // end of namespace novadaq



#endif





