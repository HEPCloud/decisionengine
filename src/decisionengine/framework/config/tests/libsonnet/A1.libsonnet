local default = import "parameters.libsonnet";

{
  sources: {
    s1_a1: default.config,
    s2_a1: default.config,
  },
  transforms: {
    t_a1: default.config,
  },
}
