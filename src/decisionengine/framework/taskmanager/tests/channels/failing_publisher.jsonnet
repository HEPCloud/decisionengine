{
  sources: {
    source1: {
      module: "decisionengine.framework.tests.SourceNOP",
      name: "SourceNOP",
      parameters: {},
      schedule: 1,
     }
   },

  transforms: {
    bar_maker: {
      module: "decisionengine.framework.tests.TransformNOP",
      name: "TransformNOP",
      parameters: {}
    }
  },
  logicengines: {
    le: {
      module: "decisionengine.framework.logicengine.LogicEngine",
      name: 'LogicEngine',
      parameters: {
        facts: {
          pass_all: "(True)"
        },
        rules: {
          r1: {
            expression: 'pass_all',
            actions: ['fail']
          }
        }
      }
    }
  },
  publishers: {
    fail: {
      module: "decisionengine.framework.tests.FailingPublisher",
      name: "FailingPublisher",
      parameters: {}
    }
  }
}
