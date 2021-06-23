#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eventually this should move to pyproject.toml
#  but setuptools must first gain support for parsing that

import importlib
import pathlib
import site
import sys
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Add this module to the import path to help centralize metadata
sys.path.append(str(here) + "/src")
about = importlib.import_module('decisionengine.framework.about')

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# pull in runtime requirements
runtime_require = ["jsonnet >= 0.17.0", "tabulate >= 0.8.7",
                   "toposort >= 1.6", "wheel >= 0.36.2",
                   "DBUtils >= 2.0",
                   "sqlalchemy >= 1.4.17",
                   "numpy == 1.19.5; python_version <= '3.6'",
                   "numpy >= 1.19.5; python_version >= '3.7'",
                   "pandas == 1.1.5; python_version <= '3.6'",
                   "pandas >= 1.1.5; python_version >= '3.7'",
                   "psycopg2-binary >= 2.8.6; platform_python_implementation == 'CPython'",  # noqa: E501
                   "psycopg2cffi >= 2.9.0; platform_python_implementation == 'PyPy'"]  # noqa: E501


devel_req = ["setuptools >= 51.2", "setuptools-scm >= 6.0.1",
             "setuptools-scm[toml] >= 6.0.1", "toml >= 0.10.2",
             "mock >= 4.0.3", "pytest >= 6.2.2", "pytest-cov >= 2.11.1",
             "pytest-flake8 >= 1.0.7", "pytest-postgresql >= 3.0.0",
             "pytest-timeout >= 1.4.2",
             "pylint >= 2.7.4",
             "importlib_resources >= 5.1.2; python_version <= '3.8'",
             "sphinx >= 3.5.3", "sphinx_rtd_theme >= 0.5.1"]

rpm_require = ["shadow-utils", "systemd", "python3"]

#
# Because some python modules are required, but not packaged
# add some additional "runtime" requirements so we can fetch,
# compile, and install the modules.
#
# NOTE: in an ideal world, we wouldn't need the following:
#       hopefully one day we can drop these.
#
__base_pip_requires = ['python3-pip', 'python3-setuptools', 'python3-wheel']
__jsonnet_requires = ['gcc', 'gcc-c++', 'make', 'python3-devel']
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
    setup_requires=["setuptools >= 51.2", "wheel >= 0.36.2", "setuptools_scm[toml] >= 6.0.1"],
    name=about.__title__,
    use_scm_version={"version_scheme": "post-release"},
    description=about.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about.__url__,
    author=about.__author__,
    license=about.__license__,
    package_dir={"": "src"},
    packages=find_packages(
        where="src", exclude=("*.tests", "*.tests.*", "build.*", "doc.*")
    ),
    install_requires=runtime_require,
    extras_require={
        "develop": devel_req,
    },
    entry_points={
        "console_scripts": [
            "de-reaper=decisionengine.framework.util.reaper:main",
            "decisionengine=decisionengine.framework.engine.DecisionEngine:main",  # noqa: E501
            "de-client=decisionengine.framework.engine.de_client:console_scripts_main",  # noqa: E501
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
