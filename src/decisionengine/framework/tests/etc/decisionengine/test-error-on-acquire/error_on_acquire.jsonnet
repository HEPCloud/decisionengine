// The ErrorOnAcquire source raises an exception as part of the acquire
// method.  We then specify a ridiculous schedule of 10k seconds, to
// test that the task manager does not wait 10k seconds before taking
// the channel offline.

{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.ErrorOnAcquire",
      parameters: {},
      schedule: 20,
    },
    source2: {
      module: "decisionengine.framework.tests.SourceNOP",
      parameters: {},
      schedule: 10,
    },
  },
  transforms: {},
  publishers: {},
}
