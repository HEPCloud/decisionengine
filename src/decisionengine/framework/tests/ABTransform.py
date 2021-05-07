from decisionengine.framework.modules import Transform


@Transform.consumes(B=None)
@Transform.produces(A=None)
class ABTransform(Transform.Transform):
    pass
