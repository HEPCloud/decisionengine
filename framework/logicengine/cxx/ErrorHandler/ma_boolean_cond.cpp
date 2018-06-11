
#include <ErrorHandler/ma_boolean_cond.h>
#include <ErrorHandler/ma_boolean_expr.h>

using namespace novadaq::errorhandler;

template <typename T>
bool
  compare(compare_op_t op, T v, T rhv)
{
  switch(op)
  {
  case CO_L:  return (v <  rhv);
  case CO_LE: return (v <= rhv);
  case CO_E:  return (v == rhv);
  case CO_NE: return (v != rhv);
  case CO_GE: return (v >= rhv);
  case CO_G:  return (v >  rhv);
  default:    return false;
  }
}

typedef std::vector<boost::any> anys_t;

void ma_boolean_cond::insert_ext_func( cond_idx_t ci
                                     , arg_t      arg
                                     , anys_t   const & func_args
                                     , string_t const & function )
{ 
  cond_arg.first = ci; 
  cond_arg.second = arg; 
  cond_type = FUNCTION; 
  ext_func.reset( ma_function_factory::create_instance(function) ); 

  if( !ext_func->parse_arguments( func_args ) )
    throw std::runtime_error("arguments rejected by " + function );
}

void ma_boolean_cond::reset( )
{
  neg_cond = false;

  if( cond_type == EXPR )
  {
    // expression must not be null
    assert( expr.get() != NULL );
    return expr->reset();
  }
  
  if( cond_type == COND )
  {
    return;
  }

  if( cond_type >= FUNCTION )
  {
    cond_idx_t cond_idx = cond_arg.first;

    // condition ptr must not be null
    assert( cond_idx.first != NULL );

    // custom function must not be null 
    assert( ext_func.get() != NULL );

    return ext_func->reset();
  }


  throw std::runtime_error("ma_boolean_cond::reset(): unknow cond_type");
}


bool ma_boolean_cond::evaluate( ma_domain & value
                              , ma_domain & alarm
                              , ma_domain const & domain ) const
{
  if( cond_type == EXPR )
  {
    // expression must not be null
    assert( expr.get() != NULL );

    // evaluate from the expr
    bool v = expr->evaluate(value, alarm, domain);
    return neg_cond ? (!v) : (v);
  }

  if( cond_type == COND )
  {
    cond_idx_t cond_idx = cond_arg.first;

    // condition ptr must not be null
    assert( cond_idx.first != NULL );

    // update alarm
    if( domain_is_null(alarm[cond_idx.second]) )
      alarm[cond_idx.second] = value[cond_idx.second];

    // get status from hitmap of the condition
    bool v = cond_idx.first->get_status(value[cond_idx.second]);
    return neg_cond ? (!v) : (v);
  }

  if( cond_type >= FUNCTION )
  {
    cond_idx_t cond_idx = cond_arg.first;

    // condition ptr must not be null
    assert( cond_idx.first != NULL );

    // custom function must not be null 
    assert( ext_func.get() != NULL );

    // update alarm
    if( ext_func->grouped_alarm() )
    {
      alarm[cond_idx.second] = domain[cond_idx.second];
    }
    else
    {
      alarm[cond_idx.second] = 
        ma_cond_domain( cond_idx.first->find_source( cond_idx.first->get_msg_source() )
                      , cond_idx.first->find_target( cond_idx.first->get_msg_target() ) );
    }

    // evaluate
    boost::any v = ext_func->evaluate( *(cond_idx.first)
                                     , domain[cond_idx.second] );
    double     d;
    bool       b;
    string_t   s;

    switch( cond_type )
    {
    case FUNCTION: 
      b = boost::any_cast<bool>(v);
      return b;

    case FUNCTION_BOOL:
      b = boost::any_cast<bool>(v);
      return compare( op, b, rhv_b );

    case FUNCTION_STRING:
      s = boost::any_cast<string_t>(v);
      return compare( op, s, rhv_s );

    case FUNCTION_DOUBLE:
      if( v.type() == typeid(int) ) d = boost::any_cast<int>(v);
      else                          d = boost::any_cast<double>(v);
      return compare( op, d, rhv_d );

    default: break;
    }
  }

  throw std::runtime_error("ma_boolean_cond::evaluate(): unknow cond_type");
}

void ma_boolean_cond::insert_expr( ma_boolean_expr const & b_expr )
{
  expr.reset(new ma_boolean_expr(b_expr));
  cond_type = EXPR;
  neg_cond = false;
}

void ma_boolean_cond::insert_expr_neg( ma_boolean_expr const & b_expr )
{
  expr.reset(new ma_boolean_expr(b_expr));
  cond_type = EXPR;
  neg_cond = true;
}
