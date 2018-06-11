
#include <ErrorHandler/ma_participants.h>

#include <stdexcept>
#include <sstream>

using namespace novadaq::errorhandler;

// -----------------------------------------------------------------
// add group

void ma_participants::add_group( string_t const & group )
{
  groups_t::const_iterator it = groups.find(group);

  if( it!=groups.end() )
    throw std::runtime_error( group + " already exists while creating new group");

  string_set_t apps;
  groups.insert( std::make_pair(group, apps) );
}

void ma_participants::add_group( string_t const & group, size_t size )
{
  groups_t::const_iterator it = groups.find(group);

  if( it!=groups.end() )
    throw std::runtime_error( group + " already exists while creating new group");

  string_set_t apps;
  std::stringstream ss;

  for( size_t i=0; i<size; ++i )
  {
    ss.str( group );
    ss << "-" << i;
    apps.insert( ss.str() );
    all_apps.insert( ss.str() );
  }
  
  groups.insert( std::make_pair(group, apps) );
}

// -----------------------------------------------------------------
// add participant

void ma_participants::add_participant( string_t const & group
                                            , string_t const & app )
{
  groups_t::iterator it = groups.find(group);

  if( it==groups.end() )
    throw std::runtime_error( group + " does not exist while inserting participants");

  it->second.insert(app);
  all_apps.insert(app);
}

void ma_participants::add_participant( string_t const & app )
{
  ungrouped_apps.insert(app);
  all_apps.insert(app);
}

// -----------------------------------------------------------------
// get count

size_t ma_participants::
         get_group_participant_count( string_t const & group ) const
{
  groups_t::const_iterator it = groups.find(group);

  if( it==groups.end() )
    throw std::runtime_error( group + " does not exist while getting participant count");

  return it->second.size();
}

size_t ma_participants::
         get_participant_count( ) const
{
  return all_apps.size();
}


// -----------------------------------------------------------------
// reset
void ma_participants::reset( )
{
  ungrouped_apps.clear();
  all_apps.clear();
  groups.clear();
}









