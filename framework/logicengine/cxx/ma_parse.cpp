#include "ma_parse.h"

#include "ma_types.h"

#include "ma_boolean_andexpr.h"
#include "ma_boolean_cond.h"
#include "ma_boolean_expr.h"

#include "Rule.h"

#include <boost/any.hpp>
#include <boost/spirit/include/phoenix_bind.hpp>
#include <boost/spirit/include/phoenix_core.hpp>
#include <boost/spirit/include/phoenix_operator.hpp>
#include <boost/spirit/include/qi.hpp>

namespace ascii = ::boost::spirit::ascii;
namespace phx = ::boost::phoenix;
namespace qi = ::boost::spirit::qi;
namespace ql = ::boost::spirit::qi::labels;

using ascii::char_;
using qi::bool_;
using qi::double_;

using ascii::no_case;
using ascii::space;
using qi::lexeme;
using qi::lit;
using qi::locals;

using logic_engine::CO_E;
using logic_engine::CO_G;
using logic_engine::CO_GE;
using logic_engine::CO_L;
using logic_engine::CO_LE;
using logic_engine::CO_NE;
using logic_engine::compare_op_t;
using logic_engine::Fact;
using logic_engine::fact_map_t;
using logic_engine::ma_boolean_andexpr;
using logic_engine::ma_boolean_cond;
using logic_engine::ma_boolean_expr;
using logic_engine::Rule;
using logic_engine::string_t;

// ------------------------------------------------------------------

namespace logic_engine {
  struct boolean_expr_parser;
}

// ------------------------------------------------------------------

static void
insert_boolean_andexpr(ma_boolean_expr& expr, ma_boolean_andexpr const& andexpr)
{
  expr.insert(andexpr);
}

static void
insert_boolean_cond(ma_boolean_andexpr& andexpr, ma_boolean_cond const& cond)
{
  andexpr.insert(cond);
}

static void
insert_boolean_expr(ma_boolean_cond& cond, ma_boolean_expr const& expr)
{
  cond.insert_expr(expr);
}

static void
insert_boolean_expr_neg(ma_boolean_cond& cond, ma_boolean_expr const& expr)
{
  cond.insert_expr_neg(expr);
}

static void
insert_primitive_cond(ma_boolean_cond& cond,
                      string_t const& name,
                      fact_map_t& fact_map,
                      Rule* rule)
{
  // 1. first insert the condition ptr to the corresponding rule
  //    such that the condition has an index in the rule
  //    NOTE* that the insertion of condition ptr only happens when
  //          parsing the boolean expression
  // 2. then insert the (ptr, idx) pair to the boolean_cond
  auto fact = rule->insert_fact_ptr(name, fact_map);
  cond.insert(fact);
}

static void
insert_primitive_cond_neg(ma_boolean_cond& cond,
                          string_t const& name,
                          fact_map_t& fact_map,
                          Rule* rule)
{
  // 1. first insert the condition ptr to the corresponding rule
  //    such that the condition has an index in the rule
  //    NOTE* that the insertion of condition ptr only happens when
  //          parsing the boolean expression
  // 2. then insert the (ptr, idx) pair to the boolean_cond
  auto fact = rule->insert_fact_ptr(name, fact_map);
  cond.insert_neg(fact);
}

// ------------------------------------------------------------------

using boost::any;
typedef std::vector<any> anys;
typedef string_t::const_iterator iter_t;
typedef ascii::space_type ws_t;

struct logic_engine::boolean_expr_parser
  : qi::grammar<iter_t, ma_boolean_expr(), ws_t> {

  // default c'tor
  boolean_expr_parser(fact_map_t& fact_map, Rule* rule);

  // data member
  qi::rule<iter_t, ma_boolean_expr(), ws_t> boolean_expr;
  qi::rule<iter_t, ma_boolean_andexpr(), ws_t> boolean_andexpr;
  qi::rule<iter_t,
           ma_boolean_cond(),
           locals<string_t, char, compare_op_t, string_t, anys>,
           ws_t>
    boolean_cond;

  qi::rule<iter_t, string_t(), ws_t> key;
  qi::rule<iter_t, string_t(), ws_t> str;
  qi::rule<iter_t, string_t(), ws_t> keywords;
  qi::rule<iter_t, compare_op_t(), ws_t> compare_op;

  qi::rule<iter_t, any(), ws_t> arg;
  qi::rule<iter_t, anys(), ws_t> args;
};

// ------------------------------------------------------------------

logic_engine::boolean_expr_parser::boolean_expr_parser(fact_map_t& fact_map,
                                                       Rule* rule)
  : boolean_expr_parser::base_type(boolean_expr)
{
  boolean_expr =
    boolean_andexpr[phx::bind(&insert_boolean_andexpr, ql::_val, ql::_1)] %
    "||";

  boolean_andexpr =
    boolean_cond[phx::bind(&insert_boolean_cond, ql::_val, ql::_1)] % "&&";

  boolean_cond =
    (lit('(') >>
     boolean_expr[phx::bind(&insert_boolean_expr, ql::_val, ql::_1)] >>
     ')') // '(' >> expr >> ')'
    | (lit('!') >> lit('(') >>
       boolean_expr[phx::bind(&insert_boolean_expr_neg, ql::_val, ql::_1)] >>
       ')') // '! (' >> expr >> ')'
    | key[phx::bind(
        &insert_primitive_cond, ql::_val, ql::_1, phx::ref(fact_map), rule)]
    // Cond
    | (lit('!') >> key[phx::bind(&insert_primitive_cond_neg,
                                 ql::_val,
                                 ql::_1,
                                 phx::ref(fact_map),
                                 rule)]);

  args = (arg % ',');

  arg = double_[ql::_val = ql::_1] | bool_[ql::_val = ql::_1] |
        str[ql::_val = ql::_1];

  keywords = no_case["AND"] | no_case["OR"];

  key = qi::lexeme[char_("a-zA-Z_") >> *char_("a-zA-Z_0-9")] - keywords;

  str = qi::lexeme['\'' >> +(char_ - '\'') >> '\''];

  compare_op = lit("==")[ql::_val = CO_E] | lit("!=")[ql::_val = CO_NE] |
               lit("<=")[ql::_val = CO_LE] | lit(">=")[ql::_val = CO_GE] |
               lit("<")[ql::_val = CO_L] | lit(">")[ql::_val = CO_G];
}

// ------------------------------------------------------------------

static void
set_boolean_expr(ma_boolean_expr& expr, Rule* rule)
{
  rule->set_boolean_expr(expr);
}

// ------------------------------------------------------------------

bool
logic_engine::parse_fact_expr(string_t const& s,
                              fact_map_t& fact_map,
                              Rule* rule)
{
  boolean_expr_parser boolean_p(fact_map, rule);

  iter_t begin = s.begin();
  iter_t const end = s.end();

  return qi::phrase_parse(begin,
                          end,
                          boolean_p[phx::bind(&set_boolean_expr, ql::_1, rule)],
                          space) &&
         begin == end;
}
