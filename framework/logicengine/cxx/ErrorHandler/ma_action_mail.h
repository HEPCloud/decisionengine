#ifndef ERRORHANDER_MA_ACTION_MAIL_H
#define ERRORHANDER_MA_ACTION_MAIL_H

#include <ErrorHandler/ma_action.h>
#include <ErrorHandler/ma_richmsg.h>

namespace novadaq {
namespace errorhandler {

class ma_action_mail : public ma_action
{

public:

  ma_action_mail(ma_rule const * rule, pset_t const & pset);
  virtual ~ma_action_mail() {}

  virtual bool exec();

private:

  std::string script_name;
  std::string script_para;

  ma_richmsg param;

};

} // end of namespace errorhandler
} // end of namespace novadaq


#endif
