{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.SourceNOP",
      name: "SourceNOP",
      parameters: {},
      schedule: 1,
     }
   },

   transforms: {
     transform1: {
       module: "decisionengine.framework.tests.FailingTransformNOP",
       name : "TransformWithMisingProducesConsumes",
       parameters: {},
       schedule: 1
     }
   },

  logicengines: {},
  publishers: {}
}
