
#include <ErrorHandler/ma_parse.h>

#include <ErrorHandler/ma_types.h>

#include <ErrorHandler/ma_boolean_expr.h>
#include <ErrorHandler/ma_boolean_andexpr.h>
#include <ErrorHandler/ma_boolean_cond.h>

#include <ErrorHandler/ma_domain_expr.h>
#include <ErrorHandler/ma_domain_andexpr.h>
#include <ErrorHandler/ma_domain_cond.h>

#include <ErrorHandler/ma_cond_test_expr.h>
#include <ErrorHandler/ma_cond_test_andexpr.h>
#include <ErrorHandler/ma_cond_test_primary.h>

#include <ErrorHandler/ma_rule.h>

#include <boost/any.hpp>
#include <boost/spirit/include/qi.hpp>
#include <boost/spirit/include/phoenix_bind.hpp>
#include <boost/spirit/include/phoenix_core.hpp>
#include <boost/spirit/include/phoenix_operator.hpp>


namespace ascii = ::boost::spirit::ascii;
namespace phx   = ::boost::phoenix;
namespace qi    = ::boost::spirit::qi;
namespace ql    = ::boost::spirit::qi::labels;

using ascii::char_;
using ascii::no_case;
using ascii::digit;
using ascii::graph;
using ascii::space;

using phx::ref;
//using phx::bind;

using qi::eol;
using qi::lexeme;
using qi::lit;
using qi::bool_;
using qi::int_;
using qi::double_;
using qi::no_skip;
using qi::raw;
using qi::skip;
using qi::locals;

//using namespace qi::labels;

using novadaq::errorhandler::ma_rule;
using novadaq::errorhandler::ma_condition;
using novadaq::errorhandler::ma_boolean_expr;
using novadaq::errorhandler::ma_boolean_andexpr;
using novadaq::errorhandler::ma_boolean_cond;
using novadaq::errorhandler::ma_domain_expr;
using novadaq::errorhandler::ma_domain_andexpr;
using novadaq::errorhandler::ma_domain_cond;
using novadaq::errorhandler::ma_cond_test_expr;
using novadaq::errorhandler::ma_cond_test_andexpr;
using novadaq::errorhandler::ma_cond_test_primary;
using novadaq::errorhandler::cond_idx_t;
using novadaq::errorhandler::cond_arg_t;
using novadaq::errorhandler::compare_op_t;
using novadaq::errorhandler::string_t;
using novadaq::errorhandler::SOURCE;
using novadaq::errorhandler::TARGET;
using novadaq::errorhandler::NONE;
using novadaq::errorhandler::CO_LE;
using novadaq::errorhandler::CO_GE;
using novadaq::errorhandler::CO_NE;
using novadaq::errorhandler::CO_E;
using novadaq::errorhandler::CO_L;
using novadaq::errorhandler::CO_G;



// ------------------------------------------------------------------

namespace novadaq
{
  namespace errorhandler 
  {
    template< class FwdIter, class Skip>
      struct domain_expr_parser;

    template< class FwdIter, class Skip>
      struct boolean_expr_parser;

    template< class FwdIter, class Skip>
      struct cond_test_expr_parser;

    class ma_rule;
  }
}


// ------------------------------------------------------------------

static void 
  insert_domain_andexpr( ma_domain_expr & expr
                       , ma_domain_andexpr const & andexpr )
{
  expr.insert_andexpr(andexpr);
}

static void 
  insert_domain_cond( ma_domain_andexpr & andexpr
                    , ma_domain_cond const & cond )
{
  andexpr.insert_cond(cond);
}

static void
  insert_domain_expr( ma_domain_cond & cond
                    , ma_domain_expr const & expr )
{
  cond.insert_expr(expr);
}

static void
  insert_cond_arg( ma_domain_cond & cond
                 , string_t const & name
                 , char arg
                 , ma_rule * rule )
{
  // update condition's notification list
  rule->update_notify_list( name
                          , (arg=='s') ? SOURCE : TARGET );

  // push the condition ptr into domain_cond
  cond.insert_cond_arg    ( rule->get_cond_idx(name)
                          , (arg=='s') ? SOURCE : TARGET 
                          , rule->get_cond_size() );
}

static void
  insert_str_cond( ma_domain_cond & cond, string_t const & str )
{
  cond.insert_str_cond( str );
}


// ------------------------------------------------------------------

template< class FwdIter, class Skip >
  struct novadaq::errorhandler::domain_expr_parser 
: qi::grammar<FwdIter, ma_domain_expr(), Skip>
{

  // default c'tor
  domain_expr_parser( ma_rule * rule );

  // data member
  qi::rule<FwdIter, ma_domain_expr(),    Skip> domain_expr;
  qi::rule<FwdIter, ma_domain_andexpr(), Skip> domain_andexpr;
  qi::rule<FwdIter, ma_domain_cond(), locals<string_t>, Skip> domain_cond;

  qi::rule<FwdIter, string_t(), Skip> key;
  qi::rule<FwdIter, string_t(), Skip> keywords;
  qi::rule<FwdIter, string_t(), Skip> str;

};


// ------------------------------------------------------------------

template< class FwdIter, class Skip >
  novadaq::errorhandler::domain_expr_parser<FwdIter, Skip>
                       ::domain_expr_parser(ma_rule * rule)
: domain_expr_parser::base_type( domain_expr )
{
  domain_expr = 
       domain_andexpr [phx::bind(&insert_domain_andexpr, ql::_val, ql::_1)] 
     % "OR"
  ;

  domain_andexpr = 
       domain_cond    [phx::bind(&insert_domain_cond, ql::_val, ql::_1)]    
     % "AND"
  ;

  domain_cond = 
          (
               lit('(') 
            >> domain_expr [phx::bind(&insert_domain_expr, ql::_val, ql::_1)] 
            >> lit(')') 
          ) // '(' >> expr >> ')'
        |
          (
            (
              (
                   key         [ql::_a = ql::_1]
                >> ".$" 
                >> char_("st") 
                      [phx::bind(&insert_cond_arg, ql::_val, ql::_a, ql::_1, rule)]
              ) % '='
            ) >> -( '=' >> (    str [phx::bind(&insert_str_cond, ql::_val, ql::_1)] 
                             | "ANY"
                           )
                  )
          ) // cond1.$x = cond2.$y = ... -( = "str_cond" )
            // cond1.$x = cond2.$y = ... -( = ANY )
  ;

  keywords =  no_case["AND"]
            | no_case["OR"]
            | no_case["ANY"]
  ;

  key =   qi::lexeme[char_("a-zA-Z_") >> *char_("a-zA-Z_0-9")]
        - keywords;
  ;

  str = qi::lexeme['\'' >> +(ascii::char_ - '\'') >> '\''];
}


// ------------------------------------------------------------------

static void
  insert_boolean_andexpr( ma_boolean_expr & expr
                        , ma_boolean_andexpr const & andexpr )
{
  expr.insert(andexpr);
}

static void
  insert_boolean_cond( ma_boolean_andexpr & andexpr
                     , ma_boolean_cond const & cond )
{
  andexpr.insert(cond);
}

static void
  insert_boolean_expr( ma_boolean_cond & cond  
                     , ma_boolean_expr const & expr )
{
  cond.insert_expr(expr);
}

static void
  insert_boolean_expr_neg( ma_boolean_cond & cond  
                     , ma_boolean_expr const & expr )
{
  cond.insert_expr_neg(expr);
}

static void 
  insert_primitive_cond( ma_boolean_cond & cond
                       , string_t const & name
                       , ma_rule * rule )
{
  // 1. first insert the condition ptr to the corresponding rule
  //    such that the condition has an index in the rule
  //    NOTE* that the insertion of condition ptr only happens when
  //          parsing the boolean expression
  // 2. then insert the (ptr, idx) pair to the boolean_cond
  cond.insert_cond( rule->insert_condition_ptr( name, true ) );
}

static void 
  insert_primitive_cond_neg( ma_boolean_cond & cond
                       , string_t const & name
                       , ma_rule * rule )
{
  // 1. first insert the condition ptr to the corresponding rule
  //    such that the condition has an index in the rule
  //    NOTE* that the insertion of condition ptr only happens when
  //          parsing the boolean expression
  // 2. then insert the (ptr, idx) pair to the boolean_cond
  cond.insert_cond_neg( rule->insert_condition_ptr( name, true ) );
}


static void
  insert_ext_func( ma_boolean_cond & cond
                 , string_t const  & function
                 , string_t const  & name
                 , char              cond_arg
                 , std::vector<boost::any> const & func_args
                 , ma_rule * rule )
{
  cond.insert_ext_func( rule->insert_condition_ptr( name, false /*non-primitive*/ )
                      , (cond_arg=='s') ? SOURCE : ((cond_arg=='t') ? TARGET : NONE)
                      , func_args
                      , function );
}

static void
  insert_compare_op_double( ma_boolean_cond & cond
                          , compare_op_t op
                          , double rhv )
{
  cond.insert_compare_op_double( op, rhv );
}

static void
  insert_compare_op_bool  ( ma_boolean_cond & cond
                          , compare_op_t op
                          , bool rhv )
{
  if( (op != CO_E) && (op != CO_NE) )
    throw std::runtime_error("error in parsing rule: booleans can only use == or !=");

  cond.insert_compare_op_bool( op, rhv );
}

static void
  insert_compare_op_string( ma_boolean_cond & cond
                          , compare_op_t op
                          , string_t rhv )
{
  cond.insert_compare_op_string( op, rhv );
}

// ------------------------------------------------------------------

using boost::any;
typedef std::vector<any> anys;

template< class FwdIter, class Skip >
  struct novadaq::errorhandler::boolean_expr_parser 
: qi::grammar<FwdIter, ma_boolean_expr(), Skip>
{

  // default c'tor
  boolean_expr_parser( ma_rule * rule );

  // data member
  qi::rule<FwdIter, ma_boolean_expr(),    Skip> boolean_expr;
  qi::rule<FwdIter, ma_boolean_andexpr(), Skip> boolean_andexpr;
  qi::rule<FwdIter, ma_boolean_cond()
                  , locals<string_t, char, compare_op_t, string_t, anys>
                  , Skip>                       boolean_cond;

  qi::rule<FwdIter, string_t(),           Skip> key;
  qi::rule<FwdIter, string_t(),           Skip> str;
  qi::rule<FwdIter, string_t(),           Skip> keywords;
  qi::rule<FwdIter, compare_op_t(),       Skip> compare_op;

  qi::rule<FwdIter, any(),                Skip> arg;
  qi::rule<FwdIter, anys(),               Skip> args;

};


// ------------------------------------------------------------------

template< class FwdIter, class Skip >
  novadaq::errorhandler::boolean_expr_parser<FwdIter, Skip>
                       ::boolean_expr_parser( ma_rule * rule )
: boolean_expr_parser::base_type( boolean_expr )
{
  boolean_expr = 
        boolean_andexpr [phx::bind(&insert_boolean_andexpr, ql::_val, ql::_1)] 
      % "||"
  ;

  boolean_andexpr = 
        boolean_cond [phx::bind(&insert_boolean_cond, ql::_val, ql::_1)] 
      % "&&"
  ;

  boolean_cond = 
         (    lit('(') 
           >> boolean_expr [phx::bind(&insert_boolean_expr,ql::_val,ql::_1)] 
           >> ')' 
         )  // '(' >> expr >> ')'
       |
         (    lit('!') >> lit('(') 
           >> boolean_expr [phx::bind(&insert_boolean_expr_neg,ql::_val,ql::_1)] 
           >> ')' 
         )  // '! (' >> expr >> ')'
       | 
         (
              key                                [ ql::_a = ql::_1 ]
           >> lit('(') >> key                    [ ql::_d = ql::_1 ]
                       >> -( ".$" >> char_("st") [ ql::_b = ql::_1 ] )
                       >> -( ','  >> args        [ ql::_e = ql::_1 ] )
           >> lit(')')  [ phx::bind( &insert_ext_func
                        , ql::_val, ql::_a, ql::_d, ql::_b, ql::_e, rule ) ]

           >> -(    compare_op                   [ ql::_c = ql::_1 ]
                 >> (   
                        double_ [ phx::bind( &insert_compare_op_double
                                           , ql::_val, ql::_c, ql::_1 ) ]
                      | bool_   [ phx::bind( &insert_compare_op_bool
                                           , ql::_val, ql::_c, ql::_1 ) ]
                      | str     [ phx::bind( &insert_compare_op_string
                                           , ql::_val, ql::_c, ql::_1 ) ]
                    ) 
               )
         )  // custom_function(cond.$st)
       |
         key    [ phx::bind( &insert_primitive_cond, ql::_val, ql::_1, rule) ] 
            // Cond
       | ( lit('!') >> key
                [ phx::bind( &insert_primitive_cond_neg, ql::_val, ql::_1, rule) ]
         )
  ;

  args     = ( arg % ',' )
  ;

  arg      =   double_ [ ql::_val = ql::_1 ]
             | bool_   [ ql::_val = ql::_1 ]
             | str     [ ql::_val = ql::_1 ]
  ;

  keywords =  no_case["AND"]
            | no_case["OR"]
  ;

  key =   qi::lexeme[char_("a-zA-Z_") >> *char_("a-zA-Z_0-9")]
        - keywords
  ;

  str =   qi::lexeme['\'' >> +(char_ - '\'') >> '\'']
  ;

  compare_op =   lit("==") [ ql::_val = CO_E  ] 
               | lit("!=") [ ql::_val = CO_NE ]
               | lit("<=") [ ql::_val = CO_LE ]
               | lit(">=") [ ql::_val = CO_GE ]
               | lit("<" ) [ ql::_val = CO_L  ]
               | lit(">" ) [ ql::_val = CO_G  ]
  ;
}


// ------------------------------------------------------------------

static void
  set_boolean_expr( ma_boolean_expr & expr, ma_rule * rule ) 
{
  rule->set_boolean_expr( expr );
}

static void
  set_domain_expr( ma_domain_expr & expr, ma_rule * rule ) 
{
  rule->set_domain_expr( expr );
}


// ------------------------------------------------------------------

bool
  novadaq::errorhandler::parse_condition_expr ( string_t const & s 
                                              , ma_rule * rule )
{
  typedef string_t::const_iterator iter_t;
  typedef ascii::space_type        ws_t;

  boolean_expr_parser<iter_t, ws_t> boolean_p(rule);
  domain_expr_parser<iter_t, ws_t>  domain_p(rule);

  iter_t           begin = s.begin();
  iter_t const     end   = s.end();

  bool b = qi::phrase_parse
                 ( 
                   begin, end
                 ,    boolean_p [phx::bind(&set_boolean_expr, ql::_1, rule)]
                   >> -( "WHERE" >> domain_p  
                                [phx::bind(&set_domain_expr , ql::_1, rule)]
                       )
                 , space
                 )
         && begin == end;
  
  return b;
}
  

// ------------------------------------------------------------------
//  Condition test expression parser
// ------------------------------------------------------------------

static void
  insert_test_primary( ma_cond_test_andexpr       & andexpr
                     , ma_cond_test_primary const & primary )
{
  andexpr.insert( primary );
}

static void
  insert_test_andexpr( ma_cond_test_expr          & expr
                     , ma_cond_test_andexpr const & andexpr )
{
  expr.insert( andexpr );
}

static void
  insert_test_expr( ma_cond_test_primary          & primary
                  , ma_cond_test_expr       const & expr )
{
  primary.insert_expr( expr );
}

static void
  insert_test_func( ma_cond_test_primary          & primary
                  , string_t                const & function
                  , std::vector<boost::any> const & func_args )
{
  primary.insert_func( function, func_args );
}

static void
  insert_test_compare_op( ma_cond_test_primary    & primary
                        , compare_op_t              op
                        , boost::any        const & rhv )
{
  primary.insert_compare_op( op, rhv );
}


// ------------------------------------------------------------------

template <typename T>
struct strict_real_policies : qi::real_policies<T>
{
    static bool const expect_dot = true;
};


template< class FwdIter, class Skip >
  struct novadaq::errorhandler::cond_test_expr_parser
: qi::grammar<FwdIter, ma_cond_test_expr(), Skip>
{

  // default c'tor
  cond_test_expr_parser( );

  // data member
  qi::rule<FwdIter, ma_cond_test_expr(),    Skip> test_expr;
  qi::rule<FwdIter, ma_cond_test_andexpr(), Skip> test_andexpr;
  qi::rule<FwdIter, ma_cond_test_primary()
                  , locals<string_t, anys_t, compare_op_t>
                                          , Skip> test_primary;

  qi::rule<FwdIter, string_t(),           Skip> key;
  qi::rule<FwdIter, string_t(),           Skip> str;
  qi::rule<FwdIter, string_t(),           Skip> keywords;
  qi::rule<FwdIter, compare_op_t(),       Skip> compare_op;

  qi::rule<FwdIter, any(),                Skip> value;
  qi::rule<FwdIter, anys(),               Skip> values;

  qi::real_parser< double, strict_real_policies<double> > real;
};


// ------------------------------------------------------------------

template< class FwdIter, class Skip >
  novadaq::errorhandler::cond_test_expr_parser<FwdIter, Skip>
                       ::cond_test_expr_parser( )
: cond_test_expr_parser::base_type( test_expr )
{
  test_expr = 
       test_andexpr [phx::bind(&insert_test_andexpr, ql::_val, ql::_1)] 
     % "||"
  ;

  test_andexpr = 
       test_primary [phx::bind(&insert_test_primary, ql::_val, ql::_1)]
     % "&&"
  ;

  test_primary = 
       (
            lit('(') 
         >> test_expr [phx::bind(&insert_test_expr, ql::_val, ql::_1)]
         >> lit(')') 
       )
     | 
       (
            key       [ ql::_a = ql::_1 ]
         >> lit('(') 
         >> - values  [ ql::_b = ql::_1 ]
         >> lit(')')  [ phx::bind(&insert_test_func, ql::_val, ql::_a, ql::_b) ]
         >> -(    compare_op [ ql::_c = ql::_1 ] 
               >> value      [ phx::bind( &insert_test_compare_op
                                        , ql::_val, ql::_c, ql::_1 ) ]
             )
       )
  ;

  values = ( value % ',' )
  ;

  value  =   ( int_  [ ql::_val = ql::_1 ] >> ! char_(".eE") )
           | double_ [ ql::_val = ql::_1 ]
           | bool_   [ ql::_val = ql::_1 ]
           | str     [ ql::_val = ql::_1 ]
  ;

  keywords = no_case["AND"] | no_case["OR"]
  ;

  key      =   qi::lexeme[char_("a-zA-Z_") >> *char_("a-zA-Z_0-9")]
             - keywords
  ;

  str      = qi::lexeme['\'' >> +(char_ - '\'') >> '\'']
  ;
 
  compare_op =   lit("==") [ ql::_val = CO_E  ] 
               | lit("!=") [ ql::_val = CO_NE ]
               | lit("<=") [ ql::_val = CO_LE ]
               | lit(">=") [ ql::_val = CO_GE ]
               | lit("<" ) [ ql::_val = CO_L  ]
               | lit(">" ) [ ql::_val = CO_G  ]
  ;
       
  
} 


// ------------------------------------------------------------------

bool
  novadaq::errorhandler::parse_condition_test ( string_t const & s 
                                              , ma_cond_test_expr & expr )
{
  typedef string_t::const_iterator iter_t;
  typedef ascii::space_type        ws_t;

  if( s.empty() ) return true;

  cond_test_expr_parser<iter_t, ws_t> test_p;

  iter_t           begin = s.begin();
  iter_t const     end   = s.end();

  bool b = qi::phrase_parse ( begin, end , test_p , space , expr )
         && begin == end;
  
  return b;
}







