#ifndef ERROR_HANDLER_MA_TIMING_EVENT_H
#define ERROR_HANDLER_MA_TIMING_EVENT_H

#include <ErrorHandler/ma_types.h>
#include <boost/thread/mutex.hpp>
#include <queue>

namespace novadaq {
namespace errorhandler {

class ma_condition;

class ma_timing_event
{
public:
  ma_timing_event(time_t t, ma_condition & c, size_t src, size_t tgt)
    : ts(t), cond(&c), s_idx(src), t_idx(tgt) { }

  time_t timestamp() const { return ts; }
  ma_condition & condition() const { return *cond; }
  size_t source_idx() const { return s_idx; }
  size_t target_idx() const { return t_idx; }

private:
  time_t ts;
  ma_condition * cond;
  size_t s_idx;
  size_t t_idx;
};

struct ma_timing_event_order
{
  bool operator()(ma_timing_event const & e1, ma_timing_event const & e2) const
  { return e1.timestamp() > e2.timestamp(); }
};

typedef std::priority_queue< ma_timing_event
                           , std::vector<ma_timing_event>
                           , ma_timing_event_order > event_queue_t;

class ma_timing_events
{
public:
  ma_timing_events()
    : queue(), lock() { }

  event_queue_t const & event_queue() const { return queue; }
  event_queue_t       & event_queue()       { return queue; }

private:
  event_queue_t queue;

public:
  boost::mutex lock;
};


}
}

#endif
