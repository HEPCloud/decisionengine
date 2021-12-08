# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import inspect


def _derived_class(cls, base_class):
    """
    Only matches subclasses that are not equal to the base class.
    """
    return cls is not base_class and issubclass(cls, base_class)


def all_subclasses(module, base_class):
    """
    Return all of a module's subclasses of the given base class.
    """
    class_members = inspect.getmembers(module, inspect.isclass)
    return [name for name, cls in class_members if _derived_class(cls, base_class)]
