#!/bin/bash -x
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
source decisionengine/build/scripts/utils.sh
setup_python_venv
setup_dependencies
export PYTHONPATH=$PWD:$PYTHONPATH
source venv/bin/activate
export PATH=$PATH:/usr/pgsql-11/bin
which pytest
pytest -v --tb=native decisionengine >  ./pytest.log 2>&1
status=$?
cat ./pytest.log
exit $status
