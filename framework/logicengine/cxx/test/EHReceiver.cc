#include <time.h>
#include <string>
#include <sstream>

#include <rms/provider/DDSConnection.h>
#include <rms/base/RmsDestination.h>
#include <rms/RmsReceiver.h>
#include <rms/RmsSender.h>

#include <NovaTimingUtilities/TimingUtilities.h>

#include <DAQMessages/ccpp_ErrorHandlerMessages.h>

#include <boost/shared_ptr.hpp>

using namespace gov::fnal::cd::rms;
using namespace novadaq::timeutils;

int main() {
  
  // create the connection to RMS
  boost::shared_ptr<provider::DDSConnection> 
    rmsConnection(new provider::DDSConnection("EHTestApplication",0));
  
  
  // create the destination that represents where we will receive
  // messages from
  base::RmsDestination receiveDest("EHServerMailbox",
				   base::RmsDestination::EH_CHANNEL);

  
  // create a receiver with the connection object and destination
  RmsReceiver<provider::DDSConnection,
    errorhandlermessages::ErrorHandlerMessage>
        requestReceiver(rmsConnection, receiveDest);

  

    while(1) {

    // wait for a message to arrive
    std::cout << "Waiting for a message..." << std::endl;
    errorhandlermessages::ErrorHandlerMessage EHMessage;
    requestReceiver.receiveMessage(EHMessage);

    std::cout << std::endl << "Received message!" << std::endl;
    std::cout << convertNovaTimeToString(EHMessage.time) << std::endl 
	      << EHMessage.error << std::endl << std::endl;
   

    
    RmsSender<provider::DDSConnection,errorhandlermessages::ErrorHandlerReply>
      requestSender(rmsConnection,receiveDest);

    errorhandlermessages::ErrorHandlerReply reply;
    reply.action_complete = true;
    requestSender.sendMessage(reply);
    requestSender.close();

    }
    
    
    // cleanup and exit
    requestReceiver.close();
    rmsConnection->close();

    return 0;
}
