# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import describe
from decisionengine.framework.modules.describe import Parameter, supports_config
from decisionengine.framework.modules.Module import consumes, Module, produces

__all__ = ["Parameter", "Transform", "consumes", "describe", "produces", "supports_config"]


describe = describe.main_wrapper


class Transform(Module):
    _consumes = {}
    _produces = {}

    def __init__(self, set_of_parameters):
        super().__init__(set_of_parameters)
        self.name_list = []

    """
    decide: The action function for a Transform. Will
    retrieve from the DataBlock the data products
    listed by consumes and performs algorithmic
    operation on them. The Transform will issue a
    DataBlock "put" transaction for each of the data
    products promised in the produces list
    """

    def transform(self):
        print("Called Transform.transform")
