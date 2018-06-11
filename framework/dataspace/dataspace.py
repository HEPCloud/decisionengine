#!/usr/bin/python

import os
import sqlite3
import traceback
import copy
import ast
import importlib

#from UserDict import UserDict
# TODO: Schema definations and validation and updations


class DataSpaceConfigurationError(Exception):
    """
    Errors related to database access
    """
    pass


class DataSpaceConnectionError(Exception):
    """
    Errors related to database access
    """
    pass


class DataSpaceError(Exception):
    """
    Errors related to database access
    """
    pass


class DataSpaceExistsError(Exception):
    """
    Errors related to database access
    """
    pass


class Singleton(type):
    """
    Singleton pattern using Metaclass
    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        # Uncomment following to run __init__ everytime class is called
        # else:
        #     cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]


class DataSourceLoader(object):

    __metaclass__ = Singleton

    _ds = None

    @staticmethod
    def create_datasource(module_name, class_name, config):
        ds = DataSourceLoader._ds
        #print module_name, class_name
        if not ds:
            py_module = importlib.import_module(module_name)
            clazz = getattr(py_module, class_name)
            ds = clazz(config)
        return ds


class DataSpace(object):
    """
    DataSpace class is collection of datablocks and provides interface
    to the database used to store the actual data
    """

    #: Description of tables and their columns
    _tables_created = False

    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """

        # Validate configuration
        if not config.get('dataspace'):
            raise DataSpaceConfigurationError('Configuration is missing dataspace information')
        elif not isinstance(config.get('dataspace'), dict):
            raise DataSpaceConfigurationError('Invalid dataspace configuration')
        try:
            self._db_driver_name = config['dataspace']['datasource']['name']
            self._db_driver_module = config['dataspace']['datasource']['module']
            self._db_driver_config = config['dataspace']['datasource']['config']
        except KeyError, e:
            raise DataSpaceConfigurationError('Invalid dataspace configuration')

        self.datasource = DataSourceLoader().create_datasource(self._db_driver_module,
                                                               self._db_driver_name,
                                                               self._db_driver_config)

        # Datablocks, current and previous, keyed by taskmanager_ids
        self.curr_datablocks = {}
        self.prev_datablocks = {}

        # Connect to the database
        self.datasource.connect()

        # Create tables if not created
        if not DataSpace._tables_created:
            self.datasource.create_tables()
            DataSpace._tables_created = True

    def __str__(self):
        return '%s' % vars(self)


    def insert(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        self.datasource.insert(taskmanager_id, generation_id, key,
                               value, header, metadata)


    def update(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        self.datasource.update(taskmanager_id, generation_id, key,
                               value, header, metadata)


    def get_dataproduct(self, taskmanager_id, generation_id, key):
        return self.datasource.get_dataproduct(taskmanager_id, generation_id, key)


    def get_header(self, taskmanager_id, generation_id, key):
        return self.datasource.get_header(taskmanager_id, generation_id, key)


    def get_metadata(self, taskmanager_id, generation_id, key):
        return self.datasource.get_metadata(taskmanager_id, generation_id, key)


    def duplicate_datablock(self, taskmanager_id, generation_id,
                            new_generation_id):
        return self.datasource.duplicate_datablock(taskmanager_id, generation_id,
                                                   new_generation_id)


    def delete(self, taskmanager_id, all_generations=False):
        # Remove the latest generation of the datablock
        # If asked, remove all generations of the datablock
        pass


    def mark_expired(self, taskmanager_id, generation_id, key, expiry_time):
        pass


    def mark_demented(self, taskmanager_id, keys, generation_id=None):
        if not generation_id:
            generation_id = self.curr_datablocks[taskmanager_id].generation_id
        self.datasource.mark_demented(taskmanager_id, generation_id, keys)


    def close(self):
        self.datasource.close()

    def store_taskmanager(self, name, id):
        return self.datasource.store_taskmanager(name, id)

    def get_last_generation_id(self,
                               taskmanager_name,
                               taskmanager_id=None):
        return self.datasource.get_last_generation_id(taskmanager_name,
                                                      taskmanager_id)

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        return self.datasource.get_taskmanager(taskmanager_name, taskmanager_id)
