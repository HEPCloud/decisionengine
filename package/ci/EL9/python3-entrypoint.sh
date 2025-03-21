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

python3 -m venv ~/de_venv
source ~/de_venv/bin/activate
python3 -m pip install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=~/de_venv/bin/python3
source ~/de_venv/bin/virtualenvwrapper.sh
add2virtualenv /var/tmp/de_venv/lib64/python3.9/site-packages/

# Useful info
python3 -m site
echo ''

python3 setup.py bdist_wheel
python3 -m pip install -e .
python3 -m pip install -e .[develop]

echo''
python3 -m pip list -v

# make sure the pipe doesn't eat failures
set -o pipefail

export PYTHONPATH=${PWD}/src:${PYTHONPATH}
echo "PYTHONPATH: ${PYTHONPATH}"

# PROMETHEUS_MULTIPROC_DIR is set in the framework Dockerfile
# but this is causing test_check_metrics_env_var_unset to fail
# so we unset this variable
unset PROMETHEUS_MULTIPROC_DIR

if [[ ${CMD} =~ "make-release" ]]; then
    # run make-release
    cur_revision=$(git describe --tags| sed -r 's/-([0-9]*)-/.dev\1+/g')
    echo "cur_revision: ${cur_revision}"
    # podman runs this python script from decisionengine folder, we need to move in the parent folder to run make-release.sh
    cd ..
    decisionengine/package/release/make-release.sh -v -e -s ${cur_revision} -t ${cur_revision} ${cur_revision} 2>&1 | tee ${LOGFILE}

else
    # run the python "module/command"
    python3 ${CMD} 2>&1 | tee ${LOGFILE}

fi
