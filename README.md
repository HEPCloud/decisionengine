# HEPCloud Decision Engine
[![Travis Status](https://travis-ci.com/HEPCloud/decisionengine.svg?branch=master)](https://travis-ci.com/HEPCloud/decisionengine) [![Docker Unit Tests](https://github.com/HEPCloud/decisionengine/workflows/.github/workflows/unit-test.yaml/badge.svg)](https://github.com/HEPCloud/decisionengine/actions?query=workflow%3A.github%2Fworkflows%2Funit-test.yaml)

HEPCloud Decision Engine framework

# Code Documentation

https://hepcloud.github.io/decisionengine/code/

# Building RPMs

At this time we recommend Boost version 1.58 or newer.  You may need to complile this for your python interpreter.

* REQUIREMENTS: RHEL 7

* Install dependencies. Following is more than required and needs to be trimmed

<pre>
yum -y install \
    https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    yum-plugin-priorities \
  && yum -y clean all
yum -y install \
   https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el7-release-latest.rpm \
  && yum -y clean all
yum -y install \
    https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
  && yum -y clean all
yum -y install \
    condor-python \
    python-pandas \
    gcc gcc-c++ libgcc \
    python-pip \
    git \
    python-unittest2 \
    python-behave \
    tmux \
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
  && easy_install DBUtils
yum -y install \
    python3-devel make \
    python3-devel \
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
  && pip3.6 install argparse WebOb astroid pylint pycodestyle unittest2 coverage sphinx DBUtils pytest mock jsonnet \
  && yum -y clean all
</pre>

* Checkout the decision engine framework code
<pre>
cd /tmp
git clone https://github.com/HEPCloud/decisionengine.git
</pre>

* For running tests, make sure you have `C.UTF-8` locale defined
<pre>
sudo localedef -v -c -i en_US -f UTF-8 C.UTF-8
</pre>

* Build RPMs
<pre>/tmp/decisionengine/build/packaging/rpm/package.sh /tmp/decisionengine</pre>
