local default = import "parameters.libsonnet";

{
  sources: {
    s1_a1: default.config {
      parameters: {
        a: 4
      },
    },
  },
}
