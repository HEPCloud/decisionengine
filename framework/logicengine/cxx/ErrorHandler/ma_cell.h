#ifndef ERROR_HANDLER_MA_FREQUENCY_H
#define ERROR_HANDLER_MA_FREQUENCY_H

#include <ErrorHandler/ma_types.h>

namespace novadaq {
  namespace errorhandler {

    class ma_cell {
    public:
      // reset to ground state
      void reset();

      // simplified hit
      bool hit(bool val);

      // get status
      bool
      is_on() const
      {
        return on;
      }

      bool
      is_defined() const
      {
        return defined;
      }

      // get number of messages
      size_t
      get_message_count() const
      {
        return msgs.size();
      }

      // get messages
      const msgs_t&
      get_messages() const
      {
        return msgs;
      }

      // get latest message
      string_t
      get_latest_message() const
      {
        assert(!msgs.empty());
        return msgs.back().message();
      }

      /* // get group */
      /* string_t */
      /* get_message_group(size_t i) const */
      /* { */
      /*   if (i > what_.size()) throw std::runtime_error("group does not exist"); */
      /*   return string_t(what_[i].first, what_[i].second); */
      /* } */

    private:
      msgs_t msgs{};
      bool on{false};
      bool defined{false};
    };

    typedef boost::multi_array<ma_cell, 2> hitmap_t;
    typedef hitmap_t::index index_t;

    typedef hitmap_t::const_array_view<2>::type hitmap_view_t;
    typedef hitmap_view_t ma_cond_domain_view;
    typedef ma_cond_domain_view::const_iterator ma_cond_domain_view_iter;
    typedef std::vector<ma_cond_domain_view_iter> ma_cond_domain_view_iters;
    typedef std::vector<ma_cond_domain_view> ma_domain_view;
    typedef ma_domain_view::const_iterator ma_domain_view_iter;
    typedef std::list<ma_domain_view> ma_domain_views;

    //     typedef boost::multi_array_types::index_range range;

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
