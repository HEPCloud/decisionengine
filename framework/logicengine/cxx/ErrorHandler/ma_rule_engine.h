#ifndef ERROR_HANDLER_MA_RULE_ENGINE_H
#define ERROR_HANDLER_MA_RULE_ENGINE_H

#include <ErrorHandler/ma_condition.h>
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

      void
      reset_rules()
      {
        for (auto& pr : rmap)
          pr.second.reset();
      }

    private:
      // merge notification list from conditions
      void merge_notify_list(notify_list_t& n_list,
                             conds_t const& c_list,
                             notify_t type);

      // evaluates the domain / status of all rules in the notification list
      void evaluate_rules_domain(notify_list_t& notify_domain);
      void evaluate_rules(notify_list_t& notify_status,
                          std::map<string_t, strings_t>& actions,
                          std::map<string_t, std::map<string_t, bool>>& facts);

    private:
      // configuration
      fhicl::ParameterSet pset{};

      // map of conditions
      cond_map_t cmap{};
      strings_t cnames{};

      // map of rules
      rule_map_t rmap{};
      strings_t rnames{};
    };

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
