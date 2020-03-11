#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_parse.h>

using namespace novadaq::errorhandler;

Fact::Fact(string_t const& name)
  : description_(name)
  , srcs_str("any")
  , e_srcs()
  , cats_str("any")
  , e_cats()
  , regex_str()
  , e()
  , tc(1)
  , at_least_(true)
  , ts()
  , persistent_(true)
  , hitmap()
  , events(events)
  , src_()
  , tgt_()
  , cat_()
  , bdy_()
  , what_()
  , last_sev_()
  , last_src_()
  , last_tgt_()
  , last_cat_()
  , last_bdy_()
  , last_what_()
  , notify_on_status()
{}

void
Fact::reset()
{
  hitmap.reset();
}

void
Fact::init()
{
  hitmap.set_parent(this);
}

void
Fact::force(bool val, conds_t& status)
{
  // register to hitmap
  unsigned int result = hitmap.force(val);

  // update reaction_start list
  if (result & STATUS_CHANGE) status.push_back(this);
}

bool
Fact::get_defined() const
{
  return hitmap.get_defined();
}
