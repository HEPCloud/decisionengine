#!/bin/bash
export PYVER=$1
echo PYVER=$PYVER
decisionengine/build/scripts/run_pylint.sh
tar cvfj $GITHUB_WORKSPACE/logs.tar.bz2 pep8.*.log pylint.*.log
exit 0
