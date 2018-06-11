
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE ma_domain_test
#include <boost/test/unit_test.hpp>

#include <ErrorHandler/ma_domain_ops.h>
#include <ErrorHandler/ma_domain_cond.h>

using namespace novadaq::errorhandler;

BOOST_AUTO_TEST_SUITE( ma_domain_test )

BOOST_AUTO_TEST_CASE(ma_domain_cond_test)
{
  {
    cond_vec_t conds;
    ma_domain_cond d_cond;
    ma_domains d1;
    ma_domains d2;
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(1,1)));
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(2,2)));
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(3,3)));
    d_cond.and_merge(d1,d2);
    BOOST_CHECK(d1.size()==3);
  }

  {
    cond_vec_t conds;
    ma_domain_cond d_cond;
    ma_domains d1;
    d1.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(1,1)));
    d1.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(3,3)));
    ma_domains d2;
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(1,1)));
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(2,2)));
    d2.push_back(ma_domain_ctor(3, ma_cond_domain_ctor(3,3)));
    d_cond.and_merge(d1,d2);
    BOOST_CHECK(d1.size()==2);
  }

}

BOOST_AUTO_TEST_SUITE_END()

