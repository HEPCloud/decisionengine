# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pandas as pd

from prometheus_client import Gauge

from decisionengine.framework.modules import Source

sourcenop_test_values = Gauge("sourcenop_test_values", "Test metric", labelnames=["key1"], multiprocess_mode="liveall")


@Source.produces(foo=pd.DataFrame)
class SourceNOP(Source.Source):
    def __init__(self, config):
        super().__init__(config)

    def acquire(self):
        result = {
            "foo": pd.DataFrame(
                [
                    {"key1": "value1", "key2": 0.1},
                    {"key1": "value2", "key2": 2},
                    {"key1": "value3", "key2": "Test"},
                ]
            )
        }
        for _, row in result["foo"].iterrows():
            if isinstance(row["key2"], (float, int)):
                sourcenop_test_values.labels(row["key1"]).set(row["key2"])

        return result


Source.describe(SourceNOP)
