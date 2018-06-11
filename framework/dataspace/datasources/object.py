#!/usr/bin/python

import os
import traceback
import copy
import ast
import importlib
import decisionengine.framework.dataspace.datasource


class ObjectDB(decisionengine.framework.dataspace.datasource.DataSource):

    _tables_created = False
    _tables = {}


    def __init__(self, config):
        decisionengine.framework.dataspace.datasource.DataSource.__init__(self, config)


    def __str__(self):
        return '%s' % ObjectDB._tables


    def _insert_or_update(self, taskmanager_id, generation_id, key,
                          value, header, metadata):
        row_id = (taskmanager_id, generation_id, key)

        ObjectDB._tables['dataproduct'][row_id] = '%s' % (value)
        ObjectDB._tables['header'][row_id] = '%s' % (header)
        ObjectDB._tables['metadata'][row_id] = '%s' % (metadata)


    def get_schema(self, table=None):
        schemas = {
            'header': [
                'taskmanager_id',
                'generation_id',
                'key',
                'create_time',
                'expiration_time',
                'scheduled_create_time',
                'creator',
                'schema_id',
            ],
            #'schema': [
            #    'schema_id INT', # Auto generated
            #    'schema BLOB',   # format of the value dict in dataproduct
            #],
            'metadata': [
                'taskmanager_id',
                'generation_id',
                'key',
                'state',
                'generation_time',
                'missed_update_count',
            ],
            'dataproduct': {
                'taskmanager_id',
                'generation_id',
                'key',
                'value'
            }
        }
        return schemas


    def connect(self):
        pass


    def create_tables(self):
        for table in self.get_schema():
            ObjectDB._tables[table] = {}
        ObjectDB._tables_created = True


    def insert(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        row_id = (taskmanager_id, generation_id, key)
        for tname in ObjectDB._tables:
            if (row_id in ObjectDB._tables[tname]):
                raise Exception('Invoking insert on existing existing row in table %s with row_id %s' % (tname, row_id))
        self._insert_or_update(taskmanager_id, generation_id, key,
                               value, header, metadata)


    def update(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        self._insert_or_update(taskmanager_id, generation_id, key,
                               value, header, metadata)


    def get_dataproduct(self, taskmanager_id, generation_id, key):
        return (ObjectDB._tables['dataproduct'][(taskmanager_id, generation_id, key)],)


    def get_header(self, taskmanager_id, generation_id, key):
        header = ast.literal_eval(ObjectDB._tables['header'][(taskmanager_id, generation_id, key)])
        return (taskmanager_id, generation_id, key,
                header['create_time'], header['expiration_time'],
                header['scheduled_create_time'], header['creator'],
                header['schema_id'])


    def get_metadata(self, taskmanager_id, generation_id, key):
        metadata = ast.literal_eval(ObjectDB._tables['metadata'][(taskmanager_id, generation_id, key)])
        return (taskmanager_id, generation_id, key,
                metadata['state'], metadata['generation_time'],
                metadata['missed_update_count'])


    def get_datablock(self, taskmanager_id, generation_id):
        return {k: v for (k, v) in ObjectDB._tables['dataproduct'].items() if (k[0]==taskmanager_id and k[1]==generation_id)}


    def duplicate_datablock(self, taskmanager_id, generation_id,
                            new_generation_id):
        # dumb and slow, but its ok for now
        datablock = self.get_datablock(taskmanager_id, generation_id)

        for old_id in datablock:
            new_id = (taskmanager_id, new_generation_id, old_id[2])
            for tname in ObjectDB._tables:
                ObjectDB._tables[tname][new_id] = copy.deepcopy(
                    ObjectDB._tables[tname][old_id])


    def close(self):
        pass


    def save_to_file(self, filename):
        if filename:
            with open(filename, 'w') as fd:
                fd.write(ObjectDB._tables)
