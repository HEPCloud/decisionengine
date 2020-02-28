#!/bin/bash -x
echo $PWD
export PYTHONPATH=$PWD
mkdir decisionengine/framework/logicengine/cxx/build
cd decisionengine/framework/logicengine/cxx/build
cmake3 ..
make VERBOSE=1
cd ../../
ln -s cxx/build/ErrorHandler/RE.so
ln -s cxx/build/ErrorHandler/libLogicEngine.so
export LD_LIBRARY_PATH=$PWD
cd ../../

py.test -v --tb=native >  $GITHUB_WORKSPACE/test.log 2>&1
exit 0
