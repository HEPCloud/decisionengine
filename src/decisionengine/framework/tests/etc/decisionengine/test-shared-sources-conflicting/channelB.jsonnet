{
  sources: {
    source: {
      # The actual module doesn't matter as this test just verifies
      # that a shared source must have identical configurations across
      # channels.
      module: "decisionengine.framework.tests.ErrorOnAcquire",
      parameters: {},
    },
  },
  transforms: {},
  publishers: {},
}
