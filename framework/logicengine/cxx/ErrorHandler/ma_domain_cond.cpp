
#include <ErrorHandler/ma_domain_ops.h>
#include <ErrorHandler/ma_domain_cond.h>
#include <ErrorHandler/ma_domain_expr.h>
#include <ErrorHandler/ma_rule.h>


using namespace novadaq::errorhandler;

ma_domain_cond::ma_domain_cond( )
: cond_type (COND)
, conds ()
, str_cond ()
, cond_size (0)
, expr ()
{

}

void ma_domain_cond::insert_expr( ma_domain_expr const & d_expr )
{
  expr.reset(new ma_domain_expr(d_expr));
  cond_type = EXPR;
}

void ma_domain_cond::evaluate(ma_domains & domains) const
{

  ma_domains worksheet;

  // 1. '(' >> expr >> ')'

  if (cond_type == EXPR)
  {
    if (expr.get() == NULL) 
      throw std::runtime_error("expr not exist");

    expr->evaluate(worksheet);
  }

  // 2. cond_1.$ = cond_2.$ = ... = 'string literal'

  else if (!str_cond.empty())
  {
    // # of conds must be not empty
    if (conds.empty())
      throw std::runtime_error("cond_arg_list cannot be empty");

    // init with (*,*) to all condition domains
    ma_domain domain = ma_domain_ctor_any(cond_size);

    // whether to keep the domain
    bool keep = true;

    // iterate
    cond_arg_list_t::const_iterator it = conds.begin();
    while(it!=conds.end())
    {
      ma_condition * c_ptr = it->first.first;
      size_t         c_idx = it->first.second;
      arg_t          c_arg = it->second;

      int idx = c_ptr->find_arg(str_cond, c_arg);

      if (idx==D_NIL) { keep = false; break; }
      else   domain[c_idx] = ma_cond_domain_ctor(idx, c_arg);

      ++it;
    }

    // push the domain if not flagged
    if (keep) worksheet.push_back(domain);
  }

  // 3. cond_1.$ = cond_2.$ = ... 

  else
  {
    // # of conds must be 1 or greater
    if (conds.empty())
      throw std::runtime_error("no cond in cond list of ma_domain_cond");

    // first condition in the list
    ma_condition * c1_ptr = conds.front().first.first;
    int            c1_idx = conds.front().first.second;
    arg_t     c1_arg_type = conds.front().second;

    // get the src/target list
    idx_t const & c1_args = c1_ptr->get_args(c1_arg_type);

    // loop through the arg list
    idx_t::const_iterator it = c1_args.begin();
    for ( ; it!=c1_args.end(); ++it)
    {
      // init everyone with (*,*)
      ma_domain domain = ma_domain_ctor_any(cond_size);
  
      // whether to keep this domain or not
      bool keep = true;

      // get the actual src/target string and index
      string_t const & c1_arg_str = it->first;
      size_t           c1_arg_idx = it->second;

      // domain[c1_idx] = domain[c1_idx] n (c1_arg_idx, *)
      domain_intersect( domain[c1_idx]
                      , ma_cond_domain_ctor(c1_arg_idx, c1_arg_type) );

      // iterate through the remaining conds
      cond_arg_list_t::const_iterator cond_it = conds.begin();

      while( ++cond_it!=conds.end() ) 
      {
        // idx of current cond and its arg type (source/target)
        ma_condition * c_ptr = cond_it->first.first;
        size_t         c_idx = cond_it->first.second;
        arg_t     c_arg_type = cond_it->second;

        // find arg_str_c1 from current cond
        int c_arg_idx = c_ptr->find_arg(c1_arg_str, c_arg_type);

        // cannot find arg_str in the current cond. go for next arg_str
        if (c_arg_idx == D_NIL) 
        {
          keep = false;
          break;
        }

        // domain[idx_c] = domain[idx_c] n (arg_idx_c, *)
        domain_intersect( domain[c_idx]
                        , ma_cond_domain_ctor(c_arg_idx, c_arg_type) );

        // stop if domain[idx_c] is null, go for next arg_str
        if (domain_is_null(domain[c_idx]))
        {
          keep = false;
          break;
        }
      } 

      // push the domain to the worksheet 
      if (keep) worksheet.push_back(domain);
    }
  }

  // combine the domain list from the worksheet, and the list passed
  // in from above levels

  and_merge(domains, worksheet);

}

ma_domains & 
  ma_domain_cond::and_merge( ma_domains & domains
                           , ma_domains & worksheet ) const
{
  if (domains.empty())
  {
    domains.splice(domains.end(), worksheet);
    return domains;
  }

  // null worksheet will null everything in the domains
  if (worksheet.empty())
  {
    domains.clear();
    return domains;
  }

  // first expand the domains to the size of 
  // N_domains * N_worksheet
  size_t nw = worksheet.size();
  ma_domains::iterator dit = domains.begin();
  for ( ; dit!=domains.end(); ++dit)
    domains.insert(dit, nw-1, *dit);

  // domain intersect operation
  dit = domains.begin();
  ma_domains::iterator wit = worksheet.begin();
  for ( ; dit!=domains.end(); ++dit,++wit)
  {
    if ( wit==worksheet.end() )  wit = worksheet.begin();

    domain_intersect(*dit, *wit);
  }

  // remove null domains
  domains.remove(ma_domain_ctor_null());

  return domains;
}








