# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
Make sure decisionengine.framework is a valid python package
"""


def test_can_import():
    from decisionengine import framework  # noqa: F401

    pass
