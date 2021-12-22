local de_std = import "de_std.libsonnet";
local channels = [
  import "first.libsonnet",
];

{
  sources: de_std.sources_from(channels) {
    second_source_A: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "_b1",
      },
      schedule: 5,
    },
  },
  transforms: de_std.transforms_from(channels) {
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
