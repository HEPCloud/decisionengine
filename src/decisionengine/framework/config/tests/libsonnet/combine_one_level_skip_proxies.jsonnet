local default = import 'parameters.libsonnet';
local de_std = import 'de_std.libsonnet';
local channels = [import 'A1_source_proxy.libsonnet', import 'A2.libsonnet', import 'A3.libsonnet'];

{
  test: {
    sources: de_std.sources_from(channels)
  },
  reference: {
    sources: {
      s1_a1: default.config,
      s2_a1: default.config,
      s_a2: default.config,
      s_a3: default.config
    }
  }
}
