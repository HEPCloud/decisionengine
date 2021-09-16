{
  sources: {
    first_source: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "_a",
      },
      schedule: 10,
    },
  },

  transforms: {
    first_transform: {
      module: "decisionengine.framework.tests.DynamicTransform",
      parameters: {
        consumes: ["_a"],
        data_product_name: "a",
      },
    },
  },

  publishers: {
    pub: {
      module: "decisionengine.framework.tests.DynamicPublisher",
      parameters: {
        consumes: ["a"],
        expects: 1,
      },
    },
  },
}
