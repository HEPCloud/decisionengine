#!/usr/bin/python

import os
import sqlite3
import traceback
import copy
import ast
import decisionengine.framework.dataspace.datasource

#from UserDict import UserDict
# TODO: Schema definations and validation and updations


class SQLite3DB(decisionengine.framework.dataspace.datasource.DataSource):
    """
    SQLite3DB class provides interface to the database used to store the data
    """

    # Internal variable to inform if the database tables have been created
    _tables_created = False

    #: Description of tables and their columns
    tables = {
        'header': [
            'taskmanager_id TEXT',
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
            'taskmanager_id TEXT',
            'generation_id INT',
            'key TEXT',
            'state TEXT',
            'generation_time REAL',
            'missed_update_count INT',
        ],
        'dataproduct': [
            'taskmanager_id TEXT',
            'generation_id INT',
            'key TEXT',
            'value BLOB'
        ]
    }

    #: Name of the dataproduct table
    #dataproduct_table = 'dataproduct'

    #: Name of the header table
    #header_table = 'header'

    #: Name of the metadata table
    #metadata_table = 'metadata'


    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary

        TODO: Change a single connection to the database to a connection pool
        """

        self.db_filename = config['filename']

        if os.path.exists(self.db_filename):
            os.unlink(self.db_filename)

        self.connect()


    def get_schema(self, table=None):
        """
        Given the table name return it's schema

        :type table: :obj:`string`
        :arg table: Name of the table
        """

        schemas = {
            'header': [
                'taskmanager_id TEXT',
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
                'taskmanager_id TEXT',
                'generation_id INT',
                'key TEXT',
                'state TEXT',
                'generation_time REAL',
                'missed_update_count INT',
            ],
            'dataproduct': [
                'taskmanager_id TEXT',
                'generation_id INT',
                'key TEXT',
                'value BLOB'
            ]
        }

        if table:
            return {table: schemas.get(table)}
        return schemas


    def connect(self):
        print self.db_filename
        self.conn = sqlite3.connect(self.db_filename)


    def create_tables(self):
        """
        Create database tables for dataproduct, header and metadata

        TODO: Need to add functionality to ignore if tables exist
        """

        try:
            for table, cols in SQLite3DB.tables.iteritems():
                if isinstance(cols, list):
                    cmd = """CREATE TABLE %s (%s)""" % (table, ', '.join(str(c) for c in cols))
                    cursor = self.conn.cursor()
                    cursor.execute(cmd)
            self.conn.commit()
            SQLite3DB._tables_created = True
        except:
            raise


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

        # Insert the data product, header and metadata to the database
        try:
            # Insert value in the dataproduct table
            cmd = """INSERT INTO %s VALUES ("%s", %i, "%s", "%s")""" % (
                SQLite3DB.dataproduct_table, taskmanager_id, generation_id,
                key, value)
            cursor = self.conn.cursor()
            cursor.execute(cmd)
  
            # Insert header in the header table
            cmd = """INSERT INTO %s VALUES ("%s", %i, "%s", %f, %f, %f, "%s", "%s")""" % (
                SQLite3DB.header_table, taskmanager_id, generation_id,
                key, header.get('create_time'), header.get('expiration_time'),
                header.get('scheduled_create_time'), header.get('creator'),
                header.get('schema_id'))
            cursor = self.conn.cursor()
            cursor.execute(cmd)

            # Insert metadata in the metadata table
            cmd = """INSERT INTO %s VALUES ("%s", %i, "%s", "%s", %f, %i)""" % (
                SQLite3DB.metadata_table, taskmanager_id, generation_id,
                key, metadata.get('state'), metadata.get('generation_time'),
                metadata.get('missed_update_count'))
            cursor = self.conn.cursor()
            cursor.execute(cmd)

            # Commit data/header/metadata as a single transaction
            self.conn.commit()
        except:
            raise
            #traceback.print_stack()
            #raise db.DatabaseError('Error creating table %s' % SQLite3.dataproduct_table)


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

        # Update the data product, header and metadata in the database
        try:
            params = (taskmanager_id, generation_id, key)
            cmd = """UPDATE %s SET value="%s" WHERE ((taskmanager_id=?) AND (generation_id=?) AND (key=?))""" % (SQLite3DB.dataproduct_table, value)
            cursor = self.conn.cursor()
            cursor.execute(cmd, params)

            cmd = """UPDATE %s SET create_time=%f, expiration_time=%f, scheduled_create_time=%f, creator="%s", schema_id=%i WHERE ((taskmanager_id=?) AND (generation_id=?) AND (key=?))""" % (
                SQLite3DB.header_table,
                header.get('create_time'),
                header.get('expiration_time'),
                header.get('scheduled_create_time'),
                header.get('creator'), header.get('schema_id'))
            cursor = self.conn.cursor()
            cursor.execute(cmd, params)

            cmd = """UPDATE %s SET state="%s", generation_time=%f, missed_update_count=%i WHERE ((taskmanager_id=?) AND (generation_id=?) AND (key=?))""" % (
                SQLite3DB.metadata_table, metadata.get('state'),
                metadata.get('generation_time'),
                metadata.get('missed_update_count'))
            cursor = self.conn.cursor()
            cursor.execute(cmd, params)

            # Commit data/header/metadata as a single transaction
            self.conn.commit()
        except:
            raise
            #traceback.print_stack()
            #raise db.DatabaseError('Error updating table %s' % SQLite3.dataproduct_table)


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

        value = self._get_table_row(SQLite3DB.dataproduct_table, taskmanager_id,
                                    generation_id, key, ['value'])
        return value


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

        cols = [(x.split())[0] for x in SQLite3DB.tables.get(SQLite3DB.header_table)]
        return self._get_table_row(SQLite3DB.header_table, taskmanager_id,
                                   generation_id, key, cols)


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

        cols = [(x.split())[0] for x in SQLite3DB.tables.get(SQLite3DB.metadata_table)]
        return self._get_table_row(SQLite3DB.metadata_table, taskmanager_id,
                                   generation_id, key, cols)


    def get_datablock(self, taskmanager_id, generation_id):
        return {}


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

        cursor = self.conn.cursor()
        params = (taskmanager_id, generation_id)

        cmd = """INSERT INTO %s (taskmanager_id, generation_id, key, value) SELECT taskmanager_id, %i, key, value FROM %s WHERE (taskmanager_id=?) AND (generation_id=?)""" % (
            SQLite3DB.dataproduct_table, new_generation_id,
            SQLite3DB.dataproduct_table)
        cursor = self.conn.cursor()
        cursor.execute(cmd, params)

        cmd = """INSERT INTO %s (taskmanager_id, generation_id, key, create_time, expiration_time, scheduled_create_time, creator, schema_id) SELECT taskmanager_id, %i, key, create_time, expiration_time, scheduled_create_time, creator, schema_id FROM %s WHERE (taskmanager_id=?) AND (generation_id=?)""" % (
            SQLite3DB.header_table, new_generation_id,
            SQLite3DB.header_table)
        cursor = self.conn.cursor()
        cursor.execute(cmd, params)

        cmd = """INSERT INTO %s (taskmanager_id, generation_id, key, state, generation_time, missed_update_count) SELECT taskmanager_id, %i, key, state, generation_time, missed_update_count FROM %s WHERE (taskmanager_id=?) AND (generation_id=?)""" % (
            SQLite3DB.metadata_table, new_generation_id,
            SQLite3DB.metadata_table)
        cursor = self.conn.cursor()
        cursor.execute(cmd, params)

        self.conn.commit()


    def close(self):
        """Close all connections to the database"""
        self.conn.close()


    def delete(self, taskmanager_id, all_generations=False):
        # Remove the latest generation of the datablock
        # If asked, remove all generations of the datablock
        pass


    def get_last_generation_id(self, taskmanager_id):
        """
        Get the last known generation_id for the given taskmanager_id

        :type taskmanager_id: :obj:`string`
        :arg taskmanager_id: taskmanager_id for generation to be retrieved
        
        :rtype: :obj:`int`

        TODO: COALESCE is not safe. Find a better way check with DB experts
        """

        try:
            cmd = """SELECT COALESCE(MAX(generation_id),0) FROM %s""" % SQLite3DB.dataproduct_table

            cursor = self.conn.cursor()
            cursor.execute(cmd)
            value = cursor.fetchall()   
        except:
            raise
        return value[0][0]


    def _get_table_row(self, table, taskmanager_id,
                       generation_id, key, cols=None):
        # Get the data product from the database

        if not cols:
            cols = ['*']
        try:
            template = (taskmanager_id, generation_id, key)
            
            #print cmd
            cmd = """SELECT %s FROM %s WHERE ((taskmanager_id=?) AND (generation_id=?) AND (key=?))""" % (', '.join(str(c) for c in cols), table)
            params = (taskmanager_id, generation_id, key)

            cursor = self.conn.cursor()
            cursor.execute(cmd, params)
            value = cursor.fetchall()
        except:
            raise

        return value[-1]
