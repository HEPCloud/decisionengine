#!/bin/bash -x
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
source decisionengine/build/scripts/utils.sh
setup_python_venv
setup_dependencies
le_builddir=decisionengine/framework/logicengine/cxx/build
[ -e $le_buildir ] && rm -rf $le_builddir
mkdir $le_builddir
cd $le_builddir
cmake3 -Wno-dev --debug-output -DPYVER=3.6 .. -Dpybind11_DIR=$(pybind11-config --cmakedir)
make install --debug
cd -
export PYTHONPATH=$PWD:$PYTHONPATH
source venv/bin/activate
export PATH=$PATH:/usr/pgsql-11/bin
which pytest
pytest -v --tb=native decisionengine >  ./pytest.log 2>&1
status=$?
cat ./pytest.log
exit $status
