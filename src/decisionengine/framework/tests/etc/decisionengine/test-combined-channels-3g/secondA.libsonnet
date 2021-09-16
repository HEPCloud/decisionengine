{
  sources: {
    from_first_channel: {
      module: "decisionengine.framework.modules.SourceProxy",
      parameters: {
        source_channel: "first",
        Dataproducts: ["a"],
        max_attempts: 3,
        retry_interval: 10,
      },
      schedule: 1,
    },
    second_source_A: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "_b1",
      },
      schedule: 5,
    },
  },

  transforms: {
    second_transform_A: {
      module: "decisionengine.framework.tests.DynamicTransform",
      parameters: {
        consumes: ["a", "_b1"],
        data_product_name: "b1",
      },
    },
  },

  publishers: {
    second_publisher_A: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["b1"],
        expects: 2,
      },
    },
  },
}
