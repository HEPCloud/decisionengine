#!/usr/bin/env python3
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
import os
import pwd
import sys
from decisionengine.framework.config import policies, ValidConfig
import decisionengine.framework.dataspace.dataspace as dataspace

if __name__ == "__main__":
    username = pwd.getpwuid(os.getuid()).pw_name
    if username not in ['root', 'decisionengine']:
        sys.exit(f"User '{username}' is not allowed to run this script.")

    config_file = policies.global_config_filename()
    global_config = ValidConfig.ValidConfig(config_file)
    reaper = dataspace.Reaper(global_config)
    reaper.reap()
