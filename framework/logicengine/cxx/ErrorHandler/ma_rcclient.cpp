
#include <NovaRunControlClient/RunControlReceiver.h>
#include <rms/base/RmsDestination.h>
#include <ErrorHandler/ma_rcclient.h>


using namespace gov::fnal::cd::rms;
using namespace novadaq::rcclient;

ma_rcclient::ma_rcclient( std::string appName, int partition )
{
  std::vector<std::string> bcastTargets;
  bcastTargets.push_back(base::RmsDestination::ALL_ELEMENT_TARGET);
  bcastTargets.push_back(base::RmsDestination::MESSAGE_ANALYZER_APPNAME);

  _rcReceiver.reset( new RunControlReceiver(appName, bcastTargets) );

  emit establishPartition( partition );

  _rcReceiver->addListener < runcontrolmessages::SetParticipantsRequest
			     , ma_rcclient
			     , runcontrolmessages::SetParticipantsResponse >
    ( partition, this );
  
}

ma_rcclient::~ma_rcclient()
{
  if( _rcReceiver.get() !=0 )
  {
    _rcReceiver->disconnectFromPartition(base::RmsDestination::NULL_PARTITION);
    _rcReceiver.reset();
  }
}

SetParticipantsResponse_t
  ma_rcclient::handleMessage( SetParticipantsRequest_t message )
{
  boost::mutex::scoped_lock sl(_callbackMutex);

  rmscore::RequestStatus reqStatus;
  reqStatus.code = 0;
  reqStatus.message = DDS::string_dup("Success");

  SetParticipantsResponse_t response;
  response.reset( new runcontrolmessages::SetParticipantsResponse() );
  response->status = reqStatus;

  QVector<QString> dcmlist;
  QVector<QString> bnevblist;

  for(size_t i=0; i<message->dcmList.length(); ++i)
    dcmlist.push_back( QString(DDS::string_dup(message->dcmList[i].appName)) );

  for(size_t i=0; i<message->bnevbList.length(); ++i)
    bnevblist.push_back( QString(DDS::string_dup(message->bnevbList[i].appName)) );

  emit setParticipants(dcmlist, bnevblist);

  return response;
}

