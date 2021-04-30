{
  sources: {},
  transforms: {
    transform1: {
      module: "decisionengine.framework.tests.FailingTransformNOP",
      name : "TransformWithMisingProducesConsumes",
      parameters: {},
    }
  },
  logicengines: {},
  publishers: {}
}
