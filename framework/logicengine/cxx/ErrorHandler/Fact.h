#ifndef ERROR_HANDLER_FACT_H
#define ERROR_HANDLER_FACT_H

// from novadaq
#include <ErrorHandler/ma_hitmap.h>
#include <ErrorHandler/ma_timing_event.h>
#include <ErrorHandler/ma_types.h>

// from ups
#include <boost/regex.hpp>

// sys headers
#include <list>
#include <map>
#include <vector>

namespace novadaq {
  namespace errorhandler {

    typedef boost::regex regex_t;
    typedef std::vector<boost::regex> vregex_t;

    class Fact {
    public:

      explicit Fact(string_t const& name);

      // reset the condition to its ground state
      void reset();

      // init
      /*!*/ void init();

      // public method that forces the status to the passed value
      void force(bool val, conds_t& status);

      // get fields from last message
      sev_code_t
      get_msg_severity() const
      {
        return last_sev_;
      }
      const string_t&
      get_msg_category() const
      {
        return last_cat_;
      }
      const string_t&
      get_msg_source() const
      {
        return last_src_;
      }
      const string_t&
      get_msg_target() const
      {
        return last_tgt_;
      }
      const string_t&
      get_msg_body() const
      {
        return last_bdy_;
      }
      string_t
      get_msg_group(size_t i) const
      {
        if (i > last_what_.size())
          throw std::runtime_error("group does not exist");
        return string_t(last_what_[i].first, last_what_[i].second);
      }

      // get a range of src/target
      void
      get_cond_range(ma_cond_domain d,
                     ma_cond_range& src,
                     ma_cond_range& tgt) const
      {
        return hitmap.get_cond_range(d, src, tgt);
      }

      // returns if the condition has been triggered at given spot(src, target)
      bool
      get_status(ma_cond_domain v) const
      {
        return hitmap.get_status(v);
      }

      // returns if the condition status has been defined on all spots
      bool get_defined() const;

      // notification list
      void
      push_notify_status(ma_rule* rule)
      {
        push_notify(notify_on_status, rule);
      }

      void
      push_notify(notify_list_t& list, ma_rule* rule)
      {
        if (std::find(list.begin(), list.end(), rule) == list.end())
          list.push_back(rule);
      }

      /*!*/ void
      sort_notify_lists()
      {
        notify_on_status.sort();
      }

      /*!*/ const notify_list_t&
      get_notify_list()
      {
        return notify_on_status;
      }

      int
      trigger_count() const
      {
        return tc;
      }
      int
      timespan() const
      {
        return ts;
      }
      bool
      at_least() const
      {
        return at_least_;
      }
      bool
      at_most() const
      {
        return !at_least_;
      }
      bool
      persistent() const
      {
        return persistent_;
      }
      ma_timing_events&
      timing_events()
      {
        return events;
      }

      // return a view to the hitmap given a ma_cond_domain
      const hitmap_view_t
      get_domain_view(ma_cond_domain const& domain)
      {
        return hitmap.get_domain_view(domain);
      }

    private:
      // condition description
      string_t description_;

      string_t srcs_str;
      vregex_t e_srcs;

      string_t cats_str;
      vregex_t e_cats;

      // match condition
      string_t regex_str;
      regex_t e;

      // hitmap and granularity
      int tc;
      bool at_least_;
      int ts;
      bool persistent_;     // persistent cond. never turns off
      ma_hitmap hitmap;

      // timing events
      ma_timing_events& events;

      // temp variables used in matching
      string_t src_;
      string_t tgt_;
      string_t cat_;
      string_t bdy_;
      boost::smatch what_;

      sev_code_t last_sev_;
      string_t last_src_;
      string_t last_tgt_;
      string_t last_cat_;
      string_t last_bdy_;
      boost::smatch last_what_;

      // notification lists
      notify_list_t notify_on_status;
    };

    using Facts = std::vector<Fact*>;
    typedef std::map<string_t, Fact> fact_map_t;

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
