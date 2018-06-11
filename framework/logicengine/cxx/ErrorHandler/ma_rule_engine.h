#ifndef ERROR_HANDLER_MA_RULE_ENGINE_H
#define ERROR_HANDLER_MA_RULE_ENGINE_H

#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_condition.h>
#include <ErrorHandler/ma_rule.h>
#include <ErrorHandler/ma_participants.h>

#include <ErrorHandler/ma_timing_event.h>
#include <boost/thread.hpp>

namespace novadaq {
namespace errorhandler {

class ma_rule_engine
{
public:
  
  // c'tor
  ma_rule_engine( fhicl::ParameterSet const & pset
                , alarm_fn_t alarm 
                , cond_match_fn_t cond_match );

  ma_rule_engine( Json::Value const & facts
                , Json::Value const & rules
                , alarm_fn_t alarm 
                , cond_match_fn_t cond_match );

  // public method, call to run the rule engine
  void feed( msg_t const & msg );

  // public method, call by the LogicEngine
  void execute( std::map<std::string, bool> const & fact_vals
              , std::map<std::string, strings_t> & actions
              , std::map<std::string, std::map<string_t, bool>> & facts );

  // public accessor for cond map and rule map
  size_t cond_size() const { return cmap.size(); }
  size_t rule_size() const { return rmap.size(); }

  const strings_t & cond_names() const { return cnames; }
  const strings_t & rule_names() const { return rnames; }

  bool is_EHS() const { return EHS; }

  // get the raw configuration ParameterSet object
  fhicl::ParameterSet
    get_configuration() const
    { return pset; }

  // get condition fields
  const string_t &
    cond_description( string_t const & name ) const
    { return find_cond_by_name(name).description(); }

  const string_t &
    cond_sources    ( string_t const & name ) const
    { return find_cond_by_name(name).sources_str(); }

  const string_t & 
    cond_regex      ( string_t const & name ) const
    { return find_cond_by_name(name).regex(); }

  int
    cond_msg_count  ( string_t const & name ) const
    { return find_cond_by_name(name).get_msg_count(); }

  // get rule fields
  const string_t &
    rule_description( string_t const & name ) const
    { return find_rule_by_name(name).description(); }

  const string_t & 
    rule_expr ( string_t const & name ) const
    { return find_rule_by_name(name).cond_expr(); }

  const strings_t &
    rule_cond_names( string_t const & name ) const
    { return find_rule_by_name(name).cond_names(); }

  int
    rule_alarm_count ( string_t const & name ) const
    { return find_rule_by_name(name).get_alarm_count(); }

  // set rule enable/disable status
  void enable_rule( string_t const & name, bool flag )
    { find_rule_by_name(name).enable(flag); }

  // enable/disable EHS
  void enable_EHS( bool flag )
    { EHS = flag; }

  // reset a rule to its ground state (reset alarms and domains)
  void reset_rule( string_t const & name )
    { find_rule_by_name(name).reset(); }

  void reset_rules( )
    { for(rule_map_t::iterator it=rmap.begin(); it!=rmap.end(); ++it) 
        it->second.reset(); }

  // reset conditions
  void reset_cond( string_t const & name )
    { find_cond_by_name(name).reset(); }

  void reset_conds( )
    { for(cond_map_t::iterator it=cmap.begin(); it!=cmap.end(); ++it) 
        it->second.reset(); }

  // reset all
  void reset( )
    { reset_conds(); reset_rules(); }

  // participants
  void add_participant_group( string_t const & group )
    { ma_participants::instance().add_group( group ); }

  void add_participant_group( string_t const & group, size_t size )
    { ma_participants::instance().add_group( group, size ); }

  void add_participant( string_t const & group, string_t const & app )
    { ma_participants::instance().add_participant( group, app ); }

  void add_participant( string_t const & app )
    { ma_participants::instance().add_participant( app ); }

  size_t get_group_participant_count( string_t const & group ) const
    { return ma_participants::instance().get_group_participant_count(group); }

  size_t get_participant_count( ) const
    { return ma_participants::instance().get_participant_count(); }


private: 

  // initialize the rule engine with configuration file
  void init_engine( Json::Value const & pset );
  void init_minimal_engine( Json::Value const & facts, Json::Value const & rules );

  // event worker
  void event_worker( );

  // merge notification list from conditions
  void merge_notify_list( notify_list_t & n_list
                        , conds_t const & c_list
                        , notify_t type );

  // evaluates the domain / status of all rules in the notification list
  void evaluate_rules_domain( notify_list_t & notify_domain );
  void evaluate_rules( notify_list_t & notify_status );
  void evaluate_rules( notify_list_t & notify_status
                     , std::map<string_t, strings_t> & actions
                     , std::map<string_t, std::map<string_t, bool>> & facts );

  // find condition/rule with given name
  const ma_condition & find_cond_by_name( string_t const & name ) const;
        ma_condition & find_cond_by_name( string_t const & name );

  const ma_rule      & find_rule_by_name( string_t const & name ) const;
        ma_rule      & find_rule_by_name( string_t const & name );

private: 

  // configuration
  fhicl::ParameterSet pset;

  // map of conditions
  cond_map_t  cmap;
  strings_t   cnames;

  // map of rules
  rule_map_t  rmap;
  strings_t   rnames;

  // callbacks
  alarm_fn_t      alarm_fn;
  cond_match_fn_t cond_match_fn;

  // a list of scheduled events
  ma_timing_events events;

  // event thread
  // boost::thread event_worker_t;

  // whether this engine is an Error Handler Supervisor
  bool EHS;
};


} // end of namespace errorhandler
} // end of namespace novadaq


#endif
