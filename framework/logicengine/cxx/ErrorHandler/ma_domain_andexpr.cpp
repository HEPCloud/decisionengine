
#include <ErrorHandler/ma_domain_andexpr.h>

using namespace novadaq::errorhandler;

ma_domain_andexpr::ma_domain_andexpr( )
//: conditions (conds)
{

}

void ma_domain_andexpr::evaluate( ma_domains & domains ) const
{

  ma_domains mydomains;

  domain_conds_t::const_iterator it = conds.begin();

  for( ; it!=conds.end(); ++it)
  {
    it->evaluate(mydomains);
    if( mydomains.empty() )  return;
  }

  // cat the domain list
  {
    domains.splice(domains.end(), mydomains);
  }
}


