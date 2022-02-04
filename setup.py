#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# Eventually this should move to pyproject.toml
#  but setuptools must first gain support for parsing that

import importlib
import os
import pathlib
import site
import sys

from setuptools import find_packages, setup

if os.geteuid() == 0:
    raise RuntimeError("You should not run this as root, make a wheel or rpm as not root")

here = pathlib.Path(__file__).parent.resolve()

# Add this module to the import path to help centralize metadata
sys.path.append(str(here) + "/src")
about = importlib.import_module("decisionengine.framework.about")

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# pull in runtime requirements
runtime_require = [
    "cherrypy >= 18.6.0",
    "kombu[redis] >= 5.1.0",
    "jsonnet >= 0.17.0",
    "prometheus-client >= 0.10.0",
    "tabulate >= 0.8.7",
    "toposort >= 1.6",
    "sqlalchemy >= 1.4.20",
    "structlog >= 21.1.0",
    "numpy == 1.19.5; python_version <= '3.6'",
    "numpy >= 1.19.5; python_version >= '3.7'",
    "pandas == 1.1.5; python_version <= '3.6'",
    "pandas >= 1.1.5; python_version >= '3.7' and platform_python_implementation == 'CPython'",
    "psycopg2-binary >= 2.8.6; platform_python_implementation == 'CPython'",  # noqa: E501
]  # noqa: E501

devel_req = [
    "setuptools >= 51.2",
    "setuptools_scm >= 6.3.1",
    "toml >= 0.10.2",
    "packaging >= 20.4",
    "wheel >= 0.36.2",
    "coverage == 6.1.2",  # https://github.com/nedbat/coveragepy/issues/1300
    "pytest >= 6.2.2, < 7.0",  # pytest 7 incompatible with pytest-postgres < 4
    "pytest-cov >= 2.11.1",
    "pytest-flake8 >= 1.0.7",
    "pytest-postgresql >= 3.0.0, < 4.0.0",
    "pytest-timeout >= 1.4.2",
    "pytest-xdist[psutil] >= 2.3.0",
    "pre-commit >= 2.13.0",
    "pylint >= 2.7.4",
    "reuse",
    "importlib_resources >= 5.1.2; python_version <= '3.8'",
    "sphinx >= 3.5.3",
    "sphinx_rtd_theme >= 0.5.1",
]

rpm_require = ["shadow-utils", "systemd", "python3"]

#
# Because some python modules are required, but not packaged
# add some additional "runtime" requirements so we can fetch,
# compile, and install the modules.
#
# NOTE: in an ideal world, we wouldn't need the following:
#       hopefully one day we can drop these.
#
__base_pip_requires = ["python3-pip", "python3-setuptools", "python3-wheel"]
__jsonnet_requires = ["gcc", "gcc-c++", "make", "python3-devel"]
rpm_require.extend(__base_pip_requires)
rpm_require.extend(__jsonnet_requires)

# workaround bug in editable install when PEP517 is detected
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

# This metadata can be read out with:
#    import importlib.metadata
#    dir(importlib.metadata.metadata('decisionengine'))
#  or
#    importlib_resources on python < 3.9
#
# Much of it comes out of decisionengine.framework.about.py
setup(
    setup_requires=["setuptools >= 51.2", "wheel >= 0.36.2", "setuptools_scm >= 6.3.1"],
    name=about.__title__,
    description=about.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about.__url__,
    author=about.__author__,
    license=about.__license__,
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=("tests", "*.tests", "*.tests.*", "build.*", "doc.*")),
    package_data={"decisionengine.framework.config": ["de_std.libsonnet"]},
    install_requires=runtime_require,
    extras_require={
        "develop": devel_req,
    },
    entry_points={
        "console_scripts": [
            "de-reaper=decisionengine.framework.util.reaper:main",
            "decisionengine=decisionengine.framework.engine.DecisionEngine:main",
            "de-client=decisionengine.framework.engine.de_client:console_scripts_main",
            "de-query-tool=decisionengine.framework.engine.de_query_tool:console_scripts_main",
            "de-logparser=decisionengine.framework.util.logparser:console_scripts_main",
        ],
    },
    options={
        "bdist_rpm": {
            "build_requires": "python3",
            "provides": "python3-" + about.__title__,
            "install_script": "package/rpm/install_section",
            "pre_install": "package/rpm/pre_install_section",
            "post_install": "package/rpm/post_install_section",
            "post_uninstall": "package/rpm/post_uninstall_section",
            "requires": rpm_require,
        },
    },
    zip_safe=True,
)
