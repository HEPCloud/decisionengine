#include <ErrorHandler/ma_action_script.h>

#include <unistd.h>
//#include <sys/types.h>
//#include <sys/wait.h>

using namespace novadaq::errorhandler;

REG_MA_ACTION( script, ma_action_script )

namespace {

  int RunCommand(std::string const & strCmd, std::string const & strParam)
  {
    int iForkId, iStatus;
    iForkId = vfork();
    if (iForkId == 0) // This is the child 
    {
      std::string command = strCmd + " " + strParam;

      iStatus = execl("/bin/sh","sh","-c", command.c_str(), (char*) NULL);
      exit(iStatus);  // We must exit here, 
                      // or we will have multiple
                      // mainlines running...  
    }
    else if (iForkId > 0) // Parent, no error
    {
      iStatus = 0;
    }
    else  // Parent, with error (iForkId == -1)
    {
      iStatus = -1;
    }
    return(iStatus);
  } 

}

ma_action_script::ma_action_script( ma_rule const * rule, pset_t const & pset )
: ma_action( rule, pset )
{
  script_name = pset.get<std::string>("name");
  script_para = pset.get<std::string>("param", std::string());

  param.init(rule, script_para);
}

bool ma_action_script::exec()
{
  RunCommand(script_name, param.message());
  return true;
}


