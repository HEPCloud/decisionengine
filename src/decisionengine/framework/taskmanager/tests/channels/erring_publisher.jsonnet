{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.SourceNOP",
      parameters: {},
      schedule: 1,
    },
  },

  transforms: {
    bar_maker: {
      module: "decisionengine.framework.tests.TransformNOP",
      parameters: {},
    },
  },
  logicengines: {
    le: {
      module: "decisionengine.framework.logicengine.LogicEngine",
      parameters: {
        facts: {
          pass_all: "fail_on_error(True)",
        },
        rules: {
          r1: {
            expression: "pass_all",
            actions: ["fail"],
          },
        },
      },
    },
  },
  publishers: {
    fail: {
      module: "decisionengine.framework.tests.ErringPublisher",
      parameters: {},
    },
  },
}
