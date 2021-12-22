local de_std = import "de_std.libsonnet";
local channels = [
  import "first.libsonnet",
  import "secondA.libsonnet",
  import "secondB.libsonnet",
  import "secondC.libsonnet",
];

{
  sources: de_std.sources_from(channels) {
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

  transforms: de_std.transforms_from(channels) {
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

  publishers: de_std.publishers_from(channels) {
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
