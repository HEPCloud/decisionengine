# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Source
from decisionengine.framework.tests import SourceWithSampleConfigNOP

SourceAlias = SourceWithSampleConfigNOP.SourceWithSampleConfigNOP
Source.describe(SourceAlias)
