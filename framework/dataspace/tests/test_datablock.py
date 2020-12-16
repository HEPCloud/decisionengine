import ast
import os
import pickle
import pytest
import pytest_postgresql
import unittest
import zlib

from decisionengine.framework.dataspace import dataspace, datablock

@pytest.fixture()
def datasource(request, postgresql, data):
    with postgresql.cursor() as cursor:
        cwd = os.path.split(os.path.abspath(__file__))[0]
        # Load decision engine schema
        cursor.execute(open(cwd + "/../datasources/postgresql.sql", "r").read())
        # Load test data
        for table, rows in data.items():
            for row in rows:
                keys = ",".join(row.keys())
                values = ("%s," * len(row.values()))[:-1]
                query = f"INSERT INTO {table} ({keys}) VALUES({values})"
                cursor.execute(query, list(row.values()))
    postgresql.commit()

    return postgresql

@pytest.fixture()
def data():
    return {
        "taskmanager": [
            {
                "taskmanager_id": "1",
                "name": "taskmanager1"
            }
        ],
        "dataproduct": [
            {
                "taskmanager_id": "1",
                "generation_id": "1",
                "key": "test_key1",
                "value": "test_value1"
            }
        ]
    }

@pytest.fixture()
def dspace(datasource):
    global_config = {
        'dataspace': {
            'reaper_start_delay_seconds': 1818,
            'retention_interval_in_days': 365,
            'datasource': {
                'module': 'decisionengine.framework.dataspace.datasources.postgresql',
                'name': 'Postgresql',
                'config': {
                    'user': datasource.info.dsn_parameters["user"],
                    'blocking': True,
                    'host': datasource.info.dsn_parameters["host"],
                    'port': datasource.info.dsn_parameters["port"],
                    'database': datasource.info.dsn_parameters["dbname"],
                    'maxconnections': 100,
                    'maxcached': 10,
                },
            },
        }
    }
    return dataspace.DataSpace(global_config)

@pytest.fixture()
def dblock(dspace, data):
    return datablock.DataBlock(dspace, data["taskmanager"][0]["name"], data["taskmanager"][0]["taskmanager_id"])

# Wrapper to embed pytest fixtures in a TestCase class
@pytest.fixture()
def fixtures(request, data, dspace, dblock):
    request.cls.data = data
    request.cls.dataspace = dspace
    request.cls.datablock = dblock

@pytest.mark.usefixtures("fixtures")
class TestDatablock(unittest.TestCase):

    def setUp(self):
        self.obj = {'a': {'b': 'c'}}

    def tearDown(self):
        pass

    def test_zdumps(self):
        zbytes = datablock.zdumps(self.obj)
        value = pickle.loads(zlib.decompress(zbytes))

        self.assertEqual(value, self.obj)

    def test_zloads(self):
        zbytes = zlib.compress(pickle.dumps(self.obj))
        value = datablock.zloads(zbytes)
        self.assertEqual(value, self.obj)

        zbytes = pickle.dumps(self.obj)
        value = datablock.zloads(zbytes.decode("latin1"))
        self.assertEqual(value, self.obj)

        zbytes = pickle.dumps(self.obj)
        value = datablock.zloads(zbytes)
        self.assertEqual(value, self.obj)

    def test_compress(self):
        zbytes = datablock.compress({'pickled': True,
                                     'value': pickle.dumps(self.obj,
                                                           protocol=pickle.HIGHEST_PROTOCOL)})
        value = ast.literal_eval(datablock.decompress(zbytes))
        value = datablock.zloads(value.get('value'))
        self.assertEqual(value, self.obj)

        zbytes = datablock.compress({'pickled': True,
                                     'value': zlib.compress(pickle.dumps(self.obj,
                                                                         protocol=pickle.HIGHEST_PROTOCOL), 9)})
        value = ast.literal_eval(datablock.decompress(zbytes))
        value = datablock.zloads(value.get('value'))
        self.assertEqual(value, self.obj)

        value = str(self.obj).encode("latin1")
        value = ast.literal_eval(datablock.decompress(value))
        self.assertEqual(value, self.obj)

    def test_DataBlock_constructor(self):
        dblock = datablock.DataBlock(self.dataspace, self.data["taskmanager"][0]["name"],
                                     self.data["taskmanager"][0]["taskmanager_id"])
        self.assertEqual(str(dblock.generation_id), self.data["dataproduct"][0]["generation_id"])

        dblock = datablock.DataBlock(self.dataspace, self.data["taskmanager"][0]["name"],
                                     generation_id=self.data["dataproduct"][0]["generation_id"])
        self.assertEqual(str(dblock.generation_id), self.data["dataproduct"][0]["generation_id"])

        dblock = datablock.DataBlock(self.dataspace, self.data["taskmanager"][0]["name"],
                                     taskmanager_id=self.data["taskmanager"][0]["taskmanager_id"],
                                     sequence_id=1)
        self.assertEqual(str(dblock.generation_id), self.data["dataproduct"][0]["generation_id"])

    def test_DataBlock_to_str(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        self.datablock.put(dataproduct["key"], dataproduct["value"], header)

        result = str(self.datablock)
        self.assertEqual(
            result,
            "{'taskamanger_id': '1', 'generation_id': 1, 'sequence_id': 2, "
            "'keys': ['%s'], 'dataproducts': {'%s': '%s'}}"
            % (dataproduct["key"], dataproduct["key"], dataproduct["value"])
        )

    def test_DataBlock_key_management(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])

        self.datablock.put(dataproduct["key"], dataproduct["value"], header)

        keys = self.datablock.keys()
        self.assertIn(dataproduct["key"], keys)

        self.assertIn(dataproduct["key"], self.datablock)

        self.assertEqual(self.datablock.get(dataproduct["key"]), dataproduct["value"])

        newDict = {"subKey": "newValue"}
        self.datablock.put(dataproduct["key"], newDict, header)
        self.assertEqual(self.datablock[dataproduct["key"]], newDict)

        with self.assertRaises(KeyError):
            self.datablock["invalidKey"]

    def test_DataBlock_get_header(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        self.datablock.put(dataproduct["key"], dataproduct["value"], header)

        self.assertEqual(header, self.datablock.get_header(dataproduct["key"]))

    def test_DataBlock_get_metadata(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        metadata = datablock.Metadata(dataproduct["taskmanager_id"], generation_id=int(dataproduct["generation_id"]))
        self.datablock.put(dataproduct["key"], dataproduct["value"], header, metadata)

        self.assertEqual(metadata, self.datablock.get_metadata(dataproduct["key"]))

    def test_DataBlock_get_taskmanager(self):
        taskmanager = self.data["taskmanager"][0]
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        self.datablock.put(dataproduct["key"], dataproduct["value"], header)

        tid = self.datablock.get_taskmanager(taskmanager["name"])["taskmanager_id"]
        self.assertEqual(taskmanager["taskmanager_id"], tid)

    def test_DataBlock_get_taskmanagers(self):
        taskmanager = self.data["taskmanager"][0]
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        self.datablock.put(dataproduct["key"], dataproduct["value"], header)
        tms = self.dataspace.get_taskmanagers()
        self.assertEqual(taskmanager["taskmanager_id"], tms[0]["taskmanager_id"])
        products = self.datablock.get_dataproducts()
        self.assertEqual(dataproduct["value"], products[0]["value"])

    def test_DataBlock_duplicate(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])
        metadata = datablock.Metadata(dataproduct["taskmanager_id"], generation_id=int(dataproduct["generation_id"]))
        self.datablock.put(dataproduct["key"], dataproduct["value"], header, metadata)

        dblock = self.datablock.duplicate()

        self.assertEqual(dblock.taskmanager_id, self.datablock.taskmanager_id)
        self.assertEqual(dblock.generation_id + 1, self.datablock.generation_id)
        self.assertEqual(dblock.sequence_id, self.datablock.sequence_id)
        self.assertEqual(dblock._keys, self.datablock._keys)
        for key in self.datablock._keys:
            self.assertEqual(dblock[key], self.datablock[key])

    def test_Metadata_constructor(self):
        dataproduct = self.data["dataproduct"][0]

        metadata = datablock.Metadata(dataproduct["taskmanager_id"])
        self.assertEqual(metadata.data["taskmanager_id"], dataproduct["taskmanager_id"])

        genTime = 1.0
        missCount = 3
        state = "START_BACKUP"
        metadata = datablock.Metadata(dataproduct["taskmanager_id"],
                                      state=state,
                                      generation_id=int(dataproduct["generation_id"]),
                                      generation_time=genTime,
                                      missed_update_count=missCount)
        self.assertEqual(metadata.data["taskmanager_id"], dataproduct["taskmanager_id"])
        self.assertEqual(metadata.data["state"], state)
        self.assertEqual(metadata.data["generation_id"], int(dataproduct["generation_id"]))
        self.assertEqual(metadata.data["generation_time"], genTime)
        self.assertEqual(metadata.data["missed_update_count"], missCount)

        with self.assertRaises(datablock.InvalidMetadataError):
            metadata = datablock.Metadata(dataproduct["taskmanager_id"], "INVALID_STATE")

    def test_Metadata_set_state(self):
        dataproduct = self.data["dataproduct"][0]
        metadata = datablock.Metadata(dataproduct["taskmanager_id"])

        state = "START_BACKUP"
        metadata.set_state(state)
        self.assertEqual(metadata.data["state"], state)

        with self.assertRaises(datablock.InvalidMetadataError):
            metadata.set_state("INVALID_STATE")

    def test_Header_constructor(self):
        dataproduct = self.data["dataproduct"][0]

        header = datablock.Header(dataproduct["taskmanager_id"])
        self.assertEqual(header.data["taskmanager_id"], dataproduct["taskmanager_id"])

        createTime = 1.0
        expirationTime = 3.0
        scheduleTime = 5.0
        creator = "creator"
        schema = 1
        header = datablock.Header(dataproduct["taskmanager_id"],
                                  create_time=createTime,
                                  expiration_time=expirationTime,
                                  scheduled_create_time=scheduleTime,
                                  creator=creator,
                                  schema_id=schema)
        self.assertEqual(header.data["taskmanager_id"], dataproduct["taskmanager_id"])
        self.assertEqual(header.data["create_time"], createTime)
        self.assertEqual(header.data["expiration_time"], expirationTime)
        self.assertEqual(header.data["scheduled_create_time"], scheduleTime)
        self.assertEqual(header.data["creator"], creator)
        self.assertEqual(header.data["schema_id"], schema)

    def test_Header_is_valid(self):
        dataproduct = self.data["dataproduct"][0]
        header = datablock.Header(dataproduct["taskmanager_id"])

        self.assertEqual(header.is_valid(), True)


if __name__ == "__main__":
    unittest.main()
