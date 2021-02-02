FROM sl:7
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm yum-plugin-priorities \
    && yum -y clean all
RUN yum -y install https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el7-release-latest.rpm \
    && yum -y clean all
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
    && yum -y clean all
RUN yum -y install yum-conf-softwarecollections && yum -y clean all
RUN yum -y install \
  gcc gcc-c++ libgcc \
  python-pip \
  git \
  tmux \
  libevent-devel \
  ncurses-devel \
  graphviz.x86_64 \
  rpm-build \
  rpm-build-libs \
  rpm-devel \
  mock \
  python3-devel make \
  python-devel \
  redhat-lsb-core \
  python36-virtualenv \
  python-virtualenv \
  postgresql11-server \
  postgresql11-devel \
  python36-pip \
  python36-m2crypto \
  python-rrdtool \
  osg-wn-client \
  vo-client \
  voms-clients-cpp \
  python36-ldap3 \
  python36-jwt \
  PyYAML \
  && yum -y clean all
ENTRYPOINT ["/bin/bash"]
