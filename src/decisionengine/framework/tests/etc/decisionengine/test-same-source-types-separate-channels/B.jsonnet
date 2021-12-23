{
  sources: {
    int_source_b: {
      module: "decisionengine.framework.tests.IntSource",
      parameters: {
        int_value: 7
      },
      schedule: 2,
    },
  },
  transforms: {},
  publishers: {
    verify: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["int_value"],
        expects: 7,
      },
    },
  },
}
