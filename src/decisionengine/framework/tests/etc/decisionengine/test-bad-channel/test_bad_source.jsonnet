{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.FailingSourceNOP",
      name: "SourceWithMisingProduces",
      parameters: {},
      schedule: 1,
     }
   },

   transforms: {
     transform1: {
       module: "decisionengine.framework.tests.TransformNOP",
       name : "TransformNOP",
       parameters: {},
       schedule: 1
     }
   },

  logicengines: {},
  publishers: {}
}
