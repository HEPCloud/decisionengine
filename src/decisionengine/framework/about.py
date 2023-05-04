# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
    PEP-0396 provides instructions for providing module versions
    While we are at it, add a few other useful bits
"""
try:
    # This is built by setuptools_scm
    from .version import version as __version__  # noqa: F401
except ImportError:  # pragma: no cover
    __version__ = "DEVELOPMENT"

__title__ = "decisionengine"
__description__ = "The HEPCloud Decision Engine Framework"
__author__ = "Fermilab"
__license__ = "Apache-2.0"
__url__ = "http://hepcloud.fnal.gov/"
