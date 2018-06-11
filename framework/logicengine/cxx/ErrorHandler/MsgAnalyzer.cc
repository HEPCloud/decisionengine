#include <QtGui/QApplication>
#include <QtCore/QSettings>

#include <ErrorHandler/MsgAnalyzerDlg.h>

#include <iostream>

using namespace novadaq::errorhandler;
using namespace std;

void printUsage()
{
  std::cout << "MsgAnalyzer usage:\n"
            << "  -h, --help                \tdisplay help message\n"
            << "  -c, --configuration [file]\tspecify the path and filename to the message analyzer conf file\n"
            << "  -l, --log [file]          \tspecify the path and filename to the log (messagefacility) conf file\n";
}

int main(int argc, char *argv[])
{
  Q_INIT_RESOURCE(rc);

  QApplication app(argc, argv);

  std::string cfg("msganalyzer.fcl");
  std::string mf_cfg("msganalyzer_mf.fcl");

  int partition = 0;

  if( argc>1 )
  {
    for( int i=0; i<argc; ++i )
    {
      if(!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help") )
      {
        printUsage();
        return 0;
      }

      if((!strcmp(argv[i], "-c") || !strcmp(argv[i], "--configuration")) 
          && i<argc-1 )
      {
        cfg = std::string(argv[i+1]);
        ++i;
        continue;
      }

      if((!strcmp(argv[i], "-l") || !strcmp(argv[i], "--log")) 
          && i<argc-1 )
      {
        mf_cfg = std::string(argv[i+1]);
        ++i;
        continue;
      }

    }
  }

  // message facility
  //putenv((char*)"FHICL_FILE_PATH=.");
  fhicl::ParameterSet pset = mf::MessageFacilityService::ConfigurationFile(mf_cfg);
  mf::StartMessageFacility( mf::MessageFacilityService::MultiThread, pset );

  mf::SetApplicationName("MsgAnalyzer");
  mf::SetModuleName("module");
  mf::SetContext("context");

  // first log
  LOG_DEBUG("category") << "DEBUG: MessageFacility service started";
  LOG_INFO("category") << "INFO: MessageFacility service started";

  // start MA dialog
  MsgAnalyzerDlg dialog(cfg,partition);

  QSettings settings("NOvA DAQ", "MsgAnalyzer");
  dialog.restoreGeometry(settings.value("geometry").toByteArray());
  dialog.show();

  return app.exec();
}
