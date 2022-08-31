#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
A stand-alone script purges data in database older than specified
in configuration. Configuration file has to have this bit added:

    .. code-block:: json

        {
            "dataspace" : {
                "retention_interval_in_days" : 365,
                "datasource" :  {}
            }
        }

Can be used in a cron job.
"""
import os
import pwd
import sys

import decisionengine.framework.config.policies as policies

from decisionengine.framework.config.ValidConfig import ValidConfig
from decisionengine.framework.dataspace.maintain import Reaper


def main():  # pragma: no cover
    username = pwd.getpwuid(os.getuid()).pw_name
    if username not in ["root", "decisionengine"]:
        sys.exit(f"User '{username}' is not allowed to run this script.")

    config_file = policies.global_config_file()
    global_config = ValidConfig(config_file)
    reaper = Reaper(global_config)
    reaper.reap()


if __name__ == "__main__":
    main()
