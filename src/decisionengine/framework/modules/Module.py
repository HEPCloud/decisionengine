# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from collections import OrderedDict
from typing import Any

import structlog

from decisionengine.framework.dataspace import datablock
from decisionengine.framework.modules.logging_configDict import CHANNELLOGGERNAME


class Module:
    """
    A skeleton of a module
    """

    def __init__(self, set_of_parameters):
        self.parameters = set_of_parameters
        self.data_block = None
        self.channel_name = set_of_parameters["channel_name"]

        self.logger = structlog.getLogger(CHANNELLOGGERNAME)
        self.logger = self.logger.bind(class_name=type(self).__name__, channel=self.channel_name)

    def get_parameters(self):
        return self.parameters

    def get_data_block(self):
        return self.data_block

    def set_data_block(self, data_block):
        self.data_block = data_block


# ====================================================================================
# Auxiliary facilities for produces, consumes, and supports_config


def produces(**kwargs):
    def decorator_produces(cls):
        if cls._produces:
            raise RuntimeError(f"@produces has already been called for {cls.__name__}")
        cls._produces = kwargs
        return cls

    return decorator_produces


def consumes(**kwargs):
    def decorator_consumes(cls):
        if cls._consumes:
            raise RuntimeError(f"@consumes has already been called for {cls.__name__}")
        cls._consumes = kwargs
        # Now add product retrievers to class instance
        user_provided_new = cls.__new__

        def new_and_add_members(class_type, module_parameters, *args, **kwargs):
            consumer = user_provided_new(class_type)
            product_specifications = module_parameters.get("product_creators", {})
            for name, product_type in cls._consumes.items():
                # FIXME: Need to adjust configuration usage in next line!
                setattr(
                    consumer,
                    name,
                    datablock.ProductRetriever(name, product_type, product_specifications.get(name, Any)),
                )
            return consumer

        cls.__new__ = new_and_add_members
        return cls

    return decorator_consumes


def verify_products(producer, data):
    expected = OrderedDict(sorted(producer._produces.items()))
    actual = OrderedDict({name: type(value) for name, value in sorted(data.items())})
    if expected == actual:
        return

    expected_keys = set(expected.keys())
    actual_keys = set(actual.keys())
    missing_keys = expected_keys.difference(actual_keys)
    extra_keys = actual_keys.difference(expected_keys)
    err_msg = ""
    if missing_keys:
        err_msg += "\nThe following products were not produced:\n"
        for name in missing_keys:
            err_msg += f" - '{name}' of type '{expected[name].__name__}'\n"
    if extra_keys:
        err_msg += "\nThe following products were not declared:\n"
        for name in extra_keys:
            err_msg += f" - '{name}' of type '{actual[name].__name__}'\n"
    if err_msg:
        raise RuntimeError(err_msg)

    mismatched_types = []
    for (name, a_type), b_type in zip(expected.items(), actual.values()):
        if Any in (a_type, b_type):
            continue
        if a_type != b_type:
            a_name = getattr(a_type, "__name__", None)
            b_name = getattr(b_type, "__name__", None)
            mismatched_types.append((name, a_name, b_name))

    if not mismatched_types:
        return

    err_msg = "\nThe following products have the wrong types:\n"
    for name, a_type, b_type in mismatched_types:
        err_msg += f" - '{name}' (expected '{a_type}', got '{b_type}')\n"
    raise RuntimeError(err_msg)
