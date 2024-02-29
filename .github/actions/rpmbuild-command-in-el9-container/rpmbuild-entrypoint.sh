#!/bin/bash -xe

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

RPMBUILDOPTS=${1:- -bb package/rpm/decisionengine-deps.spec}
LOGFILE=${2:- rpmbuild.log}

# make sure the pipe doesn't eat failures
set -o pipefail

# run the rpmbuild command
rpmbuild ${RPMBUILDOPTS} 2>&1 | tee ${LOGFILE}
