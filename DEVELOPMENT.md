<!--
SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
SPDX-License-Identifier: Apache-2.0
-->

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
You may want to setup automatic notifications for pre-commit enabled
repos: https://pre-commit.com/index.html#automatically-enabling-pre-commit-on-repositories

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

## Licensing compliance

Decison engine is released under the Apache 2.0 license and license compliance is
handled with the [REUSE](http://reuse.software/) tool.
REUSE is installed as development dependency or you can install it manually
(`pip install reuse`). All files should have a license notice:

- to check compliance you can use `reuse lint`. This is the command run also by the pre-commit and CI checks
- you can add on top of new files [SPDX license notices](https://spdx.org/licenses/) like
  ```
  # SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
  # SPDX-License-Identifier: Apache-2.0
  ```
- or let REUSE do that for you (`FILEPATH` is your new file):
  ```
  reuse addheader --year 2017 --copyright="Fermi Research Alliance, LLC" \
    --license="Apache-2.0" --template=compact FILEPATH
  ```
- Files that are not supported and have no comments to add the SPDX notice
  can be added to the `.reuse/dep5` file
- New licenses can be added to the project using `reuse download LCENSEID`. Please
  contact project management if this is needed.

# Building the package

The code is expected to package as an RPM via `python3 setup.py bdist_rpm` or
a python wheel.

NOTE:

- Make sure you have the necessary software to build RPMs

```shell
sudo yum install rpm-build
```

## Using the RPM

The RPM should create the services you need. But some dependencies are not available as RPM.
So you have to install them using `pip`. Not to pollute the system Python you should
install it in the `decisionengine` (the user used to run decisionengine) user's Python area.

Run this to install the python dependencies:

```shell
su decisionengine -s /bin/bash
python3 -m pip install --upgrade pip setuptools wheel --user
python3 /path/to/setup.py develop --user
python3 /path/to/setup.py develop --user --uninstall
exit
```

NOTE:

- The commands above should be run for the setup.py files of both decisionengine and decisionengine_modules.
- The decisionengine (and decisionengine_modules) RPMs must be installed before running the commands above.
  This will assure that the decisionengine user and its home directory exist.
