
#if 0
#include <ErrorHandler/ma_utils.h>

using namespace novadaq::errorhandler;

int novadaq::errorhandler::and_op (int i, int j)
{ 
  if (i==j)           return i;

  if (i==-2 || j==-2) return -2;
  if (i==-1)          return j;
  if (j==-1)          return i;

  return -2;
}

string_t novadaq::errorhandler::trim_hostname(string_t const & host)
{
  size_t pos = host.find('.');
  if (pos==std::string::npos) return host;
  else                        return host.substr(0, pos);
}

node_type_t novadaq::errorhandler::get_source_from_msg(string_t & src, msg_t const & msg)
{
  string_t host = trim_hostname(msg.hostname());

  if (  (host.find("dcm")!=string_t::npos) )
  {
    src  = host; return DCM;
  }
  else if (host.find("novadaq-ctrl-farm")!=string_t::npos)
  {
    src  = host; return BufferNode;
  }
  else
  {
    src  = msg.application(); return MainComponent;
  }
}

ma_cond_domain novadaq::errorhandler::domain_and(ma_cond_domain const & d1, ma_cond_domain const & d2)
{
  return ma_cond_domain( and_op(d1.first, d2.first)
                       , and_op(d1.second, d2.second));
}

void domain_and( ma_cond_domain & d1, ma_cond_domain const & d2 )
{
  d1.first  = and_op(d1.first, d2.first);
  d1.second = and_op(d1.second, d2.second);
}

ma_cond_domain novadaq::errorhandler::domain_and(ma_cond_domains const & d)
{
  if (d.empty())   return ma_cond_domain(-2,-2);

  ma_cond_domain d_out = d.front();
  ma_cond_domains::const_iterator it = d.begin();
  while(++it!=d.end()) domain_and(d_out, *it);

  return d_out;
}

void novadaq::errorhandler::domain_and(ma_cond_domains & d)
{
  if (d.empty()) 
  {
    d.push_back(ma_cond_domain(-2,-2));
    return;
  }

  ma_cond_domains::const_iterator it = d.begin();
  while(++it!=d.end())  domain_and(d.front(), *it);
}


#endif










