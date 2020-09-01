{

  "sources": {
    "source1": {
      "module": "decisionengine.framework.modules.SourceNOP",
      "name": "SourceNOP",
      "parameters": { },
      "schedule": 5,
     }
   },

   "transforms": {
     "transform1": {
       "module": "decisionengine.framework.modules.TransformNOP",
       "name" : "TransformNOP",
       "parameters": { },
       "schedule": 5,
     },
   },

   "publishers": {
     "publisher1": {
       "module": "decisionengine.framework.modules.PublisherNOP",
       "name" : "PublisherNOP",
       "parameters": { },
       "schedule": 5,
     },
   },

  "logicengines" : {
      "logicengine1" : {
          "module" : "framework.logicengine.LogicEngine",
          "name" : "LogicEngine",
          "parameters" : { }
       }
   }
}
