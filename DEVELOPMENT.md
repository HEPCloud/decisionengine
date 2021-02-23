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

`python3 setup.py develop --user`

The development environment has a number of extra requirements you can load
`python3 -m pip install --user decisionengine[develop]`

From here `pytest` should "just work".

NOTE:
* For running tests, make sure you have `C.UTF-8` locale defined
```shell
sudo localedef -v -c -i en_US -f UTF-8 C.UTF-8
```

# Building the package

The code is expected to package as an RPM via `python3 setup.py bdist_rpm` or
a python wheel.
