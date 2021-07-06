import platform
import time
import logging

import dbutils.pooled_db as pooled_db

if platform.python_implementation() == 'CPython':
    import psycopg2
    import psycopg2.extras
else:
    # try to load psycopg2cffi dynamically and use psycopg2 namespace
    import importlib
    importlib.import_module('psycopg2cffi')
    importlib.import_module('psycopg2cffi.compat')
    __import__('psycopg2cffi').compat.register()
    import psycopg2.extras

import decisionengine.framework.dataspace.datasource as ds

MAX_NUMBER_OF_RETRIES = 10
TIME_TO_SLEEP = 2


def generate_insert_query(table_name, keys):
    """
    Generate insert query given table name
    and list of fields

    :type table_name: :obj:`str`
    :arg table_name: Name of the table to insert into

    :keys: :obj:`list`
    :arg keys: List of column names

    :rtype: :obj:`str` - insert query

    """
    query = """
    INSERT INTO {} ({}) VALUES ({})
    """
    query = query.format(table_name, ",".join(keys), ("%s," * len(keys))[:-1])
    return query


SELECT_QUERY = """
SELECT tm.taskmanager_id, foo.* FROM {} foo, taskmanager tm
WHERE tm.sequence_id = foo.taskmanager_id
and foo.taskmanager_id=%s AND foo.generation_id=%s AND foo.key=%s
"""

SELECT_PRODUCTS = """
SELECT tm.taskmanager_id, foo.* FROM {} foo JOIN taskmanager tm
ON tm.sequence_id = foo.taskmanager_id
WHERE foo.taskmanager_id=%s
"""

SELECT_LAST_GENERATION_ID_BY_NAME = """
SELECT max(dp.generation_id) as generation_id
FROM dataproduct dp
JOIN taskmanager tm ON dp.taskmanager_id=tm.sequence_id
WHERE tm.name=%s
"""

SELECT_LAST_GENERATION_ID_BY_NAME_AND_ID = """
SELECT max(dp.generation_id)
FROM dataproduct dp
JOIN taskmanager tm ON dp.taskmanager_id=tm.sequence_id
WHERE tm.name=%s
AND tm.taskmanager_id=%s
"""

SELECT_TASKMANAGER_BY_NAME = """
SELECT tm.name, tm.sequence_id, tm.taskmanager_id, tm.datestamp
FROM taskmanager tm where tm.sequence_id =
(SELECT max(sequence_id) from taskmanager where name = %s);
"""

SELECT_TASKMANAGER_BY_NAME_AND_ID = """
SELECT tm.name, tm.sequence_id, tm.taskmanager_id, tm.datestamp
FROM taskmanager tm where tm.name = %s and tm.taskmanager_id = %s
"""

DELETE_OLD_DATA_QUERY = """
DELETE FROM taskmanager where datestamp < current_date - interval '%s days'
"""


class Postgresql(ds.DataSource):
    """
    Implementation of postgresql data source
    """

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
            'schema_id INT',  # Auto generated
            'schema BLOB',    # keys in the value dict of the dataproduct table
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

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.logger = logging.getLogger('decision_engine')
        self.logger.debug('Initializing a Postgresql datasource')

        # account for differences between psycopg2 and psycopg2cffi
        dbname = config_dict.get('database', config_dict.get('dbname', None))
        self.logger.debug(f"Trying to connect as {config_dict['user']}@{config_dict['host']}:{config_dict['port']}/{dbname}")

        self.connection_pool = pooled_db.PooledDB(psycopg2,
                                                  **config_dict)
        self.retries = MAX_NUMBER_OF_RETRIES
        self.timeout = TIME_TO_SLEEP

    def create_tables(self):
        return True

    def store_taskmanager(self, name, taskmanager_id, datestamp=None):
        if datestamp:
            return self._update_returning_result("INSERT INTO taskmanager (name, taskmanager_id, datestamp) values (%s, %s, %s)",
                                                 (name, taskmanager_id, datestamp)).get('sequence_id')

        return self._update_returning_result("INSERT INTO taskmanager (name, taskmanager_id) values (%s, %s)",
                                             (name, taskmanager_id)).get('sequence_id')

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        if taskmanager_id:
            try:
                return self._select_dictresult(SELECT_TASKMANAGER_BY_NAME_AND_ID,
                                               (taskmanager_name, taskmanager_id))[0]
            except IndexError:
                raise KeyError("Taskmanager={} taskmanager_id={} not found".format(
                    taskmanager_name, taskmanager_id))
        else:
            try:
                return self._select_dictresult(SELECT_TASKMANAGER_BY_NAME,
                                               (taskmanager_name,))[0]
            except IndexError:
                raise KeyError(
                    "Taskmanager={} not found".format(taskmanager_name))

    def get_taskmanagers(self,
                         taskmanager_name=None,
                         start_time=None,
                         end_time=None):

        SELECT_TASKMANAGERS = ("SELECT tm.name, "
                               "tm.sequence_id, "
                               "tm.taskmanager_id, "
                               "tm.datestamp "
                               "FROM taskmanager tm ")

        have_where = False
        if taskmanager_name:
            SELECT_TASKMANAGERS += " WHERE tm.name = '" + taskmanager_name + "'"
            have_where = True
        if start_time:
            if have_where:
                SELECT_TASKMANAGERS += " AND "
            else:
                SELECT_TASKMANAGERS += " WHERE "
                have_where = True
            SELECT_TASKMANAGERS += " tm.datestamp >= '" + start_time + "'"
        if end_time:
            if have_where:
                SELECT_TASKMANAGERS += " AND "
            else:
                SELECT_TASKMANAGERS += " WHERE "
            SELECT_TASKMANAGERS += " tm.datestamp <=  '" + end_time + "'"
        try:
            return self._select_dictresult(SELECT_TASKMANAGERS +
                                           " ORDER BY tm.datestamp ASC")
        except IndexError:
            raise KeyError()

    def get_last_generation_id(self,
                               taskmanager_name,
                               taskmanager_id=None):
        if taskmanager_id:
            try:
                generation_id = self._select(SELECT_LAST_GENERATION_ID_BY_NAME_AND_ID,
                                             (taskmanager_name, taskmanager_id))[0][0]
                assert generation_id
                return generation_id
            except AssertionError:
                raise KeyError("Last generation id not found for taskmanager={} taskmanager_id={}".
                               format(taskmanager_name, taskmanager_id))
        else:
            try:
                generation_id = self._select(SELECT_LAST_GENERATION_ID_BY_NAME,
                                             (taskmanager_name, ))[0][0]
                assert generation_id
                return generation_id
            except AssertionError:
                raise KeyError("Last generation id not found for taskmanager={}".
                               format(taskmanager_name, ))

    def insert(self, taskmanager_id, generation_id, key,
               value, header, metadata):

        self._insert(ds.DataSource.dataproduct_table,
                     {'taskmanager_id': taskmanager_id,
                      'generation_id': generation_id,
                      'key': key,
                      'value': psycopg2.Binary(value)
                      })

        self._insert(ds.DataSource.header_table,
                     {'taskmanager_id': taskmanager_id,
                      'generation_id': generation_id,
                      'key': key,
                      'create_time': header.get('create_time'),
                      'scheduled_create_time': header.get('scheduled_create_time'),
                      'expiration_time': header.get('expiration_time'),
                      'creator': header.get('creator'),
                      'schema_id': header.get('schema_id')
                      })

        self._insert(ds.DataSource.metadata_table,
                     {'taskmanager_id': taskmanager_id,
                      'generation_id': generation_id,
                      'key': key,
                      'state': metadata.get('state'),
                      'generation_time': metadata.get('generation_time'),
                      'missed_update_count': metadata.get('missed_update_count')
                      })

    def update(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        for table in (ds.DataSource.header_table, ds.DataSource.metadata_table,
                      ds.DataSource.dataproduct_table):
            q = SELECT_QUERY.format(table)
            try:
                self._select(q, (taskmanager_id, generation_id, key))[0]
            except IndexError:
                # do not log stack trace, Exception thrown is handled by the caller
                raise KeyError("taskmanager_id={} or generation_id={} or key={} not found in {}".format(
                    taskmanager_id, generation_id, key, table))

        q = """
            UPDATE {} SET value=%s
                      WHERE taskmanager_id=%s AND generation_id=%s AND key=%s
            """.format(ds.DataSource.dataproduct_table)

        self._update(q, (psycopg2.Binary(value),
                         taskmanager_id, generation_id, key))

        q = """
        UPDATE {} SET create_time=%s,
                      expiration_time=%s,
                      scheduled_create_time=%s,
                      creator=%s,
                      schema_id=%s
                  WHERE taskmanager_id=%s AND generation_id=%s AND key=%s
            """.format(ds.DataSource.header_table)
        self._update(q, (header.get('create_time'),
                         header.get('expiration_time'),
                         header.get('scheduled_create_time'),
                         header.get('creator'), header.get('schema_id'),
                         taskmanager_id, generation_id, key))

        q = """
             UPDATE {} SET state=%s,
                           generation_time=%s,
                           missed_update_count=%s
                        WHERE taskmanager_id=%s AND generation_id=%s AND key=%s
            """.format(ds.DataSource.metadata_table)
        self._update(q, (metadata.get('state'), metadata.get('generation_time'),
                         metadata.get('missed_update_count'),
                         taskmanager_id, generation_id, key))

    def get_header(self, taskmanager_id, generation_id, key):
        q = SELECT_QUERY.format(ds.DataSource.header_table)
        try:
            return self._select(q, (taskmanager_id, generation_id, key))[0]
        except IndexError:
            # do not log stack trace, Exception thrown is handled by the caller
            raise KeyError("taskmanager_id={} or generation_id={} or key={} not found".format(
                taskmanager_id, generation_id, key))

    def get_metadata(self, taskmanager_id, generation_id, key):
        q = SELECT_QUERY.format(ds.DataSource.metadata_table)
        try:
            return self._select(q, (taskmanager_id, generation_id, key))[0]
        except IndexError:
            # do not log stack trace, Exception thrown is handled by the caller
            raise KeyError("taskmanager_id={} or generation_id={} or key={} not found".format(
                taskmanager_id, generation_id, key))

    def get_dataproducts(self, taskmanager_id, key=None):
        q = SELECT_PRODUCTS.format(ds.DataSource.dataproduct_table)
        if key:
            q += f"AND foo.key = '{key}'"
        try:
            result = []
            rows = self._select_dictresult(q, (taskmanager_id,))
            for row in rows:
                result.append({'key': row['key'],
                               'taskmanager_id': row['taskmanager_id'],
                               'generation_id': row['generation_id'],
                               'value': row['value'].tobytes()})
            return result
        except IndexError:
            # do not log stack trace, Exception thrown is handled by the caller
            raise KeyError("taskmanager_id={} not found".format(taskmanager_id))

    def get_dataproduct(self, taskmanager_id, generation_id, key):
        q = SELECT_QUERY.format(ds.DataSource.dataproduct_table)
        try:
            value_row = self._select_dictresult(q, (taskmanager_id, generation_id, key))[0]
            return value_row['value'].tobytes()
        except IndexError:
            # do not log stack trace, Exception thrown is handled by the caller
            raise KeyError("taskmanager_id={} or generation_id={} or key={} not found".format(
                taskmanager_id, generation_id, key))

    def get_datablock(self, taskmanager_id, generation_id):
        return {}

    def duplicate_datablock(self, taskmanager_id, generation_id,
                            new_generation_id):
        for q in ("""
            INSERT INTO {} (taskmanager_id,
                            generation_id,
                            key,
                            value)
                   SELECT taskmanager_id,
                          %s,
                          key,
                          value
                   FROM {}
                   WHERE taskmanager_id=%s AND generation_id=%s
            """.format(ds.DataSource.dataproduct_table, ds.DataSource.dataproduct_table),
                  """
            INSERT INTO {} (taskmanager_id,
                            generation_id,
                            key,
                            state,
                            generation_time,
                            missed_update_count)
                   SELECT taskmanager_id,
                          %s,
                          key,
                          state,
                          generation_time,
                          missed_update_count
                   FROM {}
                   WHERE taskmanager_id=%s AND generation_id=%s
            """.format(ds.DataSource.metadata_table, ds.DataSource.metadata_table),
                  """
            INSERT INTO {} (taskmanager_id,
                        generation_id,
                        key,
                        create_time,
                        expiration_time,
                        scheduled_create_time,
                        creator,
                        schema_id)
                 SELECT taskmanager_id,
                        %s,
                        key,
                        create_time,
                        expiration_time,
                        scheduled_create_time,
                        creator,
                        schema_id
                 FROM {}
                 WHERE taskmanager_id=%s
                 AND   generation_id=%s
                 """.format(ds.DataSource.header_table, ds.DataSource.header_table)):
            self._insert(q, (new_generation_id, taskmanager_id, generation_id))

    def delete_data_older_than(self, days):
        """
        Delete data older that days interval
        :type days: :obj:`int`
        :arg days: remove data older than days interval
        """
        if days <= 0:
            # do not log stack trace, Exception thrown is handled by the caller
            raise ValueError("Argument has to be positive, non zero integer. Supplied {}".format(days))
        self._remove(DELETE_OLD_DATA_QUERY, (days, ))
        return

    def close(self):
        pass

    def connect(self):
        pass

    def get_schema(self, table=None):
        return {}

    def get_connection(self):
        i = self.retries + 1
        t = self.timeout
        while i:
            try:
                return self.connection_pool.connection()
            except Exception:
                # do not log stack trace, Exception thrown is handled by the caller
                i -= 1
                if not i:
                    raise
                else:
                    time.sleep(t)
                    t *= self.timeout

    def _select(self, query_string, values=None, cursor_factory=None):
        colnames, res = self.__query(query_string, values, cursor_factory)
        return res

    def __query(self, query_string, values=None, cursor_factory=None):
        db, cursor = None, None
        try:
            db = self.get_connection()
            if cursor_factory:
                cursor = db.cursor(cursor_factory=cursor_factory)
            else:
                cursor = db.cursor()
            if values:
                cursor.execute(query_string, values)
            else:
                cursor.execute(query_string)
            colnames = [desc[0] for desc in cursor.description]
            res = cursor.fetchall()
            return colnames, res
        except psycopg2.Error:  # pragma: no cover
            # do not log stack trace, Exception thrown is handled by the caller
            raise
        finally:
            try:
                list(x.close if x else None for x in (cursor, db))
            except psycopg2.Error:  # pragma: no cover
                # do not log stack trace, Exception thrown is handled by the caller
                pass

    def _update(self, query_string, values=None):
        db, cursor = None, None
        try:
            db = self.connection_pool.connection()
            cursor = db.cursor()
            if values:
                cursor.execute(query_string, values)
            else:
                cursor.execute(query_string)
            db.commit()
        except psycopg2.Error:
            try:
                if db:
                    db.rollback()
            except psycopg2.Error:  # pragma: no cover
                pass
            raise
        finally:
            list(x.close if x else None for x in (cursor, db))

    def _update_returning_result(self, query_string, values=None):
        db, cursor = None, None
        try:
            db = self.connection_pool.connection()
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query_string += " RETURNING *"
            if values:
                cursor.execute(query_string, values)
            else:
                cursor.execute(query_string)
            res = cursor.fetchone()
            db.commit()
            return res
        except psycopg2.Error:
            try:
                if db:
                    db.rollback()
            except psycopg2.Error:  # pragma: no cover
                pass
            raise
        finally:
            list(x.close if x else None for x in (cursor, db))

    def _insert(self, table_name_or_sql_query, record=None):
        try:
            if record:
                if isinstance(record, dict):
                    q = generate_insert_query(
                        table_name_or_sql_query, list(record.keys()))
                    return self._update(q, list(record.values()))
                else:
                    return self._update(table_name_or_sql_query, record)
            else:
                return self._update(table_name_or_sql_query)
        except Exception:
            raise


    def _insert_returning_result(self, table_name_or_sql_query, record=None):
        try:
            if record:
                if isinstance(record, dict):
                    q = generate_insert_query(
                        table_name_or_sql_query, list(record.keys()))
                    return self._update_returning_result(q, list(record.values()))
                else:
                    return self._update_returning_result(table_name_or_sql_query, record)
            else:
                return self._update_returning_result(table_name_or_sql_query)
        except Exception:
            raise

    def _remove(self, sql_query, values=None):
        return self._update(sql_query, values)

    def _delete(self, sql_query, values=None):
        return self._remove(sql_query, values)

    def _select_dictresult(self, sql_query, values=None):
        if values:
            result = self._select(
                sql_query, values, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            result = self._select(
                sql_query, cursor_factory=psycopg2.extras.RealDictCursor)
        return result

    def _select_getresult(self, sql_query, values=None):
        if values:
            result = self._select(
                sql_query, values, cursor_factory=psycopg2.extras.DictCursor)
        else:
            result = self._select(
                sql_query, cursor_factory=psycopg2.extras.DictCursor)
        return result

    def _select_tuple(self, sql_query, values):
        return self._select(sql_query, values)
