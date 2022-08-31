# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import ast
import copy
import pickle
import threading
import time
import uuid
import zlib

from collections import UserDict

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

###############################################################################
# TODO:
# 1) Need to make sure there are no race conditions
# 2) Add mutex/locks/critical sections where ever required
# 3) Manipulations on the Header functionality
# 4) Manipulations on the Metadata functionality
# 5) get() needs to error in case of expired data
###############################################################################

_ENCODING = "latin1"


def zdumps(obj):
    """
    Pickle and compress
    :param obj: a python object
    :return: compressed string
    """
    return zlib.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL), 9)


def zloads(zbytes):
    """
    Decompress and unpickle
    If input is not compressed
    attempts to just unpickle it

    :param zbytes: compressed bytes
    :return: returns python object
    """
    try:
        return pickle.loads(zlib.decompress(zbytes))
    except TypeError:
        b = bytes(zbytes, _ENCODING)
        return pickle.loads(b, encoding=_ENCODING)
    except zlib.error:
        return pickle.loads(zbytes)


def compress(obj):
    """
    Compress python object
    :param obj: python object
    :return: compressed object
    """
    return zlib.compress(str(obj).encode(_ENCODING), 9)


def decompress(zbytes):
    """
    Decompress zipped byte stream, convert to string.
    :param zbytes: byte stream
    :return: uncompressed string
    """
    try:
        return zlib.decompress(zbytes).decode(_ENCODING)
    except zlib.error:
        return zbytes.decode(_ENCODING)


class InvalidMetadataError(Exception):
    """
    Errors due to invalid Metadata
    """

    pass


class Metadata(UserDict):

    # Minimum information required for the Metadata dict to be valid
    required_keys = {"taskmanager_id", "state", "generation_id", "generation_time", "missed_update_count"}

    # Valid states
    valid_states = {"NEW", "START_BACKUP", "METADATA_UPDATE", "END_CYCLE"}

    def __init__(self, taskmanager_id, state="NEW", generation_id=None, generation_time=None, missed_update_count=0):
        """
        Initialize Metadata object

        :type taskmanager_id: :obj:`string`
        :type state: :obj:`string`
        :type generation_id: :obj:`int`
        :type generation_time: :obj:`float`
        :type missed_update_count: :obj:`int`
        """
        UserDict.__init__(self)
        if state not in Metadata.valid_states:
            structlog.getLogger(LOGGERNAME).exception(f"Invalid Metadata state: {state}")
            raise InvalidMetadataError()
        if not generation_time:
            generation_time = time.time()

        self.data = {
            "taskmanager_id": taskmanager_id,
            "state": state,
            "generation_id": generation_id,
            "generation_time": int(generation_time),
            "missed_update_count": missed_update_count,
        }

    def set_state(self, state):
        """
        Set the state for the Metadata

        :type state: :obj:`string`
        """

        if state not in Metadata.valid_states:
            structlog.getLogger(LOGGERNAME).exception(f"{state} is not a valid Metadata state")
            raise InvalidMetadataError()
        self.data["state"] = state


class Header(UserDict):

    # Minimum information required for the Header dict to be valid
    required_keys = {
        "taskmanager_id",
        "create_time",
        "expiration_time",
        "scheduled_create_time",
        "creator",
        "schema_id",
    }

    # Default lifetime of the data if the expiration time is not specified
    default_data_lifetime = 1800

    def __init__(
        self,
        taskmanager_id,
        create_time=None,
        expiration_time=None,
        scheduled_create_time=None,
        creator="module",
        schema_id=None,
    ):
        """
        Initialize Header object

        :type taskmanager_id: :obj:`string`
        :type create_time: :obj:`float`
        :type expiration_time: :obj:`float`
        :type scheduled_create_time: :obj:`float`
        :type creator: :obj:`string`
        :type schema_id: :obj:`int`
        """

        UserDict.__init__(self)
        if not create_time:
            create_time = time.time()
        if not expiration_time:
            expiration_time = create_time + Header.default_data_lifetime
        if not scheduled_create_time:
            scheduled_create_time = time.time()

        self.data = {
            "taskmanager_id": taskmanager_id,
            "create_time": int(create_time),
            "expiration_time": int(expiration_time),
            "scheduled_create_time": int(scheduled_create_time),
            "creator": creator,
            "schema_id": schema_id,
        }

    def is_valid(self):
        """
        Check if the Header has minimum required information
        """
        try:
            return set(self.data.keys()).issubset(Header.required_keys)
        except Exception:  # pragma: no cover
            structlog.getLogger(LOGGERNAME).exception("Unexpected error checking Header information")
            raise


class ProductRetriever:
    def __init__(self, product_name, product_type, product_source):
        self.name = product_name
        self.type = product_type  # Not yet used
        self.creator = product_source  # Not yet used

    def __call__(self, datablock):
        return datablock[self.name]

    def __str__(self):
        return f"Product retriever for {self.__dict__}"


class DataBlock:
    def __init__(self, dataspace, name, taskmanager_id=None, generation_id=None, sequence_id=None):
        """
        Initialize DataBlock object

        :type dataspace: :obj:`DataSpace`
        :type name: :obj:`string`
        :type taskmanager_id: :obj:`string`
        :type generation_id: :obj:`int`
        """

        self.__internal_data_write_lock = threading.Lock()
        self.__internal_data_read_lock = threading.Lock()
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)
        self.logger.debug("Initializing a datablock for %s", name)
        self.dataspace = dataspace

        # If taskmanager_id is None create new or
        if taskmanager_id:
            self.taskmanager_id = taskmanager_id
        else:
            self.taskmanager_id = f"{uuid.uuid1()}".upper()

        if sequence_id:
            self.sequence_id = sequence_id
        else:
            self.sequence_id = self.store_taskmanager(name, self.taskmanager_id)

        if generation_id:
            self.generation_id = generation_id
        else:
            self.generation_id = self.dataspace.get_last_generation_id(name, taskmanager_id)

        self.lock = threading.Lock()

    def __str__(self):
        value = {
            "taskmanager_id": self.taskmanager_id,
            "generation_id": self.generation_id,
            "sequence_id": self.sequence_id,
            "keys": self.keys(),
        }
        dp = {}
        for key in self.keys():
            dp[key] = self.get(key)
        value["dataproducts"] = dp
        return f"{value}"

    def __contains__(self, key):
        return key in self.keys()  # noqa: SIM118

    def keys(self):
        self.logger.debug("datablock waiting for internal read lock in 'keys'")
        with self.__internal_data_read_lock:
            return tuple(self.dataspace.get_datablock(self.sequence_id, self.generation_id).keys())

    def store_taskmanager(self, taskmanager_name, taskmanager_id):
        """
        Persist TaskManager, returns sequence number
        :type taskmanager_name: :obj:`string`
        :type taskmanager_id: :obj: `string`
        :rtype: :obj:`int`
        """
        self.logger.debug("datablock waiting for internal write lock in 'store_taskmanager'")
        with self.__internal_data_write_lock:
            self.logger.debug("datablock waiting for internal read lock in 'store_taskmanager'")
            with self.__internal_data_read_lock:
                return self.dataspace.store_taskmanager(taskmanager_name, taskmanager_id)

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        """
        Retrieve TaskManager

        Args:
            taskmanager_name (str): Name of the TaskManager
            taskmanager_id (str, optional): ID of the TaskManager to retrieve. Defaults to None.

        Returns:
            dict: TaskManager information

        The dictionary returned looks like :

        .. code-block:: python

            {
                'datestamp': datetime.datetime(2017, 12, 20, 17, 37, 17, 503210,
                            tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=-360, name=None)),
                'sequence_id': 135L,
                'name': 'AWS_Calculations',
                'taskmanager_id': '77B16EB5-C79E-45B0-B1B1-37E846692E1D'
            }
        """
        return self.dataspace.get_taskmanager(taskmanager_name, taskmanager_id)

    def put(self, key, value, header, metadata=None):
        """
        Put data into the DataBlock

        :type key: :obj:`string`
        :type value: :obj:`dict`
        :type header: :obj:`Header`
        :type metadata: :obj:`Metadata`
        """
        self._setitem(key, value, header, metadata)

    def get(self, key, default=None):
        """
        Return the value associated with the key in the database

        :type key: :obj:`string`
        :rtype: :obj:`dict`
        """
        return self.__getitem__(key, default=default)

    def __insert(self, key, value, header, metadata):
        """
        Insert a new product into database with header and metadata

        :type key: :obj:`string`
        :type value: :obj:`dict`
        :type header: :obj:`Header`
        :type metadata: :obj:`Metadata`
        """
        self.dataspace.insert(self.sequence_id, self.generation_id, key, value, header, metadata)

    def __update(self, key, value, header, metadata):
        """
        Update an existing product in the database with header and metadata

        :type key: :obj:`string`
        :type value: :obj:`dict`
        :type header: :obj:`Header`
        :type metadata: :obj:`Metadata`
        """
        self.dataspace.update(self.sequence_id, self.generation_id, key, value, header, metadata)

    def _setitem(self, key, value, header, metadata=None):
        """
        put a product in the database with header and metadata

        :type key: :obj:`string`
        :type value: :obj:`dict`
        :type header: :obj:`Header`
        :type metadata: :obj:`Metadata`
        """

        if not metadata:
            metadata = Metadata(
                self.sequence_id,
                state="NEW",
                generation_id=self.generation_id,
                generation_time=time.time(),
                missed_update_count=0,
            )

        if isinstance(value, dict):
            store_value = compress({"pickled": False, "value": value})
        else:
            store_value = compress({"pickled": True, "value": pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)})
        self.logger.debug("datablock waiting for internal write lock in '_setitem'")
        with self.__internal_data_write_lock:
            if key in self:
                # This has been already inserted, so you are working on a copy
                # that was backed up. You need to update and adjust the update
                # counter
                self.__update(key, store_value, header, metadata)
            else:
                self.__insert(key, store_value, header, metadata)

    def get_dataproducts(self, key=None):
        values = self.dataspace.get_dataproducts(self.sequence_id, key)
        result = []

        try:
            for value in values:
                v = ast.literal_eval(decompress(value.get("value")))
                if v.get("pickled"):
                    v = zloads(v.get("value"))
                else:
                    v = value.get("value")
                result.append(
                    {
                        "key": value["key"],
                        "generation_id": value["generation_id"],
                        "taskmanager_id": value["taskmanager_id"],
                        "value": v,
                    }
                )
        except Exception:  # pragma: no cover
            self.logger.exception("Unexpected error in get_dataproducts")
        return result

    def __getitem__(self, key, default=None):
        """
        Return the value associated with the key in the database

        :type key: :obj:`string`
        :type default: :obj:`dict`
        :rtype: :obj:`dict`
        """

        try:
            value = self.dataspace.get_dataproduct(self.sequence_id, self.generation_id, key)
            value = ast.literal_eval(decompress(value))
        except KeyError:
            self.logger.error(f"Did not get key '{key}' in datablock __getitem__")
            value = default

        if not value:
            self.logger.exception(f"No key '{key}' in datablock __getitem__")
            raise KeyError(f"No key '{key}' in datablock __getitem__")

        if value.get("pickled"):
            return_value = zloads(value.get("value"))
        else:
            return_value = value.get("value")
        return return_value

    def get_header(self, key):
        """
        Return the Header associated with the key in the database

        :type key: :obj:`string`
        :rtype: :obj:`Header`
        """
        header_row = self.dataspace.get_header(self.sequence_id, self.generation_id, key)
        return Header(
            header_row[0],
            create_time=header_row[4],
            expiration_time=header_row[5],
            scheduled_create_time=header_row[6],
            creator=header_row[7],
            schema_id=header_row[8],
        )

    def get_metadata(self, key):
        """
        Return the metadata associated with the key in the database

        :type key: :obj:`string`
        :rtype: :obj:`Metadata`
        """
        metadata_row = self.dataspace.get_metadata(self.sequence_id, self.generation_id, key)
        return Metadata(
            metadata_row[0],
            state=metadata_row[4],
            generation_id=metadata_row[2],
            generation_time=metadata_row[5],
            missed_update_count=metadata_row[6],
        )

    def duplicate(self):
        """
        Duplicate the datablock and return this new DataBlock. The intent is
        that at the point the duplication occurs there is only information
        from the sources in the DataBlock.
        This also increments the generation_id of this DataBlock.

        TODO: Also update the header and the metadata information
        TODO: Make this threadsafe

        :rtype: :obj:`DataBlock`
        """

        self.logger.debug("datablock waiting for internal write lock in 'duplicate'")
        with self.__internal_data_write_lock:
            dup_datablock = copy.copy(self)
            self.generation_id += 1
            self.dataspace.duplicate_datablock(self.sequence_id, dup_datablock.generation_id, self.generation_id)
        return dup_datablock

    def is_expired(self, key=None):
        """
        Check if the dataproduct for a given key or any key is expired
        """
        self.logger.info("datablock is checking for expired dataproducts")

    def mark_expired(self, expiration_time):
        """
        Set the expiration_time for the current generation of the dataproduct
        and mark it as expired if expiration_time <= current time
        """
        self.logger.info("datablock is marking expired dataproducts")
