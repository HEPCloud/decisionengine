#ifndef ERROR_HANDLER_UTILS_H
#define ERROR_HANDLER_UTILS_H

#include <ErrorHandler/ma_types.h>

namespace novadaq {
namespace errorhandler {

  inline string_t 
    trim_hostname(string_t const & host);

  inline node_type_t 
    get_source_from_msg(string_t & src, msg_t const & msg);

  inline string_t
    get_message_type_str(message_type_t type);

} // end of namespace errorhandler
} // end of namespace novadaq

// ------------------------------------------------------------------
// misc. utilities

novadaq::errorhandler::string_t 
  novadaq::errorhandler::trim_hostname(string_t const & host)
{
  size_t pos = host.find('.');
  if (pos==std::string::npos) return host;
  else                        return host.substr(0, pos);
}

novadaq::errorhandler::node_type_t 
  novadaq::errorhandler::get_source_from_msg(string_t & src, msg_t const & msg)
{
  src = "";
  return MainComponent;

#if 0 
  string_t host = trim_hostname(msg.hostname());

  if (  (host.find("dcm")!=string_t::npos) )
  {
    src  = host; return DCM;
  }
  else if (msg.application().find("dcm")!=string_t::npos)
  {
    src  = msg.application(); return DCM;
  }
  else if (host.find("novadaq-ctrl-farm")!=string_t::npos)
  {
    src  = host; return BufferNode;
  }
  else if (msg.application().find("BufferNodeEVBapp")!=string_t::npos)
  {
    src  = msg.application(); return BufferNode;
  }
  else
  {
    src  = msg.application(); return MainComponent;
  }
#endif
}


novadaq::errorhandler::string_t 
  novadaq::errorhandler::get_message_type_str(message_type_t type)
{
  switch(type)
  {
  case MSG_SYSTEM:  return "SYSTEM";
  case MSG_ERROR:   return "ERROR";
  case MSG_WARNING: return "WARNING";
  case MSG_INFO:    return "INFO";
  case MSG_DEBUG:   return "DEBUG";
  default:          return "UNKNOWN";
  }
}

#endif









