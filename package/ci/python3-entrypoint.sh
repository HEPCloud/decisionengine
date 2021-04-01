#!/bin/bash -xe
CMD=${1:- -m pytest}
LOGFILE=${2:- pytest.log}

id
getent passwd $(whoami)
python3 -m site
echo ''

python3 setup.py bdist_wheel
python3 -m pip install -r requirements/requirements-runtime.txt --user
python3 -m pip install -r requirements/requirements-develop.txt --user

echo''
python3 -m pip list

# make sure the pipe doesn't eat failures
set -o pipefail

export PYTHONPATH=${PWD}/src:${PYTHONPATH}
echo "PYTHONPATH: ${PYTHONPATH}"

# run the python "module/command"
python3 ${CMD} 2>&1 | tee ${LOGFILE}
