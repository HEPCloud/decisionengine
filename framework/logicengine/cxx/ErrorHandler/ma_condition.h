#ifndef ERROR_HANDLER_MA_CONDITION_H
#define ERROR_HANDLER_MA_CONDITION_H

// from novadaq
#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_utils.h>
#include <ErrorHandler/ma_hitmap.h>
#include <ErrorHandler/ma_cond_test_expr.h>
#include <ErrorHandler/ma_timing_event.h>

// from ups
#include <boost/regex.hpp>
#include <boost/shared_ptr.hpp>

// sys headers
#include <list>
#include <vector>
#include <map>

namespace novadaq {
namespace errorhandler {

typedef boost::regex                       regex_t;
typedef std::vector<boost::regex>          vregex_t;

// MsgAnalyzer Rule
class ma_condition
{
public:

  // c'tor full
  ma_condition( string_t  const & desc
              , string_t  const & sev
              , strings_t const & sources
              , strings_t const & categories
              , string_t  const & regex
              , string_t  const & test
              , bool              persistent_cond
              , int               trigger_count
              , bool              at_least
              , int               timespan
              , bool              per_source
              , bool              per_target
              , int               target_group
              , ma_timing_events & events
              );

 
  // c'tor minified
  ma_condition( string_t  const & name );

  // reset the condition to its ground state
  void reset();

  // init
  void init();

  // public method that gets called when new message comes in
  bool match( msg_t const & msg
            , conds_t & status
            , conds_t & source 
            , conds_t & target );

  // public method that forces the status to the passed value
  bool force( bool val
            , conds_t & status
            , conds_t & source 
            , conds_t & target );

  // scheduled event
  bool event( size_t src, size_t tgt, time_t t, conds_t & status );

  // get fields
  const string_t & description() const { return description_; }
  const string_t & regex()       const { return regex_str; }
  const string_t & sources_str() const { return srcs_str; }

  // update fields with lastest match message
  void update_fields();

  // get catched message count
  int              get_msg_count   ( ) const { return catched_messages; }

  // get fields from last message
      sev_code_t   get_msg_severity( ) const { return last_sev_; }
  const string_t & get_msg_category( ) const { return last_cat_; }
  const string_t & get_msg_source  ( ) const { return last_src_; }
  const string_t & get_msg_target  ( ) const { return last_tgt_; }
  const string_t & get_msg_body    ( ) const { return last_bdy_; }
        string_t   get_msg_group   ( size_t i ) const
    { if(i>last_what_.size()) throw std::runtime_error("group does not exist");
      return string_t(last_what_[i].first, last_what_[i].second); }

  // return index of the src/tgt string, or -2 if not found
  int find_source(string_t const & src) { return hitmap.find_source(src); }
  int find_target(string_t const & tgt) { return hitmap.find_target(tgt); }
  int find_arg(string_t const & arg, arg_t type)
    { return (type==SOURCE) ? hitmap.find_source(arg) : hitmap.find_target(arg); }

  // get src/tgt list
  const idx_t & get_sources() const { return hitmap.get_sources(); }
  const idx_t & get_targets() const { return hitmap.get_targets(); }
  const idx_t & get_args(arg_t type) const
    { if( type==SOURCE ) return hitmap.get_sources();
      if( type==TARGET ) return hitmap.get_targets();
      throw std::runtime_error("condition::get_args() unsupported arg type"); }

  // get src/tgt string. precond: size()>0, 0<=idx<size() or idx=ANY
  const string_t & get_source( ma_cond_domain v ) const 
    { return hitmap.get_source(v); }
  const string_t & get_target( ma_cond_domain v ) const 
    { return hitmap.get_target(v); }
  string_t get_arg( ma_cond_domain v, arg_t type ) const
    { if( type==SOURCE ) return hitmap.get_source(v);
      if( type==TARGET ) return hitmap.get_target(v);
      if( type==MESSAGE) return hitmap.get_message(v);
      if( type>=GROUP1 ) return hitmap.get_message_group(v, (size_t)(type-GROUP1+1));
      throw std::runtime_error("condition::get_arg() unknow arg type");
    }

  // get a range of src/target
  void
    get_cond_range( ma_cond_domain d
                  , ma_cond_range & src
                  , ma_cond_range & tgt ) const
    { return hitmap.get_cond_range(d, src, tgt); }

  // returns if the condition has been triggered at given spot(src, target)
  bool
    get_status( ma_cond_domain v ) const
    { return hitmap.get_status(v); }

  // returns if the condition status has been defined at given spot(src, target)
  bool
    get_defined( ma_cond_domain v ) const
    { return hitmap.get_defined(v); }

  // returns if the condition status has been defined on all spots
  bool
    get_defined( ) const;

  int
    get_alarm_count( ma_cond_domain v, arg_t arg ) const
    { return hitmap.get_alarm_count(v, arg); }
      

  // notification list
  void push_notify_source( ma_rule * rule ) { push_notify(notify_on_source, rule); }
  void push_notify_target( ma_rule * rule ) { push_notify(notify_on_target, rule); }
  void push_notify_status( ma_rule * rule ) { push_notify(notify_on_status, rule); }

  void 
    push_notify( notify_list_t & list, ma_rule * rule )
    { 
      if( std::find(list.begin(), list.end(), rule) == list.end() )  
        list.push_back(rule); 
    } 

  void 
    sort_notify_lists( )
    { notify_on_source.sort(); notify_on_target.sort(); notify_on_status.sort(); }

  const notify_list_t &
    get_notify_list( notify_t type )
    {
      if( type == STATUS_NOTIFY )  return notify_on_status;
      if( type == SOURCE_NOTIFY )  return notify_on_source;
      if( type == TARGET_NOTIFY )  return notify_on_target;
      throw std::runtime_error("get_notify_list: unknow type");
    }

  int trigger_count() const { return tc; }
  int timespan()      const { return ts; }
  bool at_least()     const { return at_least_; }
  bool at_most()      const { return !at_least_; }
  bool per_source()   const { return ps; }
  bool per_target()   const { return pt; }
  bool persistent()   const { return persistent_; }
  ma_timing_events & timing_events() { return events; }

  // return a view to the hitmap given a ma_cond_domain
  const hitmap_view_t 
    get_domain_view( ma_cond_domain const & domain )
    { return hitmap.get_domain_view(domain); }

private:

  // extract severity, source, category, and message body
  // from message facility message
  void extract_fields (msg_t const & msg);

  bool match_srcs ( );
  bool match_cats ( );
  bool match_body ( );
  bool match_test ( );

private:

  // condition description
  string_t     description_;

  // filtering conditions
  sev_code_t   severity_;

  string_t     srcs_str;
  vregex_t     e_srcs;
  bool         any_src;

  string_t     cats_str;
  vregex_t     e_cats;
  bool         any_cat;

  // match condition
  match_type_t match_type;
  string_t     regex_str;
  regex_t      e;

  // test condition
  ma_cond_test_expr test_expr;

  // hitmap and granularity
  int          tc;
  bool         at_least_;
  int          ts;
  bool         ps;      // per_source
  bool         pt;      // per_target
  unsigned int t_group; // target_group
  bool         persistent_; // persistent cond. never turns off
  ma_hitmap    hitmap;

  // timing events
  ma_timing_events & events;

  // temp variables used in matching
  sev_code_t   sev_;
  string_t     src_;
  string_t     tgt_;
  string_t     cat_;
  string_t     bdy_;
  boost::smatch what_;

  sev_code_t   last_sev_;
  string_t     last_src_;
  string_t     last_tgt_;
  string_t     last_cat_;
  string_t     last_bdy_;
  boost::smatch last_what_;

  // notification lists
  notify_list_t notify_on_source;
  notify_list_t notify_on_target;
  notify_list_t notify_on_status;

  // total number of catched messages which has passed
  // filtering, match condition, and test condition. Does not 
  // matter if it passed the frequency test
  int catched_messages;

};

//typedef boost::shared_ptr<ma_condition> cond_sp;
//typedef std::list<cond_sp>              conds_t;
//typedef std::vector<cond_sp>            cond_vec_t;
//typedef std::map<string_t, cond_sp>     cond_map_t;

typedef std::vector<ma_condition *>       cond_vec_t;
typedef std::map<string_t, ma_condition>  cond_map_t;

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
