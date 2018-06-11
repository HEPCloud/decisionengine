#ifndef ERRORHANDLER_PARTICIPANTS_H
#define ERRORHANDLER_PARTICIPANTS_H

// ma_participants
// --------------------------------------------
// A singleton class that keeps track of current participants (applications
// who have sent a message facility message) in the DAQ system. Participants
// can be grouped to "groups", e.g., all "dcm"s can be grouped together. One
// may query the number of participants in a group


#include <string>
#include <vector>
#include <map>
#include <set>

namespace novadaq {
namespace errorhandler {

typedef std::string                      string_t;
typedef std::vector<std::string>         strings_t;
typedef std::set<std::string>            string_set_t;
typedef std::map<string_t, string_set_t> groups_t;

class ma_participants
{
private:

  ma_participants()
    : ungrouped_apps(), all_apps(), groups() 
    { }

public:

  static ma_participants & instance()
    { static ma_participants pt; return pt; }

  // add a new group
  void add_group( std::string const & group );

  // add a new group and fill the group with participants "group-1", "group-2"
  // ... "group-size"
  void add_group( std::string const & group, size_t size );

  // add a new participant to a group
  void add_participant( std::string const & group
                      , std::string const & app );

  // add a new participant to the top level (without a group)
  void add_participant( std::string const & app );

  // get methods
  size_t get_group_participant_count( std::string const & group ) const;
  size_t get_participant_count( ) const;

  // reset method
  void reset( );

private:

  string_set_t ungrouped_apps;
  string_set_t all_apps;
  groups_t     groups;

};



} // end of namespace errorhandler
} // end of namespace novadaq



#endif




