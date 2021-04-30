{
  sources: {},
  transforms: {
    a_uses_b: {
      module: 'decisionengine.framework.tests.ABTransform',
      name: 'ABTransform',
      parameters: {}
    },
    b_uses_a: {
      module: 'decisionengine.framework.tests.BATransform',
      name: 'BATransform',
      parameters: {}
    },
  },
  logicengines: {},
  publishers: {}
}
