
#include <ErrorHandler/ma_hitmap.h>
#include <ErrorHandler/ma_condition.h>

using namespace novadaq::errorhandler;

const string_t ma_hitmap::global_s = "__S_GLOBAL__";
const string_t ma_hitmap::global_t = "__T_GLOBAL__";

const size_t ma_hitmap::cap_increment = 20;

ma_hitmap::ma_hitmap( )
: src_idx ( )
, tgt_idx ( )
, src_cap ( 20 )
, tgt_cap ( 20 )
, cond ( 0 )
, hitmap  ( boost::extents[src_cap][tgt_cap] )
{

}

void
  ma_hitmap::reset( )
{
  src_idx.clear();
  tgt_idx.clear();

  for( size_t s=0; s<src_cap; ++s )
    for( size_t t=0; t<tgt_cap; ++t )
      hitmap[s][t].reset();
}

unsigned int 
  ma_hitmap::capture( msg_t    const & msg
                    , string_t const & src
                    , string_t const & tgt
                    , boost::smatch const & what )
{
  size_t s_idx = 0;
  size_t t_idx = 0;

  unsigned int result = 0x00;

  // find source index
  if (!cond->per_source()) 
  {
    if( src_idx.empty() )
    {
      src_idx[global_s] = 0;
      result |= SOURCE_CHANGE;
    }

    s_idx = 0;
  }
  else
  {
    idx_t::const_iterator it = src_idx.find(src);
    if (it == src_idx.end())
    {
      s_idx = src_idx.size();
      src_idx.insert(std::make_pair(src, s_idx));
      result |= SOURCE_CHANGE;
    }
    else
    {
      s_idx = it->second;
    }
  }
   
  // find target index
  if (!cond->per_target()) 
  {
    if( tgt_idx.empty() )
    {
      tgt_idx[global_t] = 0;
      result |= TARGET_CHANGE;
    }

    t_idx = 0;
  }
  else
  {
    idx_t::const_iterator it = tgt_idx.find(tgt);
    if (it == tgt_idx.end())
    {
      t_idx = tgt_idx.size();
      tgt_idx.insert(std::make_pair(tgt, t_idx));
      result |= TARGET_CHANGE;
    }
    else
    {
      t_idx = it->second;
    }
  }

  // resize the array if needed
  bool resize = false;

  if (s_idx >= src_cap) 
  {
    src_cap += cap_increment;
    resize = true;
  }

  if (t_idx >= tgt_cap) 
  {
    tgt_cap += cap_increment;
    resize = true;
  }

  if (resize)
  {
    hitmap.resize(boost::extents[src_cap][tgt_cap]);
  }

  // knock the cell
  return hitmap[s_idx][t_idx].hit(msg, what, *cond, s_idx, t_idx) 
           ? (result | STATUS_CHANGE) : (result) ;
}

unsigned int 
  ma_hitmap::force( bool val )
{
  size_t s_idx = 0;
  size_t t_idx = 0;

  unsigned int result = 0x00;

  // find source index
  if( src_idx.empty() )
  {
    src_idx[global_s] = 0;
    result |= SOURCE_CHANGE;
  }

  s_idx = 0;
  
  // find target index
  if( tgt_idx.empty() )
  {
    tgt_idx[global_t] = 0;
    result |= TARGET_CHANGE;
  }

  t_idx = 0;

  // resize the array if needed
  bool resize = false;

  if (s_idx >= src_cap) 
  {
    src_cap += cap_increment;
    resize = true;
  }

  if (t_idx >= tgt_cap) 
  {
    tgt_cap += cap_increment;
    resize = true;
  }

  if (resize)
  {
    hitmap.resize(boost::extents[src_cap][tgt_cap]);
  }

  // knock the cell
  return hitmap[s_idx][t_idx].hit( val ) 
           ? (result | STATUS_CHANGE) : (result) ;
}

bool
  ma_hitmap::event(size_t src, size_t tgt, time_t t)
{
  return hitmap[src][tgt].event(t, *cond);
}

int 
  ma_hitmap::find_source(string_t const & src)
{
  idx_t::const_iterator it = src_idx.find(src);
  if (it==src_idx.end())  return D_NIL;
  else                    return it->second;
}

int 
  ma_hitmap::find_target(string_t const & tgt)
{
  idx_t::const_iterator it = tgt_idx.find(tgt);
  if (it==tgt_idx.end())  return D_NIL;
  else                    return it->second;
}

// get src/tgt string from idx
const string_t & 
  ma_hitmap::get_source( ma_cond_domain v ) const
{ 
  int idx = v.first;
  assert( !src_idx.empty() );

  if( idx==D_NIL ) throw std::runtime_error("get_source: nil idx");
  if( idx==D_ANY ) return src_idx.begin()->first;

  assert( (unsigned)idx<src_idx.size() );

  for(idx_t::const_iterator it = src_idx.begin(); it!=src_idx.end(); ++it)
    if( (unsigned)idx==it->second ) return it->first;

  throw std::runtime_error("get_source: idx not found");
}

const string_t & 
  ma_hitmap::get_target( ma_cond_domain v ) const
{ 
  int idx = v.second;
  assert( !tgt_idx.empty() );

  if( idx==D_NIL ) throw std::runtime_error("get_target: nil idx");
  if( idx==D_ANY ) return tgt_idx.begin()->first;

  assert( (unsigned)idx<tgt_idx.size() );

  for(idx_t::const_iterator it = tgt_idx.begin(); it!=tgt_idx.end(); ++it)
    if( (unsigned)idx==it->second ) return it->first;

  throw std::runtime_error("get_source: idx not found");
}

string_t 
  ma_hitmap::get_message( ma_cond_domain v ) const
{
  assert( !src_idx.empty() ); 
  assert( !tgt_idx.empty() );

  if( v.first==D_NIL || v.second==D_NIL )
    throw std::runtime_error("get_message: nil idx");

  v.first  = (v.first==D_ANY)  ? 0 : v.first;
  v.second = (v.second==D_ANY) ? 0 : v.second;

  return hitmap[v.first][v.second].get_latest_message();
}
 
string_t 
  ma_hitmap::get_message_group( ma_cond_domain v, size_t g ) const
{
  assert( !src_idx.empty() ); 
  assert( !tgt_idx.empty() );

  if( v.first==D_NIL || v.second==D_NIL )
    throw std::runtime_error("get_message: nil idx");

  v.first  = (v.first==D_ANY)  ? 0 : v.first;
  v.second = (v.second==D_ANY) ? 0 : v.second;

  return hitmap[v.first][v.second].get_message_group(g);
}
    

// if the cell has been triggered
bool 
  ma_hitmap::get_status( ma_cond_domain v ) const
{ 
  bool r = hitmap[v.first][v.second].is_on();

  //std::cout << "hitmap::get_status @ " 
  //              << v.first << ", " << v.second << " = " << r << "\n";
  return r; 
}

bool
  ma_hitmap::get_defined( ma_cond_domain v ) const
{
  bool r = hitmap[v.first][v.second].is_defined();
  return r;
}  

int 
  ma_hitmap::get_alarm_count( ma_cond_domain v, arg_t arg ) const
{
  ma_cond_range src, tgt;
  get_cond_range( v, src, tgt );

  int count = 0;;
  if( arg == NONE )
  {
    for(int s=src.first; s<=src.second; ++s)
      for(int t=tgt.first; t<=tgt.second; ++t)
        count += hitmap[s][t].get_message_count();
  }
  else if( arg == SOURCE )
  {
    for(int s=src.first; s<=src.second; ++s)
      for(int t=tgt.first; t<=tgt.second; ++t)
        if( hitmap[s][t].is_on() ) { ++count; break; }
  }
  else
  {
    for(int t=tgt.first; t<=tgt.second; ++t)
      for(int s=src.first; s<=src.second; ++s)
        if( hitmap[s][t].is_on() ) { ++count; break; }
  }

  return count;
}

// get a range of src/target
void 
  ma_hitmap::get_cond_range( ma_cond_domain d
                           , ma_cond_range & src
                           , ma_cond_range & tgt ) const
{ 
  if ( domain_is_null(d) )
    throw std::runtime_error("get_cond_range: NIL domain"); 

  if (d.first ==D_ANY) src.first = 0, src.second = src_idx.size()-1;
  else                 src.first = d.first,  src.second = d.first;

  if (d.second==D_ANY) tgt.first = 0, tgt.second = tgt_idx.size()-1;
  else                 tgt.first = d.second, tgt.second = d.second;
}


// get a view to the hitmap
const hitmap_view_t
  ma_hitmap::get_domain_view( ma_cond_domain const & d )
{ 
  if (domain_is_null(d))
    throw std::runtime_error("get_domain_view: null domain");

  return hitmap[ boost::indices [d.first ==D_ANY ? range() : range(d.first) ]
                                [d.second==D_ANY ? range() : range(d.second)] ];
}








