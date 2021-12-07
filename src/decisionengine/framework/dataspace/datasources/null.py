# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import decisionengine.framework.dataspace.datasource as ds


class NullDataSource(ds.DataSource):  # pragma: no cover
    """
    Implementation of data source ABC that does nothing
    """

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.logger.debug("Initializing a null datasource")

    def create_tables(self):
        super().create_tables()

    def store_taskmanager(self, name, taskmanager_id, datestamp=None):
        super().store_taskmanager(name, taskmanager_id, datestamp)

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        super().get_taskmanager(taskmanager_name, taskmanager_id)

    def get_taskmanagers(self, taskmanager_name=None, start_time=None, end_time=None):
        super().get_taskmanagers(taskmanager_name, start_time, end_time)

    def get_last_generation_id(self, taskmanager_name, taskmanager_id=None):
        super().get_last_generation_id(taskmanager_name, taskmanager_id)

    def insert(self, taskmanager_id, generation_id, key, value, header, metadata):
        super().insert(taskmanager_id, generation_id, key, value, header, metadata)

    def update(self, taskmanager_id, generation_id, key, value, header, metadata):
        super().update(taskmanager_id, generation_id, key, value, header, metadata)

    def get_header(self, taskmanager_id, generation_id, key):
        super().get_header(taskmanager_id, generation_id, key)

    def get_metadata(self, taskmanager_id, generation_id, key):
        super().get_metadata(taskmanager_id, generation_id, key)

    def get_dataproducts(self, taskmanager_id, key=None):
        super().get_dataproducts(taskmanager_id, key)

    def get_dataproduct(self, taskmanager_id, generation_id, key):
        super().get_dataproduct(taskmanager_id, generation_id, key)

    def get_datablock(self, taskmanager_id, generation_id):
        super().get_datablock(taskmanager_id, generation_id)

    def duplicate_datablock(self, taskmanager_id, generation_id, new_generation_id):
        super().duplicate_datablock(taskmanager_id, generation_id, new_generation_id)

    def delete_data_older_than(self, days):
        super().delete_data_older_than(days)

    def close(self):
        super().close()

    def connect(self):
        super().connect()

    def reset_connections(self):
        super().reset_connections()

    def get_schema(self, table=None):
        super().get_schema(table)
