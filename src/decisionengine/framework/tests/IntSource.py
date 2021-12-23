# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Source
from decisionengine.framework.modules.Source import Parameter


@Source.supports_config(Parameter("int_value", type=int))
@Source.produces(int_value=int)
class IntSource(Source.Source):
    def __init__(self, config):
        self._value = config["int_value"]

    def acquire(self):
        return {"int_value": self._value}


Source.describe(IntSource)
