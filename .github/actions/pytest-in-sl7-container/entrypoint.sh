#!/bin/bash -x
## cannot use -e as we lose the log that way
cd decisionengine
python3 setup.py bdist_wheel
# cannot use `tee` as it eats $? and we lose success/failure
python3 -m pytest 2>&1 > pytest.log
RC=$?
cat pytest.log
exit ${RC}
