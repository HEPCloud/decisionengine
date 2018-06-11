//#define NDEBUG

#include <iostream>

#include "messagefacility/MessageLogger/MessageLogger.h"

using namespace mf;

int main()
{

  // Start MessageFacility Service
  StartMessageFacility( MessageFacilityService::MultiThread
                      , MessageFacilityService::logCS() );

  // Set application name (use process name by default)
  SetApplicationName("app1");

  // Set module name and context for the main thread
  SetModuleName("eh-test");
  SetContext("eh-test-1");

  // Issue messages with different severity levels
  LogError("cat1|cat2") << "This is an ERROR message.";
  LogWarning("catwarn") << "Followed by a WARNING message.";

  // Switch context
  SetContext("eh-test-2");

  // Logs
  LogError("catError")     << "Error information.";
  LogWarning("catWarning") << "Warning information.";
  LogInfo("catInfo")       << "Info information.";
  LogDebug("debug")        << "DEBUG information.";

  //sleep(2);

  return 0;
}
