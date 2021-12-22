# Specify the same channel twice, testing duplicate keys with the same values.

local de_std = import "de_std.libsonnet";
local one_channel = [import "A1.libsonnet"];

{
  test: {
    sources: de_std.sources_from(one_channel + one_channel),
  },
  reference: {
    sources: de_std.sources_from(one_channel),
  },
}
