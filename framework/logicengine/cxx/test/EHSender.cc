#include <time.h>
#include <string>
#include <sstream>
#include <iostream>

#include <rms/provider/DDSConnection.h>
#include <rms/base/RmsDestination.h>
#include <rms/RmsReceiver.h>
#include <rms/RmsSender.h>

#include <NovaTimingUtilities/TimingUtilities.h>

#include <DAQMessages/ccpp_ErrorHandlerMessages.h>

#include <boost/shared_ptr.hpp>

using namespace gov::fnal::cd::rms;


int main() {
  
  // create the connection to RMS
  boost::shared_ptr<provider::DDSConnection> 
    rmsConnection(new provider::DDSConnection("EHTestApplication",0));
  
  
  // create the destination that represents where we will receive
  // messages from
  base::RmsDestination sendDest("EHServerMailbox",
				   base::RmsDestination::EH_CHANNEL);

  
  RmsSender<provider::DDSConnection,errorhandlermessages::ErrorHandlerMessage>  
    requestSender(rmsConnection,sendDest);

  std::cout << "Sending Message on EH_CHANNEL...." << std::endl;
  
  errorhandlermessages::ErrorHandlerMessage message;


  timeval now;
  gettimeofday(&now,0);
  uint64_t ts_now;
  novadaq::timeutils::convertUnixTimeToNovaTime(now,ts_now);

  message.time = ts_now;
  message.error = 1;
  requestSender.sendMessage(message);
  std::cout << "Sent Message on EH_CHANNEL...." << std::endl;


  // listen for a reply
  RmsReceiver<provider::DDSConnection,
    errorhandlermessages::ErrorHandlerReply>
    requestReceiver(rmsConnection, sendDest);

  while(1) {

    std::cout << "Waiting for a reply..." << std::endl;
    errorhandlermessages::ErrorHandlerReply reply;
    requestReceiver.receiveMessage(reply);

    std::cout << "Got reply: "  
	      << (int)reply.action_complete << std::endl;
    std::cout << "Exiting..." << std::endl;    

    break;

  }



  // clean up
  requestReceiver.close();  
  requestSender.close();
  rmsConnection->close();

    return 0;
}
