{
  sources: {
    source1: {
      module: "decisionengine.framework.modules.SourceProxy",
      parameters: {
        source_channel: "test_channel",
        Dataproducts: ["foo"],
        max_attempts: 5,
      },
      schedule: 1,
    },
  },
  transforms: {},
  publishers: {
    pub1: {
      module: "decisionengine.framework.tests.WriteToDisk",
      parameters: {
        consumes: ["foo"],
      },
    },
  },
}
