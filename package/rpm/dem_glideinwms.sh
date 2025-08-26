#!/bin/bash

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Initialization script for the GlideinWMS module in Decision Engine Modules
# This should run before running Decision Engine with the GlideinWMS module

DE_USER=decisionengine
DE_PASS_NAME=${DE_USER^^}
DE_HOME=$(getent passwd "$DE_USER" | cut -d: -f6 )

check_idtoken_password() {
    # Make sure that the IDTOKEN password exists
    local de_password="$DE_HOME"/passwords.d/$DE_PASS_NAME
    if [ ! -f "$de_password" ]; then
        local htc_password=/etc/condor/passwords.d/$DE_PASS_NAME
        if [ ! -f "$htc_password" ]; then
            openssl rand -base64 64 | /usr/sbin/condor_store_cred -u "$DE_USER@$(hostname -f)" -f "$htc_password" add > /dev/null 2>&1
        fi
        if [ ! -f "$htc_password" ]; then
            echo 'Cannot create IDTOKENs password! Check if HTCondor is installed correctly'
            exit 1
        fi
        /bin/cp "$htc_password" "$de_password"
        chown $DE_USER: "$de_password"
        # The permission of $DE_HOME/passwords.d/${pass_fname} should be 0600
        if [ ! -f "$de_password" ]; then
            echo 'Cannot create IDTOKENs password! Check if HTCondor is installed correctly'
            exit 1
        fi
    fi
}

check_idtoken_password

# TODO: this is changing another RPM's files. A better solution is desired
# Make sure the decisionengine user ($DE_USER) is in the glidein group
if [[ -d /etc/gwms-frontend ]]; then
  chown -R $DE_USER: /etc/gwms-frontend
else
  echo '/etc/gwms-frontend is missing! Was the GlideinWMS Frontend installed?'
  exit 1
fi
