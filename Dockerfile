FROM sl:7
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm yum-plugin-priorities \
    && yum -y clean all
RUN yum -y install https://repo.opensciencegrid.org/osg/3.4/osg-3.4-el7-release-latest.rpm \
    && yum -y clean all
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
    && yum -y clean all
RUN yum -y install condor-python \
  python-pandas \
  gcc gcc-c++ libgcc \
  python-pip \
  git \
  python-unittest2 \
  python-behave \
  tmux \
  cmake \
  boost \
  boost-devel \
  libevent-devel \
  ncurses-devel \
  python-pytest \
  pytest \
  graphviz.x86_64 \
  rpm-build \
  rpm-build-libs \
  rpm-devel \
  mock \
  python-boto3 \
  python-psycopg2 \ 
  python-setuptools \
  && easy_install DBUtils \
  &&  yum -y install cmake3 python3-devel make \
  boost-python36-devel \
  python3-devel \
  boost-regex \
  boost-system \
  boost-python-devel \
  python-devel \
  redhat-lsb-core \
  python36-virtualenv \
  python-virtualenv \
  postgresql11-server \
  postgresql11-devel \
  pytest \
  python36-pytest \
  python36-tabulate \
  python2-tabulate \
  python36-pip \
  && pip install --upgrade pip \
  && pip3.6 install argparse WebOb astroid pylint pycodestyle unittest2 coverage sphinx DBUtils pytest mock \
  && yum -y clean all
ENTRYPOINT ["/bin/bash"]
