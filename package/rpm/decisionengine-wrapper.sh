#!/bin/sh

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Wrapper to run the decision engine commands without being the decisionengine user
#   su -s /bin/bash -c '' - decisionengine
#   export PATH="~/.local/bin:$PATH"
#   decisionengine --no-webserver

DE_USER=decisionengine
DE_CMD=$(basename "$0")
DE_HOME=$(getent passwd "$DE_USER" | cut -d: -f6 )

check_loop() {
  # Make sure that the script is not re-invoking itself
  [ "$0" = "$(command -v "$DE_CMD")" ]
}

# DECISIONENGINE_DEBUG - debug enabled if not empty (debug flags possible in the future)
if echo "$*" | grep -- "--debug"; then
  DECISIONENGINE_DEBUG=true
  export DECISIONENGINE_DEBUG
fi

# Check if decisionengine Python code is installed
# Library ~$DE_USER/.local/lib/python3.9/site-packages/decisionengine
DE_EXPECTED="$DE_HOME/.local/bin/decisionengine"
if [ ! -f "$DE_EXPECTED" ]; then
    # Looks it is missing. Print a warning and continue
    echo "WARNING. decisionengine command not found in $DE_EXPECTED."
    echo "The command will likely fail. Was the Python code installed? Use decisionengine-install-python"
fi
# Run the command, with su if needed. NOTE that decisionengine-init can run only as root
# Including '-m' in the su command to preserve the environment. Systemd sets some variables for Prometheus and config
# Anyway we need a login shell and -m is incompatible with -l. We want to preserve the sysconfig variables DE_OPTS,PROMETHEUS_MULTIPROC_DIR
if [ "$(id -u)" -eq 0 ]; then
    decisionengine-init.sh
    # su -s /bin/bash -m -l $DE_USER -c "export PATH=\"\$HOME/.local/bin:\$PATH\"; echo \$PATH; command -v \"$DE_CMD\"; \"$DE_CMD\" $(for i in "$@"; do echo -n "\"$i\" "; done;); echo \"Test END\""
    # If a variable is added to sysconfig/decisionengine, it should be added also to the -w option
    su -s /bin/bash -w DE_OPTS,PROMETHEUS_MULTIPROC_DIR -l -c "export PATH=\"\$DE_HOME/.local/bin:\$PATH\"; \"$DE_CMD\" $(for i in "$@"; do printf "%s" "\"$i\" "; done;)" $DE_USER
elif [ "$(whoami)" = "$DE_USER" ]; then
    export PATH="$DE_HOME/.local/bin:$PATH"
    "$DE_CMD" "$@"
else
    echo "decisionengine commands can be invoked only as $DE_USER or root user"
    exit 1
fi
