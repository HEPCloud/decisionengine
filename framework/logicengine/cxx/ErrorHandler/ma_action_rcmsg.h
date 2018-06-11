#ifndef ERRORHANDER_MA_ACTION_RCMSG_H
#define ERRORHANDER_MA_ACTION_RCMSG_H

#include <ErrorHandler/ma_action.h>
#include <ErrorHandler/ma_richmsg.h>
#include <ErrorHandler/EHListener.h>

#include <boost/shared_ptr.hpp>

#include <rms/provider/DDSConnection.h>
#include <rms/base/RmsDestination.h>
#include <rms/RmsSender.h>
#include <rms/RmsReceiver.h>

#include <DAQMessages/ccpp_ErrorHandlerMessages.h>


using namespace gov::fnal::cd::rms;

namespace novadaq {
namespace errorhandler {

class ma_action_rcmsg : public ma_action
{

public:

  ma_action_rcmsg(ma_rule const * rule, pset_t const & pset);
  virtual ~ma_action_rcmsg();

  virtual bool exec();

private:

  int Talk();
  int HandleResponse();

  std::string fActionName;
  std::string fActionPara;

  const  char * fRuleName;
  ma_richmsg fParam;

  errorhandlermessages::ErrorHandlerMessage fMessage;

  boost::shared_ptr<provider::DDSConnection> fRmsConnection;
  base::RmsDestination fSendDest;
  RmsSender<provider::DDSConnection,errorhandlermessages::ErrorHandlerMessage> 
    fRequestSender;


};

} // end of namespace errorhandler
} // end of namespace novadaq


#endif
