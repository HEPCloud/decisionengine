# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import describe
from decisionengine.framework.modules.describe import Parameter, supports_config
from decisionengine.framework.modules.Module import consumes, Module

__all__ = ["Parameter", "Publisher", "consumes", "describe", "supports_config"]


describe = describe.main_wrapper


class Publisher(Module):
    _consumes = {}

    def __init__(self, set_of_parameters):
        super().__init__(set_of_parameters)

    def publish(self, data_block=None):
        pass

    def shutdown(self):
        pass
