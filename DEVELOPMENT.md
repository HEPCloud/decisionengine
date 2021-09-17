# HEPCloud Decision Engine

HEPCloud Decision Engine framework development

# Code Documentation

https://hepcloud.github.io/decisionengine/code/

# Developer Workflow

https://github.com/HEPCloud/decisionengine/wiki/Development-Workflow

# Getting Started with development

NOTE: It is recommended you use postgresql 11 or newer.
https://www.postgresql.org/download/

NOTE: The python dependencies of this project may require
additional OS features for build if python wheels
are not available for your platform.

NOTE: This project has a pre-commit config.
To install it run `pre-commit install` from the repository root.

Make sure you have up to date versions of `pip`, `setuptools`, and `wheel`.

`python3 -m pip install --upgrade pip setuptools wheel --user`

Now you can perform an editable install of the code base.

`python3 setup.py develop --user`

The development environment has a number of extra requirements you can load
`python3 -m pip install --user decisionengine[develop]`

From here `pytest` should "just work".

NOTE:

- For running tests, make sure you have `C.UTF-8` locale defined

```shell
sudo localedef -v -c -i en_US -f UTF-8 C.UTF-8
```

# Building the package

The code is expected to package as an RPM via `python3 setup.py bdist_rpm` or
a python wheel.

## Using the RPM

The RPM should create the services you need. But you may not have all the
items you need in the `decisionengine` user's python area (ie not system packages).

This should clean that up, provided you can write to the user home area.

```shell
su decisionengine -c /bin/bash
python3 -m pip install --upgrade pip setuptools wheel --user
python3 /path/to/setup.py develop --user
python3 /path/to/setup.py develop --user --uninstall
```
