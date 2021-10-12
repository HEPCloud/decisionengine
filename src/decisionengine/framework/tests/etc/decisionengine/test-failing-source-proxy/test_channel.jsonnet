{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.SourceNOP",
      parameters: {
        sleep_for: 5,
      },
      schedule: 1,
    },
  },

  transforms: {
    transform1: {
      module: "decisionengine.framework.tests.TransformNOP",
      parameters: {},
    },
  },

  publishers: {},
}
