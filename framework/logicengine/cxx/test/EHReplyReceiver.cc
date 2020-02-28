#include <memory>
#include <sstream>
#include <string>
#include <time.h>

#include <rms/RmsReceiver.h>
#include <rms/RmsSender.h>
#include <rms/base/RmsDestination.h>
#include <rms/provider/DDSConnection.h>

#include <DAQMessages/ccpp_ErrorHandlerMessages.h>
#include <ErrorHandler/EHListener.h>
#include <NovaTimingUtilities/TimingUtilities.h>

using namespace gov::fnal::cd::rms;
using namespace novadaq::timeutils;

int
main()
{

  // create the connection to RMS
  std::shared_ptr<provider::DDSConnection> rmsConnection(
    new provider::DDSConnection("EHTestApplication", 0));

  // create the destination that represents where we will receive
  // messages from
  base::RmsDestination receiveDest("EHServerMailbox",
                                   base::RmsDestination::EH_CHANNEL);

  // create a receiver with the connection object and destination
  RmsReceiver<provider::DDSConnection,
              errorhandlermessages::ErrorHandlerReply,
              EHListener>
    requestReceiver(rmsConnection, receiveDest);

  std::shared_ptr<EHListener> listener(new EHListener(rmsConnection));

  requestReceiver.setListener(listener);

  // waiting for a message to arrive
  std::cout << "Listening for messages..." << std::endl;

  // cleanup and exit
  requestReceiver.close();
  rmsConnection->close();

  return 0;
}
