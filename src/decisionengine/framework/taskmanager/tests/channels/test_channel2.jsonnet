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
  "publishers": {
    "publisher1": {
      "module": "decisionengine.framework.tests.PublisherNOP",
      "parameters": {}
    }
  }
}
