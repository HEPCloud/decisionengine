#!/bin/bash

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Initialization script for Decision Engine and its modules
# It will run all the executable files in DE_INIT_DIR
# Assuming that all scripts do only persistent changes on the file system and are idempotent
DE_INIT_DIR=/etc/decisionengine/init.d
DE_INIT_LAST="$DE_INIT_DIR"/.lastrun

# Emulate function library.
success() {
    echo -en "\033[60G[[32mOK[0m]"
    return 0
}

failure() {
    echo -en "\033[60G[[31mFAILED[0m]"
    return 1
}

log_debug() {
  [[ -z "$DECISIONENGINE_DEBUG" ]] || echo "$@"
}

if [[ -d "$DE_INIT_DIR" ]]; then
  # Check if the init scripts changed from the last execution
  # if [ -f $TSTF ] && find ./start -newer $TSTF -print -exec false {} + -quit; then echo "NO new"; else echo GO; touch $TSTF; fi
  if [[ -f "$DE_INIT_LAST" ]] && find "$DE_INIT_DIR" -newer "$DE_INIT_LAST" -exec false {} + -quit; then
    log_debug "No new Decision Engine init file"
    exit 0
  fi
  touch "$DE_INIT_LAST"

  # Running the scripts
  pushd "$DE_INIT_DIR" || exit 1
  for i in *; do
    [[ -x "$i" ]] || continue
    log_debug -n "Running '$i':"
    if ./"$i"; then
      log_debug OK
    else
      log_debug FAILED
    fi
  done
  popd || exit 1
fi
