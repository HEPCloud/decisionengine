#include <ErrorHandler/ma_action_mail.h>

#include <unistd.h>
#include <iostream>
#include <sstream>
#include <stdio.h>
//#include <sys/types.h>
//#include <sys/wait.h>

using namespace novadaq::errorhandler;

REG_MA_ACTION( mail, ma_action_mail )

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

ma_action_mail::ma_action_mail( ma_rule const * rule, pset_t const & pset )
: ma_action( rule, pset )
{

  std::stringstream ss;
  //ss << (std::string)getenv("FHICL_FILE_PATH");
  ss << (std::string)getenv("SRT_PRIVATE_CONTEXT") << ":"
     << (std::string)getenv("SRT_PUBLIC_CONTEXT") << ":.";
  std::string token;
  std::stringstream mail_file;

  // search for mail bash file using FHICL_FILE_PATH
  while( std::getline(ss,token,':') ){
    mail_file.str("");   
    mail_file << token << "/ErrorHandler/cxx/config/send_mail.sh";
    std::stringstream sys_check;
    sys_check << "-f " << mail_file.str();
    // exit loop if file exists
    if( system(&sys_check.str()[0]) )  break;
  }

  script_name = mail_file.str(); //pset.get<std::string>("name");
  script_para = pset.get<std::string>("param", std::string());
      
  param.init(rule, script_para);
}

bool ma_action_mail::exec()
{
  RunCommand(script_name, param.message());
  return true;
}


