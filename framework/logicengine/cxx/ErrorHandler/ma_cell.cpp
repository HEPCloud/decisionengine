#include <ErrorHandler/ma_cell.h>
#include <ErrorHandler/Fact.h>

#include <time.h>

using namespace novadaq::errorhandler;

bool
ma_cell::hit(bool val)
{
  // undefined, always considered as flipped
  if (!defined) {
    defined = true;
    on = val;
    return true;
  }

  // already defined, no change in status
  if (val == on) { return false; }

  // changed
  on = val;
  return true;
}

void
ma_cell::reset()
{
  on = false;
  defined = false;
  msgs.clear();
}
