
#include <ErrorHandler/ma_domain_expr.h>

using namespace novadaq::errorhandler;

ma_domain_expr::ma_domain_expr( )
{

}

void ma_domain_expr::evaluate(ma_domains & domains) const
{
  domain_andexprs_t::const_iterator it = andexprs.begin();

  for( ; it!=andexprs.end(); ++it)
    it->evaluate(domains);    
}

