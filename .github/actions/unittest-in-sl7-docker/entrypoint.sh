#!/bin/bash
export PYVER=$1
echo PYVER=$PYVER
echo PWD=$PWD
export PYTHONPATH=$PWD

[ -d decisionengine/framework/logicengine/cxx/build ] && rm -rf  decisionengine/framework/logicengine/cxx/build
OLDWD=$PWD
mkdir decisionengine/framework/logicengine/cxx/build
cd decisionengine/framework/logicengine/cxx/build
cmake3 .. -DPYVER=$PYVER
make VERBOSE=1
cd ../../
[ -f RE.so ] && rm RE.so
ln -s cxx/build/ErrorHandler/RE.so
[ -f libLogicEngine.so ] && rm libLogicEngine.so
ln -s cxx/build/ErrorHandler/libLogicEngine.so
export LD_LIBRARY_PATH=$PWD
cd $OLDWD

if [ "$PYVER" == "3.6" ] ;then
py.test-3 -v --tb=native decisionengine >  ./test-$PYVER.log 2>&1
status=$?
else
py.test -v --tb=native decisionengine >  ./test-$PYVER.log 2>&1
status=$?
fi
exit $status
