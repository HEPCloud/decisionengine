"""
Fill in data from another channel data block
"""
import time

from typing import Any

import pandas as pd

import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.dataspace.dataspace as dataspace

from decisionengine.framework.modules import Source
from decisionengine.framework.modules.Source import Parameter
from decisionengine.framework.modules.translate_product_name import translate_all

MAX_ATTEMPTS = 10
RETRY_INTERVAL = 60
must_have = ("source_channel", "Dataproducts")


@Source.supports_config(
    Parameter("source_channel", type=str, comment="Channel from which to retrieve data products."),
    Parameter("Dataproducts", type=list, comment="List of data products to retrieve."),
    Parameter("max_attempts", default=MAX_ATTEMPTS, comment="Number of attempts allowed to fetch products."),
    Parameter("retry_interval", default=RETRY_INTERVAL, comment="Number of seconds to wait between retries."),
)
class SourceProxy(Source.Source):
    def __init__(self, config):
        super().__init__(config)
        if not set(must_have).issubset(set(config.keys())):
            raise RuntimeError(f"SourceProxy misconfigured. Must have {must_have} defined")
        self.source_channel = config["source_channel"]
        self.data_keys = translate_all(config["Dataproducts"])
        self.max_attempts = config.get("max_attempts", MAX_ATTEMPTS)
        self.retry_interval = config.get("retry_interval", RETRY_INTERVAL)

        # Hack - it is possible for a subclass to declare @produces,
        #        in which case, we do not want to override that.
        if not self._produces:
            self._produces = {new_name: Any for new_name in self.data_keys.values()}

    def post_create(self, global_config):
        self.dataspace = dataspace.DataSpace(global_config)

    def _get_data(self, data_block, key):
        while True:
            try:
                data = data_block.get(key)
                break
            except KeyError as ke:
                if data_block.generation_id > 1:
                    data_block.generation_id -= 1
                else:
                    raise KeyError(ke)
        return data

    def acquire(self):
        """
        Overrides Source class method
        """
        data_block = None
        for _ in range(self.max_attempts):
            try:
                tm = self.dataspace.get_taskmanager(self.source_channel)
                self.logger.debug("task manager %s", tm)
                if tm["taskmanager_id"]:
                    # get last datablock
                    data_block = datablock.DataBlock(
                        self.dataspace,
                        self.source_channel,
                        taskmanager_id=tm["taskmanager_id"],
                        sequence_id=tm["sequence_id"],
                    )
                    self.logger.debug("data block %s", data_block)
                    if data_block and data_block.generation_id:
                        self.logger.debug("DATABLOCK %s", data_block)
                        # This is a valid datablock
                        break
            except Exception as detail:
                self.logger.error("Error getting datablock for %s %s", self.source_channel, detail)

            time.sleep(self.retry_interval)

        if not data_block:
            raise RuntimeError("Could not get data.")

        rc = {}
        filled_keys = []
        for _ in range(self.max_attempts):
            if len(filled_keys) != len(self.data_keys):
                for k_in, k_out in self.data_keys.items():
                    if k_in not in filled_keys:
                        try:
                            rc[k_out] = pd.DataFrame(self._get_data(data_block, k_in))
                            filled_keys.append(k_in)
                        except KeyError as ke:
                            self.logger.debug("KEYERROR %s", ke)
            if len(filled_keys) == len(self.data_keys):
                break
            # expected data is not ready yet
            time.sleep(self.retry_interval)

        if len(filled_keys) != len(self.data_keys):
            raise RuntimeError(f"Could not get all data. Expected {self.data_keys} Filled {filled_keys}")
        return rc
