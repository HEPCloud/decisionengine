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
     transform1: {
       module: "decisionengine.framework.tests.TransformNOP",
       name : "TransformNOP",
       parameters: {},
       schedule: 1
     }
   },
  logicengines: {
    "logicengine1": {
      "module": "decisionengine.framework.logicengine.LogicEngine",
      "name": "LogicEngine",
      "parameters": {
        "rules": {
          "publish_nersc_fom": {
            "expression": "(foo)",
            "actions": [
              "PublisherNOP"
            ],
            "facts": [
              "foo"
            ]
          }
        },
        "facts": {
          "foo": "(True)"
        }
      }
    }
  },
  publishers: {
    PublisherNOP: {
      module: "decisionengine.framework.tests.PublisherNOP",
      name : "PublisherNOP",
      parameters: {},
      schedule: 1
    }
  },
}
