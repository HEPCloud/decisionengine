# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Publisher
from decisionengine.framework.modules.Publisher import Parameter


@Publisher.supports_config(
    Parameter("no_type"),
    Parameter("only_type", type=int),
    Parameter("default_only", default=2.5),
    Parameter("convert_to", type=int, default=3.2),  # Conflicting types: int wins
    Parameter("comment", type=str, comment="Single-line comment"),
    Parameter("comment_with_nl", type=str, comment="Comment with newline\n"),
)
class SupportsConfig(Publisher.Publisher):
    pass


Publisher.describe(SupportsConfig)
