#!/bin/bash -xe
GITHUB_WORKSPACE=${GITHUB_WORKSPACE:-`pwd`}
python3 -m pip install --upgrade pip --user
python3 -m pip install --upgrade setuptools wheel setuptools-scm[toml] --user
python3 -m pip install -r ${GITHUB_WORKSPACE}/requirements/requirements-develop.txt --user
python3 setup.py bdist_rpm
