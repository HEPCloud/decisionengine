import importlib
import logging


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
            cls._instances[cls] = super().__call__(*args,
                                                   **kwargs)
        # Uncomment following to run __init__ everytime class is called
        # else:
        #     cls._instances[cls].__init__(*args, **kwargs)

        return cls._instances[cls]

class DataSourceLoader(object, metaclass=Singleton):

    _ds = None

    @staticmethod
    def create_datasource(module_name, class_name, config):
        ds = DataSourceLoader._ds
        if not ds:
            py_module = importlib.import_module(module_name)
            clazz = getattr(py_module, class_name)
            ds = clazz(config)
        return ds


class DataSpace():
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

        self.logger = logging.getLogger()
        self.logger.debug('Initializing a dataspace')

        # Validate configuration
        if not config.get('dataspace'):
            self.logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError('Configuration is missing dataspace information: dataspace key not found.')
        elif not isinstance(config.get('dataspace'), dict):
            self.logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError('Invalid dataspace configuration: '
                                              'dataspace key must correspond to a dictionary')
        try:
            self._db_driver_name = config['dataspace']['datasource']['name']
            self._db_driver_module = config['dataspace']['datasource']['module']
            self._db_driver_config = config['dataspace']['datasource']['config']
        except KeyError:
            self.logger.exception("Error in initializing DataSpace!")
            raise DataSpaceConfigurationError('Invalid dataspace configuration')

        self.datasource = DataSourceLoader().create_datasource(self._db_driver_module,
                                                               self._db_driver_name,
                                                               self._db_driver_config)

        # Datablocks, current and previous, keyed by taskmanager_ids
        self.curr_datablocks = {}
        self.prev_datablocks = {}

        # Connect to the database
        try:
            self.datasource.connect()
        except DataSpaceConnectionError:
            self.logger.exception('Cannot connect to the datasource!')
            raise

        # Create tables if not created
        if not DataSpace._tables_created:
            try:
                self.datasource.create_tables()
                DataSpace._tables_created = True
            except Exception:
                self.logger.exception('Cannot create datebase tables')
                raise

    def __str__(self):  # pragma: no cover
        return '%s' % vars(self)

    def insert(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        try:
            self.datasource.insert(taskmanager_id, generation_id, key,
                                   value, header, metadata)
        except Exception:
            self.logger.exception("Error in dataspace insert!")
            raise

    def update(self, taskmanager_id, generation_id, key,
               value, header, metadata):
        try:
            self.datasource.update(taskmanager_id, generation_id, key,
                                   value, header, metadata)
        except Exception:
            self.logger.exception("Error in dataspace update!")
            raise

    def get_dataproduct(self, taskmanager_id, generation_id, key):
        return self.datasource.get_dataproduct(taskmanager_id, generation_id, key)

    def get_dataproducts(self, taskmanager_id, key=None):
        return self.datasource.get_dataproducts(taskmanager_id, key)

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

    def store_taskmanager(self, name, taskmanager_id, datestamp=None):
        return self.datasource.store_taskmanager(name, taskmanager_id, datestamp)

    def get_last_generation_id(self,
                               taskmanager_name,
                               taskmanager_id=None):
        return self.datasource.get_last_generation_id(taskmanager_name,
                                                      taskmanager_id)

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        return self.datasource.get_taskmanager(taskmanager_name, taskmanager_id)

    def get_taskmanagers(self, taskmanager_name=None, start_time=None, end_time=None):
        return self.datasource.get_taskmanagers(taskmanager_name, start_time, end_time)
