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
    second_source_B: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "_b2",
      },
      schedule: 5,
    },
  },

  transforms: {
    second_transform_B: {
      module: "decisionengine.framework.tests.DynamicTransform",
      parameters: {
        consumes: ["a", "_b2"],
        data_product_name: "b2",
      },
    },
  },

  publishers: {
    second_publisher_B: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["a", "b2"],  // Include 'a' again in the sum to distinguish this channel from secondA
        expects: 3,
      },
    },
  },
}
