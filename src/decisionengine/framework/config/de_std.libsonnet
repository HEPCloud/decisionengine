// These utilities combine channel configurations.  Consider the
// following configurations.
//
// # A.libsonnet
// {
//   sources: {
//     a1: { ... }
//     a2: { parameters: { source_channel: ... }, ... }
//   }
// }
//
// # B.libsonnet
// {
//   sources: {
//     b: { ... }
//   }
// }
//
// They can be combined via the following configuration:
//
// # Final.jsonnet
//
// local de_std = import 'de_std.libjsonnet';
// local channels = [import 'A.libsonnet', import 'B.libsonnet'];
// {
//   sources: de_std.sources_from(channels)
// }
//
// The final Jsonnet-preprocessed configuration would look like:
//
// {
//   sources: {
//     a1: { ... },
//     b: { ... }
//   }
// }
//
// Note that the 'a2' source has not been included as the
// 'sources_from' helper utility skips over any sources that contain
// the field 'source_channel' in the nested 'parameters' table.

local append(res, block, skip_if="") =
  local current_keys = std.objectFields(res);
  local new_keys = std.objectFields(block);
  local duplicate_keys = std.setInter(current_keys, new_keys);
  if std.length(duplicate_keys) != 0 then
    error "The following duplicate keys have been detected: " + std.toString(duplicate_keys)
  else
    res + {
      [k]: block[k]
      for k in new_keys
      if skip_if == "" || !std.objectHas(block[k].parameters, skip_if)
    };

local gather_from(arr, field, skip_if) =
  std.foldl(function(res, config) append(res, config[field], skip_if), arr, {});

{
  sources_from(arr): gather_from(arr, "sources", skip_if="source_channel"),
  publishers_from(arr): gather_from(arr, "publishers"),
  transforms_from(arr): gather_from(arr, "transforms"),
}
