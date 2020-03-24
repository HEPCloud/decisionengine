#!/bin/bash
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
decisionengine/build/scripts/run_pylint.sh
tar cvfj $GITHUB_WORKSPACE/logs.tar.bz2 pep8.*.log pylint.*.log
cat pep8.*.log pylint.*.log
exit `cat pep8.*.log pylint.*.log| wc -l`
