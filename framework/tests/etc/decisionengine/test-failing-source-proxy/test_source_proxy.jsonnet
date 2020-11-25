{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.FailingSourceProxy",
      name: "FailingSourceProxy",
      parameters: {
        channel_name: 'test_channel',
        Dataproducts: ['foo'],
        retries: 1,
        retry_to: 0
      },
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
