{
  sources: {
    int_source_a: {
      module: "decisionengine.framework.tests.IntSource",
      parameters: {
        int_value: 3
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
        expects: 3,
      },
    },
  },
}
