#include <ErrorHandler/Fact.h>
#include <ErrorHandler/ma_hitmap.h>

using namespace novadaq::errorhandler;

const string_t ma_hitmap::global_s = "__S_GLOBAL__";
const string_t ma_hitmap::global_t = "__T_GLOBAL__";

ma_hitmap::ma_hitmap()
  : src_idx(), tgt_idx(), cond(0), hitmap(boost::extents[1][1])
{}

void
ma_hitmap::reset()
{
  src_idx.clear();
  tgt_idx.clear();

  hitmap[0][0].reset();
}

unsigned int
ma_hitmap::force(bool val)
{
  // find source index
  src_idx[global_s] = 0;
  tgt_idx[global_t] = 0;

  // knock the cell
  return hitmap[0][0].hit(val) ? STATUS_CHANGE : 0;
}

// if the cell has been triggered
bool
ma_hitmap::get_status(ma_cond_domain v) const
{
  return hitmap[0][0].is_on();
}

bool
ma_hitmap::get_defined() const
{
  return hitmap[0][0].is_defined();
}

// get a range of src/target
void
ma_hitmap::get_cond_range(ma_cond_domain d,
                          ma_cond_range& src,
                          ma_cond_range& tgt) const
{
  if (domain_is_null(d)) throw std::runtime_error("get_cond_range: NIL domain");

  if (d.first == D_ANY)
    src.first = 0, src.second = src_idx.size() - 1;
  else
    src.first = d.first, src.second = d.first;

  if (d.second == D_ANY)
    tgt.first = 0, tgt.second = tgt_idx.size() - 1;
  else
    tgt.first = d.second, tgt.second = d.second;
}

// get a view to the hitmap
const hitmap_view_t
ma_hitmap::get_domain_view(ma_cond_domain const& d)
{
  if (domain_is_null(d))
    throw std::runtime_error("get_domain_view: null domain");

  return hitmap[boost::indices[d.first == D_ANY ? range() : range(d.first)]
                              [d.second == D_ANY ? range() : range(d.second)]];
}
