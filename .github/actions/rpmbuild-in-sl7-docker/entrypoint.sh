#!/bin/bash
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
decisionengine/build/packaging/rpm/package.sh decisionengine
status=$?
if [[ ! -e /var/tmp/`whoami`/rpm/decisionengine/RPMS/x86_64 ]];then
echo "Error: RPMS did not build"
exit 1
else
tar cf $GITHUB_WORKSPACE/rpmbuild.tar /var/tmp/`whoami`/rpm/decisionengine/RPMS/x86_64
exit 0
fi
