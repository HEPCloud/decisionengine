# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# on dockerhub hepcloud/decision-engine-ci
#    The CI container should probably come from modules...
FROM almalinux:9
LABEL description="hepcloud/decision-engine-framework-el9"

# You can select another version at container build time by setting
# this value to the expected version - ie 13
ARG PG_VERSION=13

# Set where to collect metrics "on disk"
ENV PROMETHEUS_MULTIPROC_DIR=/tmp

# If you want to run decisionengine in this container
# you'll need to bind mount onto these points
RUN mkdir -m 750 -p /var/log/decisionengine ; \
    mkdir -m 750 -p /etc/decisionengine

# Extra repos we need
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm \
 && dnf -y clean all

# set PATH for build and runtime
ENV PATH="/usr/pgsql-${PG_VERSION}/bin:~/.local/bin:$PATH"
ARG PATH="/usr/pgsql-${PG_VERSION}/bin:~/.local/bin:$PATH"

# Install postgresql-${PG_VERSION}
RUN dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
 && dnf -y clean all
RUN dnf -y install --enablerepo crb \
            postgresql${PG_VERSION}-server \
            postgresql${PG_VERSION}-devel \
            postgresql${PG_VERSION} \
 && dnf -y clean all

# Install utils
RUN dnf -y install --enablerepo crb \
    python3 python3-rpm-macros python3-pip python3-setuptools python3-wheel \
    gcc gcc-c++ make python3-devel swig openssl-devel \
    git \
    rpm-build \
 && dnf -y clean all

# Install redis server and tools
RUN dnf install -y redis \
 && dnf -y clean all

# Ensure pip/setuptools are up to date
#  rpm-build requires libraries in /usr
RUN python3 -m pip install --upgrade --prefix=/usr pip ; \
    python3 -m pip install --upgrade --prefix=/usr setuptools wheel setuptools-scm[toml]

# Install decisionengine requirements (runtime and testing)
#  do as one layer to simplify merges
#  rpm-build requires libraries in /usr
RUN su - adm -s /bin/bash -c "git clone https://github.com/HEPCloud/decisionengine.git /tmp/decisionengine.git"; \
    cd /tmp/decisionengine.git ; \
    su adm -s /bin/bash -c "cd /tmp/decisionengine.git ; python3 setup.py bdist_wheel" ; \
    python3 -m pip install --prefix=/usr dist/*.whl ; \
    python3 -m pip install --prefix=/usr decisionengine[develop] ; \
    python3 -m pip uninstall -y decisionengine ; \
    rm -rf /tmp/decisionengine.git

ENTRYPOINT ["/bin/bash"]
