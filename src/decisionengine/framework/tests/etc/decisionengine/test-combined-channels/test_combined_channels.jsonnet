local de_std = import "de_std.libsonnet";
local channels = [import "source_channel.libsonnet"];

{
  sources: de_std.sources_from(channels),
  transforms: de_std.transforms_from(channels),
  publishers: {
    pub1: {
      module: "decisionengine.framework.tests.WriteToDisk",
      parameters: {
        consumes: ["foo"],
      },
    },
  },
}
