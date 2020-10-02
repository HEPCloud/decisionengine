'''pytest fixtures/constants'''
import os
from pytest_postgresql import factories

DE_DB_HOST = '127.0.0.1'
DE_DB_USER = 'postgres'
DE_DB_PASS = None
DE_DB_NAME = 'decisionengine'
DE_SCHEMA = [os.path.dirname(os.path.abspath(__file__)) + "/../postgresql.sql", ]

# DE_DB_PORT assigned at random
PG_PROG = factories.postgresql_proc(user=DE_DB_USER, password=DE_DB_PASS,
                                    host=DE_DB_HOST, port=None)
DE_DB = factories.postgresql('PG_PROG', db_name=DE_DB_NAME, load=DE_SCHEMA)
