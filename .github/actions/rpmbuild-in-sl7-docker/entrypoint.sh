#!/bin/bash
PYVER=${1:-"2.7"}
export PYVER
echo PYVER=$PYVER
decisionengine/build/packaging/rpm/package.sh decisionengine
status=$?
tar cf $GITHUB_WORKSPACE/rpmbuild-$PYVER.tar /var/tmp/`whoami`/rpm/decisionengine/*
exit $status
