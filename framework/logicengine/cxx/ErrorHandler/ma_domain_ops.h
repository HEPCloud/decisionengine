#ifndef ERROR_HANDLER_MA_DOMAIN_OPS_H
#define ERROR_HANDLER_MA_DOMAIN_OPS_H

#include <ErrorHandler/ma_types.h>

namespace novadaq {
namespace errorhandler {

  // ----------------------------------------------------------------
  // intersection of domains

  // element op
  inline int and_op (int i, int j);

  // 1. (s_out, t_out) = (s1, t1) n (s2, t2), in-place and
  // intersection of two cond_domain objects
  inline ma_cond_domain & 
    domain_intersect( ma_cond_domain & d1, ma_cond_domain const & d2 );

  // copy version
  inline ma_cond_domain 
    domain_intersect_copy( ma_cond_domain d1, ma_cond_domain const & d2 );

  // 2. (s_out, t_out) = (s1, t1) n (s2, t2) n ... n (s_n, t_n), in-place and
  // intersection of multiple cond_domain objects
  inline ma_cond_domain &
    domain_intersect( ma_cond_domains & d );

  // copy version
  inline  ma_cond_domain 
    domain_intersect_copy( ma_cond_domains d );

  // 3. intersection of two domain objects, result stores in the first
  inline ma_domain &
    domain_intersect( ma_domain & d1, ma_domain const & d2 );

  // copy version
  inline ma_domain
    domain_intersect_copy( ma_domain d1, ma_domain const & d2 );

  // 4. (so1, to1), (so2, to2) ... 
  //        = (s1_1, t1_1) n (s1_2, t1_2) n (s1_3, t1_3) ... ,
  //          (s2_1, t2_1) n (s2_2, t2_2) n (s2_3, t2_3) ... ,
  //          ... 
  // intersection of multiple ma_domain objects
  // in-place calculation, result will be placed in d[0]
  inline ma_domain & 
    domain_intersect( ma_domains & d );

  // copy version
  inline ma_domain  
    domain_intersect_copy( ma_domains d );

  // ----------------------------------------------------------------
  // union of domains

  // element op -- test if a contains(>=) b
  inline bool contains_op( int a, int b );

  // 0. compare two cond_domains see if they contain one to another
  enum   domain_compare_result_t { NO_COMMON
                                 , EQUAL
                                 , L_CONTAINS
                                 , R_CONTAINS };

  inline domain_compare_result_t
    domain_compare( ma_cond_domain const & d1
                  , ma_cond_domain const & d2 );

  // 1. add a new cond_domain to a list of cond_domains
  inline ma_cond_domains &
    domain_union( ma_cond_domains & ds, ma_cond_domain const & new_d );

  // 2. (s1_1, t1_1) U (s1_2, t1_2) U (s1_3, t1_3) ... ,
  //    (s2_1, t2_1) U (s2_2, t2_2) U (s2_3, t2_3) ... ,
  //     ... 
  // * in-place union
  inline ma_domains &
    domain_union( ma_domains & ds );

  // utility functions
  inline bool 
    domain_is_null( ma_cond_domain const & d );

  inline bool 
    domain_is_null( ma_domain const & d );

  inline void
    domain_union_construct ( ma_domains & ds
                           , ma_domain & d
                           , std::vector<ma_cond_domains> & mid
                           , int depth
                           , int max );

  // construct a null ma_cond_domain (nil, nil)
  inline ma_cond_domain
    ma_cond_domain_ctor_null ( );

  // construct a any ma_cond_domain (*,*)
  inline ma_cond_domain
    ma_cond_domain_ctor_any ( );

  // construct a ma_cond_domain from s and t
  inline ma_cond_domain
    ma_cond_domain_ctor ( int s, int t );

  // construct a ma_cond_domain from a value and arg type (source or target)
  // ends up with a ma_cond_domain of (i,*) or (*,i)
  inline ma_cond_domain
    ma_cond_domain_ctor ( int i, arg_t t );

  // construct a null ma_domain
  inline ma_domain
    ma_domain_ctor_null ( );

  // construct a null ma_domain
  inline ma_domain
    ma_domain_ctor_null ( size_t size );

  // construct a any ma_domain with size s
  inline ma_domain
    ma_domain_ctor_any ( size_t size );

  // construct a ma_domain object with size s and init'd to d
  inline ma_domain
    ma_domain_ctor( size_t size, ma_cond_domain d );

} // end of namespace errorhandler
} // end of namespace novadaq


// ------------------------------------------------------------------
// utility functions

novadaq::errorhandler::ma_cond_domain
  novadaq::errorhandler::ma_cond_domain_ctor_null ( )
{
  return ma_cond_domain_ctor(D_NIL, D_NIL);
}

novadaq::errorhandler::ma_cond_domain
  novadaq::errorhandler::ma_cond_domain_ctor_any ( )
{
  return ma_cond_domain_ctor(D_ANY, D_ANY);
}

novadaq::errorhandler::ma_cond_domain
  novadaq::errorhandler::ma_cond_domain_ctor ( int s, int t )
{
  return ma_cond_domain(s, t);
}

novadaq::errorhandler::ma_cond_domain
  novadaq::errorhandler::ma_cond_domain_ctor ( int i, arg_t t )
{
  return (t==SOURCE) ? ma_cond_domain(i, D_ANY) : ma_cond_domain(D_ANY, i);
}

novadaq::errorhandler::ma_domain
  novadaq::errorhandler::ma_domain_ctor_null ( )
{
  return ma_domain(1, ma_cond_domain_ctor_null());
}

novadaq::errorhandler::ma_domain
  novadaq::errorhandler::ma_domain_ctor_null ( size_t size )
{
  return ma_domain(size, ma_cond_domain_ctor_null());
}

novadaq::errorhandler::ma_domain
  novadaq::errorhandler::ma_domain_ctor_any ( size_t size )
{
  return ma_domain(size, ma_cond_domain_ctor_any());
}

novadaq::errorhandler::ma_domain
  novadaq::errorhandler::ma_domain_ctor ( size_t size, ma_cond_domain d )
{
  return ma_domain(size, d);
}


// ------------------------------------------------------------------
// domain intersection 

int 
  novadaq::errorhandler::and_op( int i, int j )
{ 
  if (i==D_NIL || j==D_NIL) return D_NIL;

  if (i==j)      return i;
  if (i==D_ANY)  return j;
  if (j==D_ANY)  return i;

  return D_NIL;
}

novadaq::errorhandler::ma_cond_domain &
  novadaq::errorhandler::domain_intersect( ma_cond_domain & d1
                                         , ma_cond_domain const & d2 )
{
  d1.first  = and_op(d1.first, d2.first);
  d1.second = and_op(d1.second, d2.second);

  if (domain_is_null(d1))
    d1 = ma_cond_domain_ctor_null();

  return d1;
}

novadaq::errorhandler::ma_cond_domain 
  novadaq::errorhandler::domain_intersect_copy( ma_cond_domain d1
                                              , ma_cond_domain const & d2)
{
  return domain_intersect(d1, d2);
}

novadaq::errorhandler::ma_cond_domain &
  novadaq::errorhandler::domain_intersect( ma_cond_domains & ds )
{
  if (ds.empty()) 
  {
    ds.push_back(ma_cond_domain_ctor_null());
    return ds.front();
  }

  ma_cond_domains::const_iterator it = ds.begin();
  while(++it!=ds.end() && !domain_is_null(ds.front()))  
    domain_intersect(ds.front(), *it);

  return ds.front();
}

novadaq::errorhandler::ma_cond_domain 
  novadaq::errorhandler::domain_intersect_copy( ma_cond_domains d )
{
  return domain_intersect(d);
}

novadaq::errorhandler::ma_domain &
  novadaq::errorhandler::domain_intersect( ma_domain & d1 
                                         , ma_domain const & d2 )
{
  if (domain_is_null(d1) || domain_is_null(d2))
  {
    d1 = ma_domain_ctor_null();
    return d1;
  }

  if (d1.size() != d2.size())
    throw std::runtime_error("domain size incomparable while doing domain_intersect");

  for(size_t i=0; i<d1.size(); ++i)
  {
    domain_intersect(d1[i], d2[i]); 

    if (domain_is_null(d1[i]))
    {
      d1 = ma_domain_ctor_null();
      return d1;
    }
  }

  return d1;
}

novadaq::errorhandler::ma_domain 
  novadaq::errorhandler::domain_intersect_copy( ma_domain d1 
                                              , ma_domain const & d2 )
{
  return domain_intersect(d1, d2);
}

novadaq::errorhandler::ma_domain & 
    novadaq::errorhandler::domain_intersect( ma_domains & ds )
{
  if (ds.empty())
  {
    ds.push_back(ma_domain_ctor_null());
    return ds.front();
  }

  ma_domains::const_iterator it = ds.begin();
  while(++it!=ds.end())
  {
    for(size_t i=0; i<ds.front().size(); ++i)
    {
      domain_intersect(ds.front()[i], (*it)[i]);

      if (domain_is_null(ds.front()[i]))
      {
        ds.front() = ma_domain_ctor_null();
        goto exit;
      }
    }
  }

exit:

  return ds.front();
}

novadaq::errorhandler::ma_domain 
    novadaq::errorhandler::domain_intersect_copy( ma_domains ds )
{
  return domain_intersect(ds);
}


// ------------------------------------------------------------------
// domain union

bool
  novadaq::errorhandler::contains_op( int a, int b )
{
  return (a==b) ? (true) : ( (a==D_ANY || b==D_NIL) ? true : false );
}

bool 
novadaq::errorhandler::domain_is_null( ma_cond_domain const & d )
{
  return (d.first==D_NIL || d.second==D_NIL) ? true : false;
}

bool 
novadaq::errorhandler::domain_is_null( ma_domain const & d )
{
  if (d.empty()) return true;

  for (size_t i=0; i<d.size(); ++i)
    if (domain_is_null(d[i]))  return true;

  return false;
}

novadaq::errorhandler::domain_compare_result_t
  novadaq::errorhandler::domain_compare( ma_cond_domain const & d1
                                       , ma_cond_domain const & d2 )
{
  if (d1.first==d2.first && d1.second==d2.second)
    return EQUAL;

  bool flag1 = false;
  bool flag2 = false;

  if (contains_op(d1.first, d2.first))   flag1 = true;
  if (contains_op(d1.second, d2.second)) flag2 = true;

  if (flag1 != flag2)
    return NO_COMMON;

  if (flag1)
    return L_CONTAINS;
  else
    return R_CONTAINS;
}

novadaq::errorhandler::ma_cond_domains &
    novadaq::errorhandler::domain_union( ma_cond_domains & ds
                                       , ma_cond_domain const & new_d )
{
  if (domain_is_null(new_d))  return ds;

  ma_cond_domains::iterator it = ds.begin();
  while(it!=ds.end())
  {
    domain_compare_result_t r = domain_compare(*it, new_d);

    if (r == EQUAL || r == L_CONTAINS) 
      return ds;

    if (r == R_CONTAINS)
    {
      ds.erase(it);
      return domain_union(ds, new_d);
    }

    // NO_COMMON
    ++it;
  }

  ds.push_back(new_d);
  return ds;
}

void
  novadaq::errorhandler::domain_union_construct
                           ( ma_domains & ds
                           , ma_domain & d
                           , std::vector<ma_cond_domains> & mid
                           , int depth
                           , int max )
{
  ma_cond_domains::const_iterator it = mid[depth].begin();

  while(it!=mid[depth].end())
  {
    d[depth] = *it;

    if (depth != max)
      domain_union_construct(ds, d, mid, depth+1, max);
    else
      ds.push_back(d);
    
    ++it;
  }
}


novadaq::errorhandler::ma_domains &
  novadaq::errorhandler::domain_union( ma_domains & ds )
{
  if (ds.empty()) return ds;

  // domain size (how many conditions in a domain)
  size_t size = ds.front().size();

  // temp place to hold intermediate results
  std::vector<ma_cond_domains> mid(size);

  ma_domains::const_iterator it = ds.begin();
  while(it!=ds.end())
  {
    for(size_t i=0; i<size; ++i)
      domain_union(mid[i], (*it)[i]);

    ++it;
  }

  ma_domains result;
  ma_domain  domain(size);

  domain_union_construct(result, domain, mid, 0, size-1);

  ds = result;
  return ds;
}

#endif









