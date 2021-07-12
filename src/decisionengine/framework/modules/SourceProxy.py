"""
Fill in data from another channel data block
"""
import structlog
import time

import pandas as pd
from typing import Any

import decisionengine.framework.dataspace.datablock as datablock
import decisionengine.framework.dataspace.dataspace as dataspace
from decisionengine.framework.modules import Source
from decisionengine.framework.modules.Source import Parameter
from decisionengine.framework.modules.translate_product_name import translate_all
from decisionengine.framework.modules.de_logger import LOGGERNAME

RETRIES = 10
RETRY_TO = 60
must_have = ('channel_name', 'Dataproducts')


@Source.supports_config(Parameter('channel_name', type=str, comment="Channel from which to retrieve data products."),
                        Parameter('Dataproducts', type=list, comment="List of data products to retrieve."),
                        Parameter('retries', default=RETRIES, comment="Number of attempts allowed to fetch products."),
                        Parameter('retry_timeout', default=RETRY_TO, comment="Number of seconds to wait between retries."))
class SourceProxy(Source.Source):
    def __init__(self, config):
        if not set(must_have).issubset(set(config.keys())):
            raise RuntimeError(
                'SourceProxy misconfigured. Must have {} defined'.format(must_have))
        self.source_channel = config['channel_name']
        self.data_keys = translate_all(config['Dataproducts'])
        self.retries = config.get('retries', RETRIES)
        self.retry_to = config.get('retry_timeout', RETRY_TO)
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1])

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
        for _ in range(self.retries):
            try:
                tm = self.dataspace.get_taskmanager(self.source_channel)
                self.logger.debug('task manager %s', tm)
                if tm['taskmanager_id']:
                    # get last datablock
                    data_block = datablock.DataBlock(self.dataspace,
                                                     self.source_channel,
                                                     taskmanager_id=tm['taskmanager_id'],
                                                     sequence_id=tm['sequence_id'])
                    self.logger.debug('data block %s', data_block)
                    if data_block and data_block.generation_id:
                        self.logger.debug("DATABLOCK %s", data_block)
                        # This is a valid datablock
                        break
            except Exception as detail:
                self.logger.error(
                    'Error getting datablock for %s %s', self.source_channel, detail)

            time.sleep(self.retry_to)

        if not data_block:
            raise RuntimeError('Could not get data.')

        rc = {}
        filled_keys = []
        for _ in range(self.retries):
            if len(filled_keys) != len(self.data_keys):
                for k_in, k_out in self.data_keys.items():
                    if k_in not in filled_keys:
                        try:
                            rc[k_out] = pd.DataFrame(
                                self._get_data(data_block, k_in))
                            filled_keys.append(k_in)
                        except KeyError as ke:
                            self.logger.debug("KEYERROR %s", ke)
            if len(filled_keys) == len(self.data_keys):
                break
            # expected data is not ready yet
            time.sleep(self.retry_to)

        if len(filled_keys) != len(self.data_keys):
            raise RuntimeError('Could not get all data. Expected {} Filled {}'.format(
                self.data_keys, filled_keys))
        return rc
