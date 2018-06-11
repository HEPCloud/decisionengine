#include <rms/provider/DDSConnection.h>
#include <rms/base/RmsDestination.h>
#include <rms/RmsReceiver.h>
#include <rms/RmsSender.h>
#include <rms/RmsMessageListener.h>

#include <DAQMessages/ccpp_ErrorHandlerMessages.h>

#include <boost/shared_ptr.hpp>

using namespace gov::fnal::cd::rms;



class EHListener : RmsMessageListener{

 public:

  EHListener(boost::shared_ptr<provider::DDSConnection> ddsConnection);
  void processMessage(boost::shared_ptr<errorhandlermessages::ErrorHandlerReply> reply);
  void messageReceived(boost::shared_ptr<base::RmsMessage> reply);
  bool success(){return fSuccess;};

 private:

  boost::shared_ptr<provider::DDSConnection> fDdsConnection;
  bool fSuccess;

};
