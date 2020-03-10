#ifndef ERROR_HANDLER_MA_RULE_ENGINE_H
#define ERROR_HANDLER_MA_RULE_ENGINE_H

#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_rule.h>
#include <ErrorHandler/ma_types.h>

#include <ErrorHandler/ma_timing_event.h>

namespace novadaq {
  namespace errorhandler {

    class ma_rule_engine {
    public:
      ma_rule_engine(Json::Value const& facts,
                     Json::Value const& rules);

      void execute(std::map<std::string, bool> const& fact_vals,
                   std::map<std::string, strings_t>& actions,
                   std::map<std::string, std::map<string_t, bool>>& facts);

    private:
      // merge notification list from conditions
      notify_list_t merge_notify_list(conds_t const& c_list);

      // evaluates the domain / status of all rules in the notification list
      void evaluate_rules(notify_list_t& notify_status,
                          std::map<string_t, strings_t>& actions,
                          std::map<string_t, std::map<string_t, bool>>& facts);

      fact_map_t cmap{};
      rule_map_t rmap{};
    };

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
