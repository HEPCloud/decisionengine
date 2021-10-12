local de_std = import "de_std.libsonnet";
local default = import "parameters.libsonnet";
local channels = [
  import "B1_source_proxy.libsonnet",
  import "B2_source_proxy.libsonnet",
];

{
  test: {
    sources: de_std.sources_from(channels),
  },
  reference: {
    sources: {
      s_b1: default.config,
      s_b2: default.config,
    },
  },
}
