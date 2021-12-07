# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import abc

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME


class DataSource(metaclass=abc.ABCMeta):  # pragma: no cover

    #: Name of the taskmanager table
    taskmanager_table = "taskmanager"

    #: Name of the dataproduct table
    dataproduct_table = "dataproduct"

    #: Name of the header table
    header_table = "header"

    #: Name of the metadata table
    metadata_table = "metadata"

    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """

        self.config = config
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)
        self.logger.debug("Initializing a datasource")

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def __str__(self):  # pragma: no cover
        return f"{vars(self)}"

    @abc.abstractmethod
    def get_schema(self, table=None):
        """
        Given the table name return it's schema

        :type table: :obj:`string`
        :arg table: Name of the table
        """
        self.logger.info("getting the datasource schema")

        schemas = {
            "taskmanager": [
                "sequence_id INT",
                "taskmanager_id TEXT",
                "name TEXT",
                "datestamp timestamp with timezone",
            ],
            "header": [
                "taskmanager_id INT",
                "generation_id INT",
                "key TEXT",
                "create_time REAL",
                "expiration_time REAL",
                "scheduled_create_time REAL",
                "creator TEXT",
                "schema_id INT",
            ],
            "schema": [
                "schema_id INT",  # Auto generated
                "schema BLOB",  # keys in the value dict of the dataproduct table
            ],
            "metadata": [
                "taskmanager_id INT",
                "generation_id INT",
                "key TEXT",
                "state TEXT",
                "generation_time REAL",
                "missed_update_count INT",
            ],
            "dataproduct": ["taskmanager_id INT", "generation_id INT", "key TEXT", "value BLOB"],
        }

        if table:
            return {table: schemas.get(table)}
        return schemas

    @abc.abstractmethod
    def connect(self):
        """
        Create a pool of database connections
        """
        self.logger.info("datasource is creating the database connections")
        return

    @abc.abstractmethod
    def reset_connections(self):
        """
        Drop any cached connections and reconnect to the database
        """
        self.logger.info("datasource is resetting database the connections")
        return

    @abc.abstractmethod
    def create_tables(self):
        """
        Create database tables
        """
        self.logger.info("datasource is creating the database tables")
        return

    @abc.abstractmethod
    def insert(self, taskmanager_id, generation_id, key, value, header, metadata):
        """
        Insert data into respective tables for the given
        taskmanager_id, generation_id, key

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type key: :obj:`string`
        :arg key: key for the value
        :type value: :obj:`object`
        :arg value: Value can be an object or dict
        :type header: :obj:`~datablock.Header`
        :arg header: Header for the value
        :type metadata: :obj:`~datablock.Metadata`
        :arg header: Metadata for the value
        """
        self.logger.info("datasource is inserting data into the database tables")
        return

    @abc.abstractmethod
    def update(self, taskmanager_id, generation_id, key, value, header, metadata):
        """
        Update the data in respective tables for the given
        taskmanager_id, generation_id, key

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type key: :obj:`string`
        :arg key: key for the value
        :type value: :obj:`object`
        :arg value: Value can be an object or dict
        :type header: :obj:`~datablock.Header`
        :arg header: Header for the value
        :type metadata: :obj:`~datablock.Metadata`
        :arg header: Metadata for the value
        """
        self.logger.info("datasource is updating data in the database tables")
        return

    @abc.abstractmethod
    def get_dataproduct(self, taskmanager_id, generation_id, key):
        """
        Return the data from the dataproduct table for the given
        taskmanager_id, generation_id, key

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type key: :obj:`string`
        :arg key: key for the value
        """
        self.logger.info("datasource is getting a dataproduct for a taskmanger")
        return

    @abc.abstractmethod
    def get_dataproducts(self, taskmanager_id, key):
        """
        Return list of all data products associated with
        with taskmanager_id

        :type taskmanager_id: :obj:`string`
        :type key: :obj:`string`
        :arg key: data product key
        """
        self.logger.info("datasource is getting all dataproducts for a taskmanger")
        return

    @abc.abstractmethod
    def get_header(self, taskmanager_id, generation_id, key):
        """
        Return the header from the header table for the given
        taskmanager_id, generation_id, key

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type key: :obj:`string`
        :arg key: key for the value
        """
        self.logger.info("datasource is getting the header for a taskmanger")
        return

    @abc.abstractmethod
    def get_metadata(self, taskmanager_id, generation_id, key):
        """
        Return the metadata from the metadata table for the given
        taskmanager_id, generation_id, key

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type key: :obj:`string`
        :arg key: key for the value
        """
        self.logger.info("datasource is getting the metadata for a taskmanger")
        return

    @abc.abstractmethod
    def get_datablock(self, taskmanager_id, generation_id):
        """
        Return the entire datablock from the dataproduct table for the given
        taskmanager_id, generation_id

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        """
        self.logger.info("datasource is getting the datablock for a taskmanger")
        return

    @abc.abstractmethod
    def duplicate_datablock(self, taskmanager_id, generation_id, new_generation_id):
        """
        For the given taskmanager_id, make a copy of the datablock with given
        generation_id, set the generation_id for the datablock copy

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        :type generation_id: :obj:`int`
        :arg generation_id: generation_id of the data
        :type new_generation_id: :obj:`int`
        :arg new_generation_id: generation_id of the new datablock created
        """
        self.logger.info("datasource is duplicating a datablock for a taskmanger")
        return

    @abc.abstractmethod
    def get_last_generation_id(self, taskmanager_name, taskmanager_id=None):
        """
        Return last generation id for current task manager
        or taskmanager w/ task_manager_id.

        :type taskmanager_name: :obj:`string`
        :arg taskmanager_name: task manager name
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: task manager id
        """
        self.logger.info("datasource is getting the last generation id for a taskmanager")
        return

    @abc.abstractmethod
    def close(self):
        """
        Close all connections to the database
        """
        self.logger.info("datasource is closing database connections")
        return

    @abc.abstractmethod
    def store_taskmanager(self, taskmanager_name, taskmanager_id, datestamp=None):
        """
        Store TaskManager
        :type taskmanager_name: :obj:`string`
        :arg taskmanager_name: name of taskmanager to retrieve
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: id of taskmanager to retrieve
        :type datestamp: :obj:`datetime`
        :arg datestamp: datetime of created object, defaults to 'now'
        """
        self.logger.info("datasource is storing a taskmanager")
        return

    @abc.abstractmethod
    def get_taskmanagers(self, taskmanager_name=None, start_time=None, end_time=None):
        """
        Retrieve TaskManagers
        :type taskmanager_name: :obj:`string`
        :arg taskmanager_name: name of taskmanager to retrieve
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: id of taskmanager to retrieve
        """
        self.logger.info("datasource is getting all taskmanagers")
        return

    @abc.abstractmethod
    def get_taskmanager(self, taskmanager_name, taskmanager_id):
        """
        Retrieve TaskManager
        :type taskmanager_name: :obj:`string`
        :arg taskmanager_name: name of taskmanager to retrieve
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: id of taskmanager to retrieve
        """
        self.logger.info("datasource is getting a taskmanager")
        return

    @abc.abstractmethod
    def delete_data_older_than(self, days):
        """
        Delete data older that interval
        :type days: :obj:`long`
        :arg days: remove data older than interval
        """
        self.logger.info("datasource is deleting data")
        return
