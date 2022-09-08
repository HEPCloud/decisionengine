# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# on dockerhub hepcloud/decision-engine-ci
#    The CI container should probably come from modules...
FROM redhat/ubi8:latest
LABEL description="hepcloud/decision-engine-framework-el8"

# You can select another version at container build time by setting
# this value to the expected version - ie 9.6
ARG PG_VERSION=12

# Set where to collect metrics "on disk"
ENV PROMETHEUS_MULTIPROC_DIR=/tmp

# If you want to run decisionengine in this container
# you'll need to bind mount onto these points
RUN mkdir -m 750 -p /var/log/decisionengine ; \
    mkdir -m 750 -p /etc/decisionengine

# Extra repos we need
#RUN yum install -y http://ftp.scientificlinux.org/linux/scientific/7x/repos/x86_64/yum-conf-softwarecollections-2.0-1.el7.noarch.rpm \
# && yum -y clean all
RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm \
 && yum -y clean all

# set PATH for build and runtime
ENV PATH="/usr/pgsql-${PG_VERSION}/bin:~/.local/bin:$PATH"
ARG PATH="/usr/pgsql-${PG_VERSION}/bin:~/.local/bin:$PATH"

# Install postgresql-${PG_VERSION}
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
 && yum -y clean all
RUN yum -y install postgresql$(echo -n ${PG_VERSION} | tr -d '.')-server \
                   postgresql$(echo -n ${PG_VERSION} | tr -d '.')-devel \
                   postgresql$(echo -n ${PG_VERSION} | tr -d '.') \
 && yum -y clean all

# Install utils
RUN yum -y install \
    python39 python39-rpm-macros python39-pip python39-setuptools python39-wheel \
    gcc gcc-c++ make python39-devel swig openssl-devel \
    git \
    rpm-build \
 && yum -y clean all

# Install CentOS 8 repo to get redis
RUN yum install -y http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/centos-stream-repos-8-6.el8.noarch.rpm \
    http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/centos-gpg-keys-8-6.el8.noarch.rpm \
 && yum -y clean all
# Install redis 5 server and tools
RUN yum install -y redis \
 && yum -y clean all

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
