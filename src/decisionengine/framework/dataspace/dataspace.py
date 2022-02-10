# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import importlib

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME
from decisionengine.framework.util.singleton import ScopedSingleton

__all__ = [
    "DataSpaceConfigurationError",
    "DataSpaceConnectionError",
    "DataSpaceError",
    "DataSpaceExistsError",
    "DataSpace",
]


logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


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


class DataSourceLoader(metaclass=ScopedSingleton):

    _ds = None

    @staticmethod
    def create_datasource(module_name, class_name, config):
        ds = DataSourceLoader._ds
        if not ds:
            py_module = importlib.import_module(module_name)
            logger.debug(f"in Dataspace, importlib has imported module {class_name}")
            clazz = getattr(py_module, class_name)
            ds = clazz(config)
        else:
            # There is a good chance we are forked off to another process
            # and already have cached connections, so reset the connections.
            ds.reset_connections()
        return ds


class DataSpace:
    """
    DataSpace class is collection of datablocks and provides interface
    to the database used to store the actual data
    """

    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """

        logger.debug("Initializing a dataspace")

        # Validate configuration
        if not config.get("dataspace"):
            logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError(
                "Configuration is missing dataspace information: dataspace key not found."
            )
        elif not isinstance(config.get("dataspace"), dict):
            logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError(
                "Invalid dataspace configuration: " "dataspace key must correspond to a dictionary"
            )
        try:
            self._db_driver_name = config["dataspace"]["datasource"]["name"]
            self._db_driver_module = config["dataspace"]["datasource"]["module"]
            self._db_driver_config = config["dataspace"]["datasource"]["config"]
        except KeyError:
            logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError("Invalid dataspace configuration")

        self.config = config

        # Connect to the datasource/database
        self.datasource = DataSourceLoader().create_datasource(
            self._db_driver_module, self._db_driver_name, self._db_driver_config
        )

        # Datablocks, current and previous, keyed by taskmanager_ids
        self.curr_datablocks = {}
        self.prev_datablocks = {}

    def __str__(self):  # pragma: no cover
        return f"{vars(self)}"

    def insert(self, taskmanager_id, generation_id, key, value, header, metadata):
        try:
            self.datasource.insert(taskmanager_id, generation_id, key, value, header, metadata)
        except Exception:  # pragma: no cover
            logger.exception("Error in dataspace insert!")
            raise

    def update(self, taskmanager_id, generation_id, key, value, header, metadata):
        try:
            self.datasource.update(taskmanager_id, generation_id, key, value, header, metadata)
        except Exception:  # pragma: no cover
            logger.exception("Error in dataspace update!")
            raise

    def get_datablock(self, taskmanager_id, generation_id):
        return self.datasource.get_datablock(taskmanager_id, generation_id)

    def get_dataproduct(self, taskmanager_id, generation_id, key):
        return self.datasource.get_dataproduct(taskmanager_id, generation_id, key)

    def get_dataproducts(self, taskmanager_id, key=None):
        return self.datasource.get_dataproducts(taskmanager_id, key)

    def get_header(self, taskmanager_id, generation_id, key):
        return self.datasource.get_header(taskmanager_id, generation_id, key)

    def get_metadata(self, taskmanager_id, generation_id, key):
        return self.datasource.get_metadata(taskmanager_id, generation_id, key)

    def duplicate_datablock(self, taskmanager_id, generation_id, new_generation_id):
        return self.datasource.duplicate_datablock(taskmanager_id, generation_id, new_generation_id)

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

    def store_taskmanager(self, name, taskmanager_id, datestamp=None):
        return self.datasource.store_taskmanager(name, taskmanager_id, datestamp)

    def get_last_generation_id(self, taskmanager_name, taskmanager_id=None):
        return self.datasource.get_last_generation_id(taskmanager_name, taskmanager_id)

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        return self.datasource.get_taskmanager(taskmanager_name, taskmanager_id)

    def get_taskmanagers(self, taskmanager_name=None, start_time=None, end_time=None):
        return self.datasource.get_taskmanagers(taskmanager_name, start_time, end_time)
