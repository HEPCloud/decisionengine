#ifndef ERROR_HANDLER_MA_COND_TEST_EXPR_H
#define ERROR_HANDLER_MA_COND_TEST_EXPR_H


#include <ErrorHandler/ma_cond_test_andexpr.h>


namespace novadaq {
namespace errorhandler {


class ma_cond_test_expr
{
public:

  ma_cond_test_expr( ) : andexprs() { }

  bool evaluate( ma_condition const * cond ) const;

  void insert( ma_cond_test_andexpr const & andexpr )
    { andexprs.push_back(andexpr); }

private:

  test_andexprs_t andexprs;


};


} // end of namespace errorhandler
} // end of namespace novadaq



#endif





