from decisionengine.framework.modules import Transform


@Transform.consumes(A=None)
@Transform.produces(B=None)
class BATransform(Transform.Transform):
    pass
