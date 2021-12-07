# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.modules import Transform


@Transform.consumes(B=None)
@Transform.produces(A=None)
class ABTransform(Transform.Transform):
    pass
