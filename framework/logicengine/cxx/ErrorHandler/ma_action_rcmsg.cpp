#include <ErrorHandler/ma_action_rcmsg.h>
#include <ErrorHandler/ma_rule.h>


#include <NovaTimingUtilities/TimingUtilities.h>

#include <QtCore/QMetaType>
#include <QtCore/QObject>
#include <QtCore/QVector>

#include <unistd.h>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <string>
#include <time.h>

using namespace novadaq::errorhandler;
using namespace gov::fnal::cd::rms;

REG_MA_ACTION( rcmsg, ma_action_rcmsg )


  
int gGetPartition(){
  int partition = 0;
  char* p = getenv("DAQ_LOG_ROOT");  
  if( p != NULL ) partition = (int)p[(int)strlen(p)-1] - 48;
  return partition;
}



ma_action_rcmsg::ma_action_rcmsg( ma_rule const * rule, pset_t const & pset )
  : ma_action( rule, pset ),
    fRmsConnection(new provider::DDSConnection("EHTestApplication",gGetPartition())),
    fSendDest("EHServerMailbox",base::RmsDestination::EH_CHANNEL),
    fRequestSender(fRmsConnection,fSendDest) 
{

  fActionName = pset.get<std::string>("name");
  fActionPara = pset.get<std::string>("param", std::string());
        
  fParam.init(rule, fActionPara);
  fRuleName = (rule->name().c_str());
}

ma_action_rcmsg::~ma_action_rcmsg(){
  fRequestSender.close();
  fRmsConnection->close();
}



int ma_action_rcmsg::Talk(){
  
  //  std::cout << "Sending Message on EH_CHANNEL...." << std::endl;

  timeval now;
  gettimeofday(&now,0);
  uint64_t ts_now;
  novadaq::timeutils::convertUnixTimeToNovaTime(now,ts_now);

  fMessage.time = ts_now;
  std::stringstream stupid_c;
  stupid_c << fActionPara;
  int error_code;
  stupid_c >> error_code;
  fMessage.error = error_code; // fActionName -> convert using enum...
  fRequestSender.sendMessage(fMessage);
  //std::cout << "Sent Message on EH_CHANNEL...." << std::endl;  

  return 0;
}

int ma_action_rcmsg::HandleResponse(){


  // reply comes back on same channel
  RmsReceiver<provider::DDSConnection,
    errorhandlermessages::ErrorHandlerReply,EHListener>
    requestReceiver(fRmsConnection,fSendDest);


  boost::shared_ptr<EHListener>
    listener(new EHListener(fRmsConnection));

  requestReceiver.setListener(listener);

  clock_t time_start = clock();
  float timeLimit = 10.*60.;

  // wait until time out.
  while( (((float)(clock() - time_start))/CLOCKS_PER_SEC) < timeLimit ){
    if( listener->success() ){
      return 1;
    }
  } // wait until RC tells us it's done

  return 0;
}

bool ma_action_rcmsg::exec()
{
  Talk();
  if( HandleResponse() ) return true;
  return false;
}


