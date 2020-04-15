#ifndef ERROR_HANDLER_MA_HITMAP_H
#define ERROR_HANDLER_MA_HITMAP_H

#include <ErrorHandler/ma_cell.h>
#include <ErrorHandler/ma_domain_ops.h>
#include <ErrorHandler/ma_types.h>

#include <map>
#include <string>
#include <vector>

namespace novadaq {
  namespace errorhandler {

    class Fact;

    class ma_hitmap {
    public:
      ma_hitmap();

      void
      set_parent(Fact* parent)
      {
        cond = parent;
      }

      unsigned int force(bool val);

      const static string_t global_s;
      const static string_t global_t;

      // reset to ground state
      void reset();

      // get size of src/tgt
      size_t
      source_size() const
      {
        return src_idx.size();
      }
      size_t
      target_size() const
      {
        return tgt_idx.size();
      }

      // if the cell has been triggered
      bool get_status(ma_cond_domain v) const;
      bool get_defined() const;

      // get a range of src/target
      void get_cond_range(ma_cond_domain d,
                          ma_cond_range& src,
                          ma_cond_range& tgt) const;

      // get a view to the hitmap
      const hitmap_view_t get_domain_view(ma_cond_domain const& d);

    private:
      idx_t src_idx;
      idx_t tgt_idx;

      Fact* cond;

      hitmap_t hitmap;
    };

  } // end of namespace errorhandler
} // end of namespace novadaq

#endif
