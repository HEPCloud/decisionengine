#!/bin/bash -xe

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

CMD=${1:- -m pytest}
LOGFILE=${2:- pytest.log}

# this trap shouldn't eat the exit code of python
function stop_redis {
    /usr/libexec/redis-shutdown
}
trap stop_redis EXIT

id
getent passwd $(whoami)
echo ''

# Start redis in the background, stop server via traps
/usr/bin/redis-server &
sleep 1
echo ''

# Useful info
python3 -m site
echo ''

python3 setup.py bdist_wheel
python3 -m pip install -e . --user
python3 -m pip install -e .[develop] --user

echo''
python3 -m pip list

# make sure the pipe doesn't eat failures
set -o pipefail

export PYTHONPATH=${PWD}/src:${PYTHONPATH}
echo "PYTHONPATH: ${PYTHONPATH}"

# PROMETHEUS_MULTIPROC_DIR is set in the framework Dockerfile
# but this is causing test_check_metrics_env_var_unset to fail
# so we unset this variable
unset PROMETHEUS_MULTIPROC_DIR

# run the python "module/command"
python3 ${CMD} 2>&1 | tee ${LOGFILE}
