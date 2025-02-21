#!/bin/sh

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Wrapper to run the decision engine commands without being the decisionengine user
#   su -s /bin/bash -c '' - decisionengine
#   export PATH="~/.local/bin:$PATH"
#   decisionengine --no-webserver

DE_USER=decisionengine
DE_CMD=$(basename "$0")

# Check if decisionengine Python code is installed
# Library ~$DE_USER/.local/lib/python3.9/site-packages/decisionengine
DE_EXPECTED="~$DE_USER/.local/bin/decisionengine"
if [ ! -f "$DE_EXPECTED" ]; then
    # Looks it is missing. Print a warning and continue
    echo "WARNING. decisionengine command not found in $DE_EXPECTED."
    echo "The command will likely fail. Was the Python code installed? Use decisionengine-install-python"
fi
# Run the command, with su if needed
if [ "$UID" -eq 0 ]; then
    # su -s /bin/bash -l $DE_USER -c "export PATH=\"\$HOME/.local/bin:\$PATH\"; echo \$PATH; command -v \"$DE_CMD\"; \"$DE_CMD\" $(for i in "$@"; do echo -n "\"$i\" "; done;); echo \"Test END\""
    su -s /bin/bash -l -c "export PATH=\"\$HOME/.local/bin:\$PATH\"; \"$DE_CMD\" $(for i in "$@"; do echo -n "\"$i\" "; done;)" $DE_USER
elif [ "$(whoami)" = "$DE_USER" ]; then
    export PATH="$HOME/.local/bin:$PATH"
    "$DE_CMD" "$@"
else
    echo "decisionengine commands can be invoked only as $DE_USER or root user"
    exit 1
fi
