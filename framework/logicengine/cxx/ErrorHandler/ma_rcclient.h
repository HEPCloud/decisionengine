#ifndef ERRORHANDLER_MA_RCCLIENT_H
#define ERRORHANDLER_MA_RCCLIENT_H

#include <DAQMessages/ccpp_RunControlMessages.h>

#include <boost/shared_ptr.hpp>
#include <boost/thread/mutex.hpp>

#include <QtCore/QObject>
#include <QtCore/QVector>

namespace RMSNS = gov::fnal::cd::rms;

namespace novadaq {
namespace rcclient {

class RunControlReceiver;

typedef boost::shared_ptr<runcontrolmessages::SetParticipantsRequest>
               SetParticipantsRequest_t;

typedef boost::shared_ptr<runcontrolmessages::SetParticipantsResponse>
               SetParticipantsResponse_t;

class ma_rcclient : public QObject
{

  Q_OBJECT

public:

  explicit ma_rcclient( std::string appName, int p );
  ~ma_rcclient();


  SetParticipantsResponse_t
    handleMessage( SetParticipantsRequest_t message );
  
signals:

  void establishPartition(int partition);
  void setParticipants( QVector<QString> const & dcmList
                      , QVector<QString> const & bnevbList );

private:

  boost::shared_ptr<RunControlReceiver> _rcReceiver;
  mutable boost::mutex _callbackMutex;

};




} // end of namespace errorhandler
} // end of namespace novadaq




#endif






