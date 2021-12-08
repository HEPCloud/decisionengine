# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
The utils/reaper.py is one of our console entry points.
Testing it requires the test user be either root or decisionengine,
since this isn't 'CI' friendly we are just making sure it is valid python.
"""


def test_valid_python():
    """make sure it is valid python"""
    from decisionengine.framework.util import reaper  # noqa: F401

    pass
