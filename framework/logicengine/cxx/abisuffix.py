# CMAKE 3.12 introduces Python_SOABI which can obsolete this snippet
from __future__ import print_function
import sysconfig
if sysconfig.get_config_var('EXT_SUFFIX'):
    print(sysconfig.get_config_var('EXT_SUFFIX'), end='')
else:
    print('.so', end='')
