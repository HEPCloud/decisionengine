# HEPCloud Decision Engine
HEPCloud Decision Engine framework

# Building RPMs

* REQUIREMENTS: RHEL 7

* Install dependencies. Following is more than required and needs to be trimmed

<pre>
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install yum-plugin-priorities
yum clean all
yum install https://repo.grid.iu.edu/osg/3.4/osg-3.4-el7-release-latest.rpm
yum clean all
yum install condor-python
yum install python-pandas
yum install gcc gcc-devel  (gcc-devel doesn't exist)
yum install gcc* ( not done--what you really need is gcc, gcc-c++, libgcc) 
yum install python-pip
yum install git*
yum install python-unittest2
yum install python-behave
yum install tmux
yum install cmake
yum install boost
yum install boost-devel
yum install libevent-devel
yum install ncurses-devel
yum install ipython
yum install matplotlib
yum install python-matplotlib
yum install python-pytest  ( under SL7 this is python2-pytest)
yum install pytest
yum install graphviz.x86_64
yum install rpm-build
yum install rpm-build-libs
yum install rpm-devel
yum install mock
yum install python2-boto3
yum install python-psycopg2
yum install python-setuptools

easy_install DBUtils
</pre>

* Checkout the decision engine framework code
<pre>
cd /tmp
git clone https://github.com/HEPCloud/decisionengine.git
</pre>

* Build RPMs
<pre>/tmp/decisionengine/build/packaging/rpm/package.sh /tmp/decisionengine</pre>
