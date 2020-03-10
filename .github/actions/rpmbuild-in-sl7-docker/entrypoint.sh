#!/bin/bash
echo PYVER=$1
export PYVER=$1
decisionengine/build/packaging/rpm/package.sh decisionengine
tar cvf $GITHUB_WORKSPACE/rpmbuild-$PYVER.tar /var/tmp/root/rpm/decisionengine/*
exit 0
