# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

ARG BASEIMAGE=hepcloud/decision-engine-ci-el9
FROM ${BASEIMAGE}
COPY python3-entrypoint.sh /entrypoint.sh

# Identity information for the decisionengine user
ARG UID=1001
ARG USERNAME=decisionengine
ARG GID=116
ARG GROUPNAME=decisionengine
ARG HOMEDIR=/home/decisionengine

# Make user and place for logs/configs
RUN groupadd -g $GID $GROUPNAME ; \
    useradd -u $UID -g $GID -d $HOMEDIR -m $USERNAME ; \
    usermod -a -G mock $USERNAME ; \
    chown $USERNAME:$GROUPNAME /var/log/decisionengine /etc/decisionengine

# Become container user
USER $USERNAME
WORKDIR $HOMEDIR

ENTRYPOINT ["/entrypoint.sh"]
