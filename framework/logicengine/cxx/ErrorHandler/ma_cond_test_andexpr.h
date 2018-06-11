#ifndef ERROR_HANDLER_MA_COND_TEST_ANDEXPR_H
#define ERROR_HANDLER_MA_COND_TEST_ANDEXPR_H


#include <ErrorHandler/ma_cond_test_primary.h>

#include <list>


namespace novadaq {
namespace errorhandler {


class ma_cond_test_andexpr
{
public:

  ma_cond_test_andexpr( ) : primaries() { }

  bool evaluate( ma_condition const * cond ) const;

  void insert( ma_cond_test_primary const & primary )
    { primaries.push_back(primary); }

private:

  test_primaries_t primaries;

};

typedef std::list<ma_cond_test_andexpr> test_andexprs_t;


} // end of namespace errorhandler
} // end of namespace novadaq



#endif





