local de_std = import 'de_std.libsonnet';
local channels = [import 'A1.libsonnet', import 'A1.libsonnet'];

{
  sources: de_std.sources_from(channels)
}
