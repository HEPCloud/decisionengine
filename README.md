# HEPCloud Decision Engine
![run unit tests in SL7 container](https://github.com/HEPCloud/decisionengine/workflows/run%20unit%20tests%20in%20SL7%20container/badge.svg)

![Run CI](https://github.com/HEPCloud/decisionengine/workflows/Run%20CI/badge.svg)


HEPCloud Decision Engine framework

# Code Documentation

https://hepcloud.github.io/decisionengine/code/

# Building RPMs

At this time we recommend Boost version 1.58 or newer.

* REQUIREMENTS: RHEL 7

* Install dependencies, mostly from pip

```shell
yum -y install \
    https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el7-release-latest.rpm \
    https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
    yum-plugin-priorities \
 && yum -y clean expire-cache
yum -y install \
    rpm-build  \
    gcc gcc-c++ libgcc    \
    'cmake3 >= 3.16' make \
    boost boost-devel     \
    postgresql11-server   \
    postgresql11-devel    \
    python3 python3-devel \
    python3-virtualenv    \
    python3-psycopg2      \
    python3-sphinx        \
 && yum -y clean expire-cache
python3 -m pip install --user --upgrade pip
python3 -m pip install --user -r requirements.txt
```

* Checkout the decision engine framework code
```shell
cd /tmp
git clone https://github.com/HEPCloud/decisionengine.git
```

* Build the framework C++ library
```shell
mkdir -p /tmp/decisionengine/framework/logicengine/cxx/build
cd /tmp/decisionengine/framework/logicengine/cxx/build
cmake3 -DPython_FIND_IMPLEMENTATIONS=$(python3 -c 'import platform; print(platform.python_implementation())') -Dpybind11_DIR=$(pybind11-config --cmakedir) ..
make install
```

* For running tests, make sure you have `C.UTF-8` locale defined
```shell
sudo localedef -v -c -i en_US -f UTF-8 C.UTF-8
```

* To run tests,
```shell
pytest -v -l --durations=0 --tb=native /tmp/decisionengine
```

* Build RPMs
```shell
/tmp/decisionengine/build/packaging/rpm/package.sh /tmp/decisionengine
```
