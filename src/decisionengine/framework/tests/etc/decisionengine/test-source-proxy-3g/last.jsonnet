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
    from_secondA_channel: {
      module: "decisionengine.framework.modules.SourceProxy",
      parameters: {
        source_channel: "secondA",
        Dataproducts: ["b1"],
        max_attempts: 5,
        retry_interval: 10,
      },
      schedule: 1,
    },
    from_secondB_channel: {
      module: "decisionengine.framework.modules.SourceProxy",
      parameters: {
        source_channel: "secondB",
        Dataproducts: ["b2"],
        max_attempts: 5,
        retry_interval: 10,
      },
      schedule: 1,
    },
    from_secondC_channel: {
      module: "decisionengine.framework.modules.SourceProxy",
      parameters: {
        source_channel: "secondC",
        Dataproducts: ["b3"],
        max_attempts: 5,
        retry_interval: 10,
      },
      schedule: 1,
    },
    last_source_A: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "c1",
      },
      schedule: 5,
    },
    last_source_B: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "c2",
      },
      schedule: 5,
    },
  },

  transforms: {
    last_transform_A: {
      module: "decisionengine.framework.tests.DynamicTransform",
      parameters: {
        consumes: ["a", "b1", "b3", "c1"],
        data_product_name: "tA",
      },
    },
    last_transform_B: {
      module: "decisionengine.framework.tests.DynamicTransform",
      parameters: {
        consumes: ["a", "b2", "b3", "c2"],
        data_product_name: "tB",
      },
    },
  },

  publishers: {
    last_publisher: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["tA", "tB"],
        expects: 10,
      },
    },
    write_to_disk: {
      module: "decisionengine.framework.tests.WriteToDisk",
      parameters: {
        consumes: ["tA", "tB"],
      },
    },

  },
}
