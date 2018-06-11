
#include <ErrorHandler/ma_rule_engine.h>

//#include <cetlib/filepath_maker.h>
//#include <fhiclcpp/make_ParameterSet.h>

using fhicl::ParameterSet;

using namespace novadaq::errorhandler;

ma_rule_engine::ma_rule_engine( fhicl::ParameterSet const & pset
                              , alarm_fn_t alarm 
                              , cond_match_fn_t cond_match )
: pset   ( pset )
, cmap   ( )
, cnames ( )
, rmap   ( )
, rnames ( )
, alarm_fn      ( alarm )
, cond_match_fn ( cond_match )
, events ( )                              
//, event_worker_t ( )
, EHS    ( false )
{
  init_engine( pset );
}

ma_rule_engine::ma_rule_engine( Json::Value const & conf_facts
                              , Json::Value const & conf_rules
                              , alarm_fn_t alarm 
                              , cond_match_fn_t cond_match )
: pset   ( )
, cmap   ( )
, cnames ( )
, rmap   ( )
, rnames ( )
, alarm_fn      ( alarm )
, cond_match_fn ( cond_match )
, events ( )                              
//, event_worker_t ( )
, EHS    ( false )
{
  init_minimal_engine( conf_facts, conf_rules );
}


void ma_rule_engine::init_engine( fhicl::ParameterSet const & pset )
{
  // Error Handling Supervisor -- EHS
  EHS = pset["EHS"].asBool();

  ParameterSet conds = pset["conditions"];
  ParameterSet rules = pset["rules"];

  cnames = conds.getMemberNames();
  rnames = rules.getMemberNames();

  // go through all conditions
  for( size_t i=0; i<cnames.size(); ++i )
  {
    ParameterSet nulp;

    ParameterSet cond   = conds[cnames[i]];
    ParameterSet rate   = cond["rate"];
    ParameterSet gran   = cond["granularity"];

    // decide whether "at_least" or "at_most"
    int occur, occur_at_most, occur_at_least;
    bool at_most  = rate["occur_at_most"].asInt();
    bool at_least = rate["occur_at_least"].asInt();

    // compatible with the previous "occurence" keyword
    if (!at_least) at_least = rate["occurence"].asInt();

    if (at_most && at_least)
    {
      throw std::runtime_error("rule_engine::init_engine() cannot have both 'occur_at_least' "
          "and 'occur_at_most' in the rate entry, in condition " + cnames[i]);
    }
    else if (!at_most && !at_least)
    {
      occur = 1;
      at_least = true;
    }
    else
    {
      occur = at_least ? occur_at_least : occur_at_most;
    }

    // construct the condition object
    ma_condition c( cond["description"].asString()
                  , cond["severity"].asString()
                  , strings_t(1, "*") // cond["source"].asString()
                  , strings_t(1, "*") // cond.get<strings_t>("category", strings_t(1, "*"))
                  , cond["regex"].asString()
                  , cond["test"].asString()
                  , cond["persistent"].asBool()
                  , occur
                  , at_least
                  , rate["timespan"].asInt()
                  , gran["per_source"].asBool()
                  , gran["per_target"].asBool()
                  , gran["target_group"].asInt()
                  , events
                  );

    // push the condition to the container, and parse the test function
    cond_map_t::iterator it = cmap.insert(std::make_pair(cnames[i], c)).first;

    // init after the condition has been inserted into the map
    it->second.init();
  }

  // go through all rules
  for( size_t i=0; i<rnames.size(); ++i )
  {
    ParameterSet nulp;

    ParameterSet rule = rules[rnames[i]];

    // construct the rule object
    ma_rule r( rnames[i]
             , rule["description"].asString()
             , false //, rule["repeat_alarm"].asBool()
             , 0     //, rule["holdoff"].asInt()
             );

    // push the rule to the container
    rule_map_t::iterator it = rmap.insert(std::make_pair(rnames[i], r)).first;
    
    // parse the condition expression and alarm message
    // this is done in a two-step method (init the object, push into container
    // then parse) because the parse process involves updating the conditions
    // notification list which needs the pointer to the ma_rule object. There-
    // fore we push the ma_rule object into the container first, then do the
    // parse
    it->second.parse( rule["expression"].asString()
                    , rule["message"].asString()
                    , rule["action"]
                    , &cmap );
  }

  // for all conditions sort their notification lists
  cond_map_t::iterator it = cmap.begin();
  for( ; it!=cmap.end(); ++it ) it->second.sort_notify_lists();

  // timing event worker thread
  // event_worker_t = boost::thread(&ma_rule_engine::event_worker, this);
}

void ma_rule_engine::init_minimal_engine( Json::Value const & facts, Json::Value const & rules )
{
  // Error Handling Supervisor -- EHS
  EHS = false;

  // fact names and rule names
  cnames = facts.getMemberNames();
  rnames = rules.getMemberNames();

  // find all facts from the rule's actions
  for( size_t i=0; i<rnames.size(); ++i )
  {
    ParameterSet rule = rules[rnames[i]];

    if (rule.isMember("facts"))
    {
      for (auto const & f : rule["facts"]) 
      {
        cnames.emplace_back(f.asString());
      }
    }
  }

  // create all facts
  for( size_t i=0; i<cnames.size(); ++i )
  {
    // construct the condition object
    ma_condition c( cnames[i] );

    // push the condition to the container, and parse the test function
    cond_map_t::iterator it = cmap.insert(std::make_pair(cnames[i], c)).first;

    // init after the condition has been inserted into the map
    it->second.init();
  }

  // go through all rules
  for( size_t i=0; i<rnames.size(); ++i )
  {
    ParameterSet rule = rules[rnames[i]];

    // construct the rule object
    ma_rule r( rnames[i]
             , rnames[i]
             , false //, rule["repeat_alarm"].asBool()
             , 0     //, rule["holdoff"].asInt()
             );

    // push the rule to the container
    rule_map_t::iterator it = rmap.insert(std::make_pair(rnames[i], r)).first;
    
    // parse the condition expression and alarm message
    // this is done in a two-step method (init the object, push into container
    // then parse) because the parse process involves updating the conditions
    // notification list which needs the pointer to the ma_rule object. There-
    // fore we push the ma_rule object into the container first, then do the
    // parse

    std::vector<std::string> actions;
    std::vector<std::string> false_actions;
    std::vector<std::string> facts;

    for (auto const & action : rule["actions"])  
      actions.emplace_back(action.asString());

    for (auto const & action : rule["false_actions"])  
      false_actions.emplace_back(action.asString());

    for (auto const & fact   : rule["facts"  ])  
      facts.emplace_back(fact.asString());

    it->second.parse( rule["expression"].asString()
                    , rule["message"].asString()
                    , actions
                    , false_actions
                    , facts
                    , &cmap );
  }

  // for all conditions sort their notification lists
  cond_map_t::iterator it = cmap.begin();
  for( ; it!=cmap.end(); ++it ) it->second.sort_notify_lists();
}

void ma_rule_engine::event_worker()
{
#if 0
  while(true)
  {
    // get current second
    time_t now = time(0);


    // loop for all past due events, and execute them
    {
      // scoped lock
      boost::mutex::scoped_lock lock(events.lock);

      conds_t status;
      event_queue_t & eq = events.event_queue();

      while (!eq.empty() && eq.top().timestamp() < now)
      {
        ma_timing_event const & e = eq.top();
        e.condition().event(e.source_idx(), e.target_idx(), e.timestamp(), status);
        eq.pop();
      }

      // build notify list
      notify_list_t notify_status;
      merge_notify_list( notify_status, status, STATUS_NOTIFY );

      // rules->evaluate
      evaluate_rules( notify_status );
    }

    sleep(1);
  }
#endif
}

void ma_rule_engine::feed( msg_t const & msg )
{
  // reaction starters
  conds_t status;
  conds_t source;
  conds_t target;

  // loop through conditions
  {
    cond_map_t::iterator it = cmap.begin();
    for( ; it!=cmap.end(); ++it ) 
      if( it->second.match( msg, status, source, target ) )
        cond_match_fn( it->first ); // callback fn for condition match
  }

  // notification mechanism

  // merge notification lists from reaction starters
  notify_list_t notify_status;
  notify_list_t notify_domain;

  merge_notify_list( notify_status, status, STATUS_NOTIFY );
  merge_notify_list( notify_domain, source, SOURCE_NOTIFY );
  merge_notify_list( notify_domain, target, TARGET_NOTIFY );

  // update domains
  evaluate_rules_domain( notify_domain );

  // loop to update status
  evaluate_rules( notify_status );
}

void ma_rule_engine::execute( std::map<std::string, bool> const & fact_vals
                            , std::map<std::string, strings_t> & actions
                            , std::map<std::string, std::map<string_t, bool>> & facts )
{
  // reaction starters
  conds_t status;
  conds_t source;
  conds_t target;

  // loop through conditions
  for ( std::map<std::string, bool>::const_iterator it = fact_vals.begin();
        it != fact_vals.end(); ++it )
  {
      cond_map_t::iterator cit = cmap.find(it->first);

      if (cit == cmap.end())
          throw std::runtime_error("invalid fact name");

      cit->second.force(it->second, status, source, target);
  }

  // notification mechanism

  // merge notification lists from reaction starters
  notify_list_t notify_status;
  notify_list_t notify_domain;

  merge_notify_list( notify_status, status, STATUS_NOTIFY );
  merge_notify_list( notify_domain, source, SOURCE_NOTIFY );
  merge_notify_list( notify_domain, target, TARGET_NOTIFY );

  // update domains
  evaluate_rules_domain( notify_domain );

  // prepare for the new facts
  std::map<string_t, std::map<string_t, bool>> new_facts;  // rule -> { f1 : true, f2 : false }
  std::map<string_t, bool> new_fact_vals;                  // fact -> bool

  // loop to update status, and store the new facts into the new_facts map
  evaluate_rules( notify_status, actions, new_facts );

  // exam the new facts
  for (auto const & rfs : new_facts)
  {
      for (auto const & f : rfs.second)
      {
          new_fact_vals.insert(std::make_pair(f.first, f.second));
      }
  }

  // insert the new facts into the facts map
  facts.insert(new_facts.begin(), new_facts.end());

  // if there's any new fact values, we should call the execute again
  if (!new_fact_vals.empty())
  {
      execute(new_fact_vals, actions, facts);
  }
}

void ma_rule_engine::evaluate_rules_domain( notify_list_t & notify_domain )
{
  notify_list_t::iterator it = notify_domain.begin();
  for( ; it!=notify_domain.end(); ++it )
    (*it)->evaluate_domain();
}

void ma_rule_engine::evaluate_rules( notify_list_t & notify_status )
{
  notify_list_t::iterator it = notify_status.begin();

  for( ; it!=notify_status.end(); ++it )
  {
    if( (*it)->evaluate() )
    {
      // alarm message
      alarm_fn((*it)->name(), (*it)->get_alarm_message());
    }
  }
}

void ma_rule_engine::evaluate_rules( notify_list_t & notify_status
                                   , std::map<string_t, strings_t> & actions
                                   , std::map<string_t, std::map<string_t, bool>> & facts )
{
  notify_list_t::iterator it = notify_status.begin();

  for( ; it!=notify_status.end(); ++it )
  {
    if( !(*it)->evaluable() ) continue;

    if( (*it)->evaluate() )
    {
      // alarm message
      alarm_fn((*it)->name(), (*it)->get_alarm_message());

      // form the actions
      actions.emplace((*it)->name(), (*it)->get_action_names());

      // for the new facts
      std::map<string_t, bool> rule_facts;
      auto const & rule_fact_names = (*it)->get_chained_fact_names();

      for (auto const & name : rule_fact_names)
        rule_facts.emplace(name, true);

      facts.emplace((*it)->name(), rule_facts);
    }
    else
    {
      // form the actions from rule's false actions
      actions.emplace((*it)->name(), (*it)->get_false_action_names());

      // still need to form the facts, but with false values
      std::map<string_t, bool> rule_facts;
      auto const & rule_fact_names = (*it)->get_chained_fact_names();

      for (auto const & name : rule_fact_names)
        rule_facts.emplace(name, false);

      facts.emplace((*it)->name(), rule_facts);
    }
  }
}

void ma_rule_engine::merge_notify_list( notify_list_t & n_list
                                      , conds_t const & c_list
                                      , notify_t type )
{
  conds_t::const_iterator it = c_list.begin();
  for( ; it!=c_list.end(); ++it ) 
  {
    notify_list_t notify((*it)->get_notify_list(type));
    n_list.merge(notify);
    n_list.unique();
  }
}

const ma_condition &
  ma_rule_engine::find_cond_by_name( string_t const & name ) const
{
  cond_map_t::const_iterator it = cmap.find(name);
  if( it == cmap.end() )
    throw std::runtime_error("rule_engine::find_cond_by_name() name not found");
  return it->second;
}

ma_condition &
  ma_rule_engine::find_cond_by_name( string_t const & name )
{
  cond_map_t::iterator it = cmap.find(name);
  if( it == cmap.end() )
    throw std::runtime_error("rule_engine::find_cond_by_name() name not found");
  return it->second;
}

const ma_rule &
  ma_rule_engine::find_rule_by_name( string_t const & name ) const
{
  rule_map_t::const_iterator it = rmap.find(name);
  if( it == rmap.end() )
    throw std::runtime_error("rule_engine::find_rule_by_name() name not found");
  return it->second;
}

ma_rule &
  ma_rule_engine::find_rule_by_name( string_t const & name )
{
  rule_map_t::iterator it = rmap.find(name);
  if( it == rmap.end() )
    throw std::runtime_error("rule_engine::find_rule_by_name() name not found");
  return it->second;
}





