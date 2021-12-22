local de_std = import "de_std.libsonnet";
local channels = [
  import "first.libsonnet",
];

{
  sources: de_std.sources_from(channels) {
    second_source_B: {
      module: "decisionengine.framework.tests.DynamicSource",
      parameters: {
        data_product_name: "_b2",
      },
      schedule: 5,
    },
  },
  transforms: de_std.transforms_from(channels) {
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
