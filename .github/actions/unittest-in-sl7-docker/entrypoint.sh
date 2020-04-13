#!/bin/bash -x
PYVER=${1:-"2.7"}
export PYVER
echo PYVER=$PYVER
source decisionengine/build/scripts/utils.sh
setup_python_venv
setup_dependencies
le_builddir=decisionengine/framework/logicengine/cxx/build
[ -e $le_buildir ] && rm -rf $le_builddir
mkdir $le_builddir
cd $le_builddir
cmake3 -Wno-dev --debug-output -DPYVER=$PYVER ..
make --debug
make --debug liblinks
cd -
export PYTHONPATH=$PWD:$PYTHONPATH
source venv-$PYVER/bin/activate
which pytest
pytest -v --tb=native decisionengine >  ./pytest-$PYVER.log 2>&1
status=$?
#if [ "$PYVER" == "3.6" ];then
#which pytest
#pytest -v --tb=native decisionengine >  ./pytest-$PYVER.log 2>&1
#status=$?
#else
#which py.test
#py.test -v --tb=native decisionengine >  ./pytest-$PYVER.log 2>&1
#status=$?
#fi
cat ./pytest-$PYVER.log
exit $status
