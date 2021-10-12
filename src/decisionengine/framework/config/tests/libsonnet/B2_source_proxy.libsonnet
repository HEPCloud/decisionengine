local default = import "parameters.libsonnet";

{
  sources: {
    s_b2: default.config,
    source_proxy: {
      parameters: {
        source_channel: "B0",
      },
    },
  },
}
