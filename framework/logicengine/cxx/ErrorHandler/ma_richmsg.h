#ifndef ERRORHANDLER_MA_RICHMSG_H
#define ERRORHANDLER_MA_RICHMSG_H

#include <ErrorHandler/ma_types.h>

#include <vector>

namespace novadaq {
namespace errorhandler {

class ma_rule;

class ma_richmsg
{
public:

  ma_richmsg( );
  ma_richmsg( string_t const & s, ma_rule const * parent );

  ~ma_richmsg( ) { }

  void init( ma_rule const * parent, string_t const & s );

  const string_t & plain_message() const;
        string_t   message() const;

private:

  ma_rule const * rule;
  string_t plain_msg;
  string_t stripped_msg;

  std::vector<size_t>     insert_pos;
  std::vector<cond_arg_t> symbols;
};

} // end of namespace errorhandler
} // end of namespace novadaq


#endif
