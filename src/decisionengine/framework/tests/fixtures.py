'''defaults for pytest'''
import os

# load DE Server fixtures
# even though we are only using DEServer
# we need to import all of these to instantiate the other fixtures
# so that DEServer gets setup correctly
from decisionengine.framework.engine.tests.fixtures import DE_DB_HOST, DE_DB_USER, DE_DB_PASS, DE_DB_NAME, DE_SCHEMA, PG_PROG, DE_DB, DE_HOST, DEServer

# set path to test config
TEST_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etc/decisionengine")
TEST_CHANNEL_CONFIG_PATH = os.path.join(TEST_CONFIG_PATH, 'config.d')

__all__ = ['DE_DB_HOST', 'DE_DB_USER', 'DE_DB_PASS', 'DE_DB_NAME', 'DE_SCHEMA',
           'PG_PROG', 'DE_DB', 'DE_HOST', 'DEServer', 'TEST_CONFIG_PATH', 'TEST_CHANNEL_CONFIG_PATH']
