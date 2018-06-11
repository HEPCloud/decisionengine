import pytest
import os
import sys
import time
import getpass

from decisionengine.framework.dataspace.datablock import DataBlock, Header, Metadata
from decisionengine.framework.dataspace.dataspace import DataSpace

config_object_db = {
    'dataspace': {
        'db_driver': {
            'module': 'decisionengine.framework.dataspace.db_object',
            'name': 'ObjectDB',
            'config': {},
        },
    }
}

config_sqlite3_db = {
    'dataspace': {
        'db_driver': {
            'module': 'decisionengine.framework.dataspace.db_sqlite3',
            'name': 'SQLite3DB',
            'config': {
                'filename': '/tmp/testdb-%s.db' % (os.environ.get('USER'),),
            },
        },
    }
}

config = config_object_db

def are_dicts_same(x, y):

    xitems = x.items()
    yitems = y.items()
    shared_items = set(xitems) & set(yitems)

    return len(xitems) == len(yitems) and len(shared_items) == len(xitems)

class TestDataBlock:

    def test_datablock(self):
        print "Hello test_datablock"
        if config['dataspace']['db_driver']['name'] == 'SQLite3DB':
            filename = config['dataspace']['db_driver']['config']['filename']
            if os.path.exists(filename):
                os.unlink(filename)

        dataspace = DataSpace(config)

        taskmanager_id = 'E0B9A7F5-B55E-47F6-B5EF-DCCB8B977AFE'
        generation_id = 9999

        datablock = DataBlock(dataspace, taskmanager_id, generation_id)

        timestamp = time.time()
        key = 'aKey'
        value = {"m1": "v1"}
        header = Header(taskmanager_id, create_time=timestamp,
                        scheduled_create_time=timestamp+600,
                        schema_id=0)
        metadata = Metadata(taskmanager_id, generation_time=timestamp, generation_id=generation_id)

        print 'Doing put:\nkey=%s\nvalue=%s\n\nheader=%s\n\nmetadata=%s\n\n' % (
            key, value, header, metadata)
        datablock.put(key, value, header, metadata)
        datablock.put('zKey', {'mz': 'vz'}, header, metadata)

        print 'Doing get: key=%s ...\n' % key
        db_value = datablock.get(key)
        print db_value
        print 'Doing get_header: key=%s ...\n' % key
        db_header = datablock.get_header(key)
        print db_header
        print 'Doing get_metadata: key=%s ...\n' % key
        db_metadata = datablock.get_metadata(key)
        print db_metadata

        print 'Performing comparison of value, header and metadata ...'
        if (are_dicts_same(value, db_value) and
           are_dicts_same(header, db_header) and
           are_dicts_same(metadata, db_metadata)):
            print 'DICTS CONSISTENCY CHECK PASSED\n'
        else:
            print 'DICTS CONSISTENCY CHECK FAILED\n'
        assert (are_dicts_same(value, db_value) and
                are_dicts_same(header, db_header) and
                are_dicts_same(metadata, db_metadata))


        # TEST: Insert new value for same key
        new_value = {"m2": "v2"}
        print 'Doing put:\nkey=%s\nvalue=%s\nheader=%s\nmetadata=%s\n' % (
            key, new_value, header, metadata)
        datablock.put(key, new_value, header, metadata)
        print 'Doing get: key=%s ...\n' % key
        print datablock.get(key)
        db_new_value = datablock.get(key)
        db_header = datablock.get_header(key)
        db_metadata = datablock.get_metadata(key)
        assert are_dicts_same(new_value, db_new_value)
        assert (are_dicts_same(new_value, db_new_value) and
                are_dicts_same(header, db_header) and
                are_dicts_same(metadata, db_metadata))


        # TEST: Duplicate functionality

        print '-----------------------'
        print 'Duplicating datablock ...\n'
        dup_datablock = datablock.duplicate()

        print '---'
        print 'datablock.generation_id = ', datablock.generation_id
        print 'Doing get: key=%s ...\n' % key
        print datablock.get(key)
        print 'Doing get_header: key=%s ...\n' % key
        print datablock.get_header(key)
        print 'Doing get_metadata: key=%s ...\n' % key
        print datablock.get_metadata(key)
        print '---'
        print 'dup_datablock.generation_id = ', dup_datablock.generation_id
        print 'Doing get on dup_datablock: key=%s\n' % key
        print dup_datablock.get(key)
        print 'Doing get_header on dup_datablock: key=%s ...\n' % key
        print dup_datablock.get_header(key)
        print 'Doing get_metadata on dup_datablock: key=%s ...\n' % key
        print dup_datablock.get_metadata(key)
        print '---'

        # TEST: Insert new value on duplicated datablock
        new_value3 = {"m3": "v3"}
        dup_datablock.put(key, new_value3, dup_datablock.get_header(key), dup_datablock.get_metadata(key))

        print dup_datablock.get(key)
        print dup_datablock.get_header(key)
        print dup_datablock.get_metadata(key)

        db_dup_value = dup_datablock.get(key)
        db_dup_header = dup_datablock.get_header(key)
        db_dup_metadata = dup_datablock.get_metadata(key)

        assert (are_dicts_same(new_value3, db_dup_value) and
                are_dicts_same(header, db_dup_header) and
                are_dicts_same(metadata, db_dup_metadata))

        metadata1 = Metadata(taskmanager_id, generation_time=timestamp, generation_id=(generation_id + 1))

        db_orig_value = datablock.get(key)
        db_orig_header = datablock.get_header(key)
        db_orig_metadata = datablock.get_metadata(key)

        assert (are_dicts_same(new_value, db_orig_value) and
                are_dicts_same(header, db_orig_header) and
                are_dicts_same(metadata1, db_orig_metadata))

        dataspace.close()
