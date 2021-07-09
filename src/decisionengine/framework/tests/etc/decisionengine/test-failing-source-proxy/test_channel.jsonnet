{
  "sources": {
    "source1": {
      "module": "decisionengine.framework.tests.SourceNOP",
      "name": "SourceNOP",
      "parameters": {
        "sleep_for": 5
      },
      "schedule": 1
    }
  },

  "transforms": {
    "transform1": {
      "module": "decisionengine.framework.tests.TransformNOP",
      "name": "TransformNOP",
      "parameters": {},
      "schedule": 1
    }
  },

  "logicengines": {},
  "publishers": {}
}
