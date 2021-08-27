{
  "channel_name": "name_in_config",
  "sources": {
    "source1": {
      "module": "decisionengine.framework.tests.SourceNOP",
      "parameters": {},
      "schedule": 1
    }
  },
  "transforms": {
    "transform1": {
      "module": "decisionengine.framework.tests.TransformNOP",
      "parameters": {},
      "schedule": 1
    }
  },
  "logicengines": {
    "le1": {
      "module": "decisionengine.framework.logicengine.LogicEngine",
      "parameters": {
        "facts": {
          "pass_all": "True"
        },
        "rules": {
          "r1": {
            "expression": "pass_all",
            "actions": ["publisher1"]
          }
        }
      }
    }
  },
  "publishers": {
    "publisher1": {
      "module": "decisionengine.framework.tests.PublisherNOP",
      "parameters": {}
    }
  }
}
