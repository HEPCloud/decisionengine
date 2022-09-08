# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# on dockerhub hepcloud/??????
FROM redhat/ubi8:latest
LABEL description="hepcloud/decision-engine-framework-minimal-el8"

# If you want to run decisionengine in this container
# you'll need to bind mount onto these points
RUN mkdir -m 750 -p /var/log/decisionengine ; \
    mkdir -m 750 -p /etc/decisionengine

# Identity information for the decisionengine user
ARG UID=1001
ARG USERNAME=decisionengine
ARG GID=116
ARG GROUPNAME=decisionengine
ARG HOMEDIR=/home/decisionengine

# Make user and place for logs/configs owned correctly
RUN groupadd -g $GID $GROUPNAME ; \
    useradd -u $UID -g $GID -d $HOMEDIR -m $USERNAME ; \
    chown $USERNAME:$GROUPNAME /var/log/decisionengine /etc/decisionengine

# Extra repos we need
RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm \
 && yum -y clean all

# Install python utils we need
RUN yum -y install \
    python39 python39-rpm-macros python39-pip python39-setuptools python39-wheel \
 && yum -y clean all

# Wheels for these don't always exist for these on our python version
RUN yum -y install --enablerepo=epel \
    python39-jsonnet python39-psycopg2 \
 && yum -y clean all

# Ensure pip/setuptools are up to date
#  updates put into /usr/local
RUN python3 -m pip install --upgrade pip ; \
    python3 -m pip install --upgrade setuptools wheel setuptools-scm[toml]

# Install decisionengine requirements (runtime)
#  do as one layer to simplify merges
#  new/updates put into /usr/local
RUN su - adm -s /bin/bash -c "git clone https://github.com/HEPCloud/decisionengine.git /tmp/decisionengine.git"; \
    cd /tmp/decisionengine.git ; \
    su adm -s /bin/bash -c "cd /tmp/decisionengine.git ; python3 setup.py bdist_wheel" ; \
    python3 -m pip install dist/*.whl ; \
    python3 -m pip uninstall -y decisionengine ; \
    rm -rf /tmp/decisionengine.git

# Become container user
USER $USERNAME
WORKDIR $HOMEDIR

# Set where to collect metrics "on disk"
ENV PROMETHEUS_MULTIPROC_DIR=/tmp/

ENTRYPOINT ["/home/decisionengine/src/decisionengine/framework/engine/DecisionEngine.py"]
