#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Eventually this should move to pyproject.toml
#  but setuptools must first gain support for parsing that

import os
import pathlib
import platform
import sys
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Add this module to the import path to help centralize metadata
sys.path.append(str(here))
sys.path.append(str(here) + '/src')
from src.decisionengine.framework import about

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# pull in runtime requirements
require = []
rpm_require = ['shadow-utils', 'systemd']
devel_req = []
try:
    with open('requirements/requirements-runtime.txt') as _fd:
        for item in _fd.readlines():
            req = item.partition('#')[0].partition('-')[0].partition('>')[0].partition('=')[0]
            req = req.replace(' ','').replace('\n','')
            if req != '' and not req.startswith('http'):
                if platform.python_implementation() == 'CPython':
                    if req != 'psycopg2cffi':
                        # Disable more detailed RPM requires for now
                        # TODO: resolve this long term for deployment
                        #rpm_require.append('python3-' + req.partition(';')[0])
                        require.append(req)
                elif platform.python_implementation() == 'PyPy':
                    if req != 'psycopg2-binary':
                        rpm_require.append('python3-' + req.partition(';')[0])
                        require.append(req)
                else:
                    raise NotImplementedError("Unknown python implementation")

except FileNotFoundError:
    print("", file=sys.stderr)
    print("> You are probably running without setuptools-scm and toml", file=sys.stderr)
    print("", file=sys.stderr)
    raise

# read in development requirements in development environment
with open('requirements/requirements-develop.txt') as _fd:
    for item in _fd.readlines():
        req = item.partition('#')[0].partition('-')[0].partition('>')[0].partition('=')[0]
        if req != '' and not req.startswith('http'):
            devel_req.append(req)

# This metadata can be read out with:
#    import importlib.metadata
#    dir(importlib.metadata.metadata('decisionengine'))
#  or
#    importlib_resources on python < 3.9
#
# Much of it comes out of decisionengine.framework.about.py
setup(
  setup_requires=['setuptools', 'wheel', 'setuptools_scm', 'toml'],
  name = about.__title__,
  use_scm_version = {
        "version_scheme": "post-release"
  },
  description = about.__description__,
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = about.__url__,
  author = about.__author__,
  license = about.__license__,
  package_dir={'': 'src'},
  packages = find_packages(where='src', exclude=('*.tests', '*.tests.*', 'build.*', 'doc.*')),
  install_requires = require,
  extras_require = {
    'develop': devel_req,
  },
  entry_points = {
    'console_scripts': [
      'de-reaper=decisionengine.framework.utils.reaper:main',
      'decisionengine=decisionengine.framework.engine.DecisionEngine:main',
      'de-client=decisionengine.framework.engine.de_client:main',
    ],
  },
  options = {'bdist_rpm': {
    'build_requires': 'python3',
    'provides': "python3-" + about.__title__,
    'install_script': 'package/rpm/install_section',
    'post_install': 'package/rpm/post_install_section',
    'post_uninstall': 'package/rpm/post_uninstall_section',
    'requires': rpm_require,
  },},
  zip_safe = True,
)
