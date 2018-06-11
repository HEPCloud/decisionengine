#include <ErrorHandler/EHListener.h>
#include <iostream>

EHListener::EHListener(boost::shared_ptr<provider::DDSConnection> ddsConnection){
  fDdsConnection = ddsConnection;
  fSuccess = false;
}

void EHListener::processMessage(boost::shared_ptr<errorhandlermessages::ErrorHandlerReply> reply){

  // parse the reply here....                                                                         
  fSuccess = (bool)reply->action_complete;
  //std::cout << "Complete? " << fSuccess << std::endl;

  return;
}


// this has to be here
void EHListener::messageReceived(boost::shared_ptr<base::RmsMessage> reply){

  return;
}
