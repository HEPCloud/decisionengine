
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE ma_domain_ops_test
#include <boost/test/unit_test.hpp>

#include <ErrorHandler/ma_domain_ops.h>

using namespace novadaq::errorhandler;

BOOST_AUTO_TEST_SUITE( ma_domain_ops_test )

BOOST_AUTO_TEST_CASE(domain_ctor_test)
{
  {
    ma_cond_domain d = ma_cond_domain_ctor_null();
    BOOST_CHECK_EQUAL(d.first, D_NIL);
    BOOST_CHECK_EQUAL(d.second, D_NIL);
  }

  {
    ma_cond_domain d = ma_cond_domain_ctor_any();
    BOOST_CHECK_EQUAL(d.first, D_ANY);
    BOOST_CHECK_EQUAL(d.second, D_ANY);
  }

  {
    ma_cond_domain d = ma_cond_domain_ctor(5, 6);
    BOOST_CHECK_EQUAL(d.first, 5);
    BOOST_CHECK_EQUAL(d.second, 6);
  }

}

BOOST_AUTO_TEST_CASE(domain_intersect_test)
{

  // ----------------------------------------------------------------
  // ma_cond_domain intersection

  {
    ma_cond_domain d1 = ma_cond_domain_ctor_null();
    ma_cond_domain d2 = ma_cond_domain_ctor(5, 6);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, D_NIL);
    BOOST_CHECK_EQUAL(d1.second, D_NIL);
    BOOST_CHECK(domain_is_null(d1));
  }

  {
    ma_cond_domain d1 = ma_cond_domain_ctor_any();
    ma_cond_domain d2 = ma_cond_domain_ctor(5, 6);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, 5);
    BOOST_CHECK_EQUAL(d1.second, 6);
  }

  {
    ma_cond_domain d1 = ma_cond_domain_ctor(5, 8);
    ma_cond_domain d2 = ma_cond_domain_ctor(5, 6);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, D_NIL);
    BOOST_CHECK_EQUAL(d1.second, D_NIL);
    BOOST_CHECK(domain_is_null(d1));
  }

  {
    ma_cond_domain d1 = ma_cond_domain_ctor(5, D_ANY);
    ma_cond_domain d2 = ma_cond_domain_ctor(5, 6);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, 5);
    BOOST_CHECK_EQUAL(d1.second, 6);
  }

  {
    ma_cond_domain d1 = ma_cond_domain_ctor(D_ANY, 6);
    ma_cond_domain d2 = ma_cond_domain_ctor(5, 6);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, 5);
    BOOST_CHECK_EQUAL(d1.second, 6);
  }

  {
    ma_cond_domain d1 = ma_cond_domain_ctor(D_ANY, 6);
    ma_cond_domain d2 = ma_cond_domain_ctor(5, D_ANY);
    domain_intersect(d1, d2);
    BOOST_CHECK_EQUAL(d1.first, 5);
    BOOST_CHECK_EQUAL(d1.second, 6);
  }

  // ----------------------------------------------------------------
  // ma_domain_intersection

  {
    ma_domain d1 = ma_domain_ctor(3, ma_cond_domain_ctor(2,3));
    ma_domain d2 = ma_domain_ctor(4, ma_cond_domain_ctor(5,6));
    BOOST_CHECK_THROW( domain_intersect(d1,d2), std::runtime_error );
  }

  {
    ma_domain d1 = ma_domain_ctor(3, ma_cond_domain_ctor(2,3));
    ma_domain d2 = ma_domain_ctor(3, ma_cond_domain_ctor(5,6));
    domain_intersect(d1, d2);
    BOOST_CHECK( domain_is_null(d1) );
  }

}

BOOST_AUTO_TEST_CASE(domain_union_test)
{

}

BOOST_AUTO_TEST_SUITE_END()

