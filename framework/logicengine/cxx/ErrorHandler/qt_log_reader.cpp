
#include <ErrorHandler/qt_log_reader.h>

using namespace novadaq::errorhandler;

bool qt_log_reader::open( QString const & filename )
{
  reader.open(filename.toUtf8().constData());

  idx = 0;
  pause = false;
  return true;
}


void qt_log_reader::run()
{
  pause = false;

  while( !reader.iseof() )
  {
    if( pause )
    {
      pause = false;
      return;
    }

    // read
    mf::MessageFacilityMsg msg = reader.read_next();
    emit newMessage(msg);

    // report progress
    //if( idx%10000000 == 0 )
    //  emit updateProgress(idx/10000000);

    //++idx;
  }

  emit readCompleted();
}

void qt_log_reader::pause_exec()
{
  pause = true;
  wait();
}

void qt_log_reader::resume()
{
  start();
}

