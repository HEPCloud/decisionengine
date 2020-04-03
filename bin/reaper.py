"""
A stand-alone script purges data in database older than specified
in configuration. Configuration file has to have this bit added:
   {
     "dataspace" : { "retention_interval_in_days" : 365,
                      "datasource" :  { ... }
                   }
    }
Can be used in a cron job.
"""
import decisionengine.framework.configmanager.ConfigManager as config
import decisionengine.framework.dataspace.dataspace as dataspace

if __name__ == "__main__":
    conf_manager = config.ConfigManager()
    conf_manager.load()
    reaper = dataspace.Reaper(conf_manager.get_global_config())
    reaper.reap()
