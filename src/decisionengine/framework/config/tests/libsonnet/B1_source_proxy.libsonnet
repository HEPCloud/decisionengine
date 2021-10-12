local default = import "parameters.libsonnet";

{
  sources: {
    s_b1: default.config,
    source_proxy: {
      parameters: {
        source_channel: "B0",
      },
    },
  },
}
