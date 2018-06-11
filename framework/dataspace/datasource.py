#!/usr/bin/python

import abc


class DataSource(object):

    __metaclass__ = abc.ABCMeta

    #: Name of the taskmanager table
    taskmanager_table = 'taskmanager'

    #: Name of the dataproduct table
    dataproduct_table = 'dataproduct'

    #: Name of the header table
    header_table = 'header'

    #: Name of the metadata table
    metadata_table = 'metadata'


    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """

        self.config = config


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return '%s' % vars(self)


    @abc.abstractmethod
    def get_schema(self, table=None):
        """
        Given the table name return it's schema

        :type table: :obj:`string`
        :arg table: Name of the table
        """

        schemas = {
            'taskmanager': [
                'sequence_id INT',
                'taskmanager_id TEXT',
                'name TEXT',
                'datestamp timestamp with timezone',
            ],
            'header': [
                'taskmanager_id INT',
                'generation_id INT',
                'key TEXT',
                'create_time REAL',
                'expiration_time REAL',
                'scheduled_create_time REAL',
                'creator TEXT',
                'schema_id INT',
            ],
            'schema': [
                'schema_id INT', # Auto generated
                'schema BLOB',   # keys in the value dict of the dataproduct table
            ],
            'metadata': [
                'taskmanager_id INT',
                'generation_id INT',
                'key TEXT',
                'state TEXT',
                'generation_time REAL',
                'missed_update_count INT',
            ],
            'dataproduct': [
                'taskmanager_id INT',
                'generation_id INT',
                'key TEXT',
                'value BLOB'
            ]
        }

        if table:
            return {table: schemas.get(table)}
        return schemas


    @abc.abstractmethod
    def connect(self):
        """
        Create a pool of database connections
        """
        return

    @abc.abstractmethod
    def create_tables(self):
        """
        Create database tables
        """
        return


    @abc.abstractmethod
    def insert(self, taskmanager_id, generation_id, key,
               value, header, metadata):
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
        return


    @abc.abstractmethod
    def update(self, taskmanager_id, generation_id, key,
               value, header, metadata):
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
        return


    @abc.abstractmethod
    def duplicate_datablock(self, taskmanager_id, generation_id,
                            new_generation_id):
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
        return

    @abc.abstractmethod
    def get_last_generation_id(self, name, taskmanager_id=None):
        """
        Return last generation id for current task manager
        or taskmanager w/ task_manager_id.

        :type name: :obj:`string`
        :arg name: task manager name
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: task manager id
        """
        return

    @abc.abstractmethod
    def close(self):
        """
        Close all connections to the database
        """
        return

    @abc.abstractmethod
    def store_taskmanager(self, taskmanager_name, taskmanager_id):
        """
        Store TaskManager
        :type taskmanager_name: :obj:`string`
        :arg taskmanager_name: name of taskmanager to retrieve
        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: id of taskmanager to retrieve
        """
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
        return
