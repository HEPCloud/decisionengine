{
  sources: {
    second_source_C: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "b3",
      },
      schedule: 5,
    },
  },

  transforms: {},

  publishers: {
    second_publisher_C: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["b3"],
        expects: 1,
      },
    },
  },
}
