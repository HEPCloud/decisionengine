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
    rpm-build mock \
 && dnf -y clean all

# Install redis server and tools
RUN dnf install -y redis \
 && dnf -y clean all

# Prepare a venv and ensure we have up to date pip/setuptools/build modules
RUN su - adm -s /bin/bash -c "python3 -m venv /var/tmp/de_venv ; \
    source /var/tmp/de_venv/bin/activate ; \
    python3 -m pip install --upgrade pip ; \
    python3 -m pip install --upgrade setuptools wheel setuptools-scm[toml] build"

# Install decisionengine requirements (runtime and testing) in the venv
RUN su - adm -s /bin/bash -c "source /var/tmp/de_venv/bin/activate ; \
    git clone https://github.com/HEPCloud/decisionengine.git /tmp/decisionengine.git ; \
    cd /tmp/decisionengine.git ; \
    python3 setup.py bdist_wheel ; \
    python3 -m pip install dist/*.whl ; \
    python3 -m pip install decisionengine[develop] ; \
    python3 -m pip uninstall -y decisionengine ; \
    rm -rf /tmp/decisionengine.git"

ENTRYPOINT ["/bin/bash"]
