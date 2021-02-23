#!/bin/bash -x
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
export PATH=$PATH:/usr/pgsql-11/bin
python3 -m pip install --upgrade pip --user
python3 -m pip install --upgrade setuptools wheel setuptools-scm[toml] --user
python3 -m pip install -r ${GITHUB_WORKSPACE}/requirements/requirements-runtime.txt --user
python3 -m pip install -r ${GITHUB_WORKSPACE}/requirements/requirements-develop.txt --user
python3 setup.py bdist_wheel
# cannot use `tee` as it eats $? and we lose success/failure
python3 -m pytest 2>&1 > pytest.log 
RC=$?
cat pytest.log
exit ${RC}
