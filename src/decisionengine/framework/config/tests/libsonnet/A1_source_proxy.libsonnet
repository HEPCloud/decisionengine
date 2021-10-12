local default = import "parameters.libsonnet";

{
  sources: {
    s1_a1: default.config,
    s2_a1: default.config,
    s3_a1: {
      parameters: {
        source_channel: "A0",
      },
    },
  },
  transforms: {
    t_a1: default.config,
  },
}
