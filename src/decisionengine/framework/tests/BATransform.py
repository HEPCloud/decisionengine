# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Transform


@Transform.consumes(A=None)
@Transform.produces(B=None)
class BATransform(Transform.Transform):
    pass
