#ifndef ERROR_HANDLER_MA_HITMAP_H
#define ERROR_HANDLER_MA_HITMAP_H

#include <ErrorHandler/ma_types.h>
#include <ErrorHandler/ma_utils.h>
#include <ErrorHandler/ma_domain_ops.h>
#include <ErrorHandler/ma_cell.h>

#include <string>
#include <vector>
#include <map>

namespace novadaq {
namespace errorhandler {

class ma_condition;

class ma_hitmap
{
public:
  ma_hitmap( );

  void set_parent( ma_condition * parent ) { cond = parent; }

  unsigned int capture( msg_t    const & msg
                      , string_t const & src
                      , string_t const & tgt
                      , boost::smatch const & what );

  unsigned int force( bool val );

  bool event(size_t src, size_t tgt, time_t t);

  const static string_t global_s;
  const static string_t global_t;

  // reset to ground state
  void reset( );

  // return index of the src/tgt string, or -2 if not found
  int find_source(string_t const & src);
  int find_target(string_t const & tgt);

  // get src/tgt string list
  const idx_t & get_sources() const { return src_idx; }
  const idx_t & get_targets() const { return tgt_idx; }

  // get size of src/tgt
  size_t source_size() const { return src_idx.size(); }
  size_t target_size() const { return tgt_idx.size(); }

  // get src/tgt string from idx
  const string_t & get_source( ma_cond_domain v ) const;
  const string_t & get_target( ma_cond_domain v ) const;

  string_t get_message( ma_cond_domain v ) const;
  string_t get_message_group( ma_cond_domain v, size_t g ) const;
   

  // if the cell has been triggered
  bool get_status( ma_cond_domain v ) const;
  bool get_defined( ma_cond_domain v ) const;

  int get_alarm_count( ma_cond_domain v, arg_t arg ) const;

  // get a range of src/target
  void get_cond_range( ma_cond_domain d
                     , ma_cond_range & src
                     , ma_cond_range & tgt ) const;

  // get a view to the hitmap
  const hitmap_view_t
    get_domain_view( ma_cond_domain const & d );


private:
  // increment size when the hitmap is resized
  const static size_t cap_increment;

  idx_t    src_idx;
  idx_t    tgt_idx;

  size_t   src_cap;
  size_t   tgt_cap;

  ma_condition * cond;

  hitmap_t hitmap;
};

} // end of namespace errorhandler
} // end of namespace novadaq

#endif
