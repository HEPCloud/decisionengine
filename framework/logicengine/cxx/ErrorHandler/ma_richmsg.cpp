#include <ErrorHandler/ma_richmsg.h>
#include <ErrorHandler/ma_rule.h>

using namespace novadaq::errorhandler;

namespace {

  bool parse_msg_ref( string_t const & s
                    , ma_rule  const * rule 
                    , std::vector<cond_arg_t> & symbols )
  {
    size_t pos = s.find('.');

    if( pos==string_t::npos ) return false;  // no .

    cond_idx_t cond_idx = rule->get_cond_idx( s.substr(0, pos) );

    ++pos;

    if( pos==s.size() || s[pos]!='$') return false; // no $

    ++pos;

    if( pos==s.size() || string_t("stmg").find(s[pos])==string_t::npos) return false;

    switch( s[pos] )
    {
      case 's':  // $s, source
      if( pos==s.size()-1 )
      {
        symbols.push_back( cond_arg_t(cond_idx, SOURCE) );
        return true;
      }
      return false;
                                        
      case 't': // $t, target
      if( pos==s.size()-1 )
      {
        symbols.push_back( cond_arg_t(cond_idx, TARGET) );
        return true;
      }
      return false;

      case 'm': // $m, message
      if( pos==s.size()-1 )
      {
        symbols.push_back( cond_arg_t(cond_idx, MESSAGE) );
        return true;
      }
      return false;

      case 'g': // $gn, group-n
      if( pos==s.size()-2 && s[pos+1]>='1' && s[pos+1]<='9' )
      {
        symbols.push_back( cond_arg_t( cond_idx, (arg_t)(GROUP1+s[pos+1]-'1') ) );
        return true;
      }
      return false;

      default:
        return false;

    }
  }

  bool parse_msg( string_t const & s
                , ma_rule  const * rule
                , string_t & stripped_msg
                , std::vector<size_t> & insert_pos
                , std::vector<cond_arg_t> & symbols )
  {
    size_t old = 0;
    size_t pos = s.find("${");
    size_t ins = 0;

    while( pos!=string_t::npos )
    {
      ins += (pos-old);
      insert_pos.push_back(ins);
      stripped_msg.append(s, old, pos-old);

      size_t close = s.find('}', pos);

      if( close == string_t::npos )
        return false; // no close '}'

      if ( !parse_msg_ref( s.substr(pos+2, close-pos-2), rule, symbols ) )
        return false;

      old = close+1;
      pos = s.find("${", old);
    }

    if( old<s.size() )
      stripped_msg.append(s.substr(old));

    return true;
  }

} // end of anonymous namespace

ma_richmsg::ma_richmsg( )
: rule(NULL)
, plain_msg()
, stripped_msg()
, insert_pos()
, symbols()
{

}

ma_richmsg::ma_richmsg( string_t const & s, ma_rule const * parent )
: rule(NULL)
, plain_msg()
, stripped_msg()
, insert_pos()
, symbols()
{
  init(parent, s);
}

void ma_richmsg::init( ma_rule const * parent, string_t const & s )
{
  rule = parent;
  plain_msg = s;

  if( !parse_msg(plain_msg, rule, stripped_msg, insert_pos, symbols) )
    throw std::runtime_error("Error parsing rule messages!");
}

const string_t & ma_richmsg::plain_message() const
{
  return plain_msg;
}

string_t ma_richmsg::message() const
{
  string_t result = stripped_msg;
  ma_domain const & alarm = rule->get_alarm();
          
  for(int i=symbols.size()-1; i>=0; --i)
  {
    ma_condition * cond_ptr = symbols[i].first.first;
    size_t         cond_idx = symbols[i].first.second;
    arg_t          cond_arg = symbols[i].second;
                                
    result.insert( insert_pos[i]
                 , cond_ptr->get_arg(alarm[cond_idx], cond_arg));
  }

  return result;
}

