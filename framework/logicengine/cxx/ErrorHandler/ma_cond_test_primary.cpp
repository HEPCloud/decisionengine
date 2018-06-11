#include <ErrorHandler/ma_cond_test_primary.h>
#include <ErrorHandler/ma_cond_test_expr.h>


using namespace novadaq::errorhandler;

template <typename T>
bool
  compare( compare_op_t op, T v, T rhv )
{
  switch( op )
  {
  case CO_L : return (v <  rhv);
  case CO_LE: return (v <= rhv);
  case CO_E : return (v == rhv);
  case CO_NE: return (v != rhv);
  case CO_GE: return (v >= rhv);
  case CO_G : return (v >  rhv);
  default:    return false;
  }
}


void ma_cond_test_primary::insert_expr( ma_cond_test_expr const & e )
{
  expr.reset( new ma_cond_test_expr(e) );
  cond_type = EXPR;
}

void ma_cond_test_primary::insert_func( string_t     const & name
                                      , anys_t       const & args )
{
  func.reset( ma_test_function_factory::create_instance(name) );

  try
  {
    if( !func->parse_arguments( args ) )
      throw std::runtime_error("arguments rejected by test function " + name);
  } 
  catch (std::exception & e)
  {
    throw std::runtime_error( "arguments rejected by test function " + name
                            + "() with an exception:\n" + e.what() );
  }

  cond_type = FUNCTION;
}


void ma_cond_test_primary::insert_compare_op( compare_op_t cop
                                            , any_t const & v )
{
  op = cop;

  if( v.type() == typeid(bool) )
  {
    rhv_b = boost::any_cast<bool>(v);
    cond_type = FUNCTION_BOOL;
  }
  else if( v.type() == typeid(int) )
  {
    rhv_d = boost::any_cast<int>(v);
    cond_type = FUNCTION_DOUBLE;
  }
  else if( v.type() == typeid(double) )
  {
    rhv_d = boost::any_cast<double>(v);
    cond_type = FUNCTION_DOUBLE;
  }
  else
  {
    rhv_s = boost::any_cast<string_t>(v);
    cond_type = FUNCTION_STRING;
  }
}


bool ma_cond_test_primary::evaluate( ma_condition const * cond ) const
{

  if( cond_type == EXPR )
  {
    assert( expr.get() != NULL );
    return expr->evaluate( cond );
  }
  else
  {
    any_t v = func->evaluate( *cond );

    bool     b;
    double   d;
    string_t s;

    switch( cond_type )
    {
    case FUNCTION:  
      return boost::any_cast<bool>( v );

    case FUNCTION_BOOL:
      b = boost::any_cast<bool>( v );
      return compare( op, b, rhv_b );

    case FUNCTION_STRING:
      s = boost::any_cast<string_t>( v );
      return compare( op, s, rhv_s );

    case FUNCTION_DOUBLE:
      if     ( v.type()==typeid(int)   ) d = boost::any_cast<int         >( v );
      else if( v.type()==typeid(unsigned int) ) 
                                         d = boost::any_cast<unsigned int>( v );
      else if( v.type()==typeid(long)  ) d = boost::any_cast<long        >( v );
      else if( v.type()==typeid(float) ) d = boost::any_cast<float       >( v );
      else                               d = boost::any_cast<double      >( v );

      return compare( op, d, rhv_d );

    default: 
      throw std::runtime_error("Unkonwn test primary type");
    }
  } 

}

