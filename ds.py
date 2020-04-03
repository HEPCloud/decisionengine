import threading
import time
import decisionengine.framework.dataspace.dataspace as dataspace


_MIN_RETENTION_INTERVAL_DAYS = 7

class Reaper(object):
    """
    Reaper provides functionality of periodic deletion
    of data
    """

    def __init__(self, config):
        """
        :type config: :obj:`dict`
        :arg config: Configuration dictionary
        """
        # Validate configuration
        if not config.get('dataspace'):
            raise dataspacce.DataSpaceConfigurationError('Configuration is missing dataspace information: dataspace key not found.')
        elif not isinstance(config.get('dataspace'), dict):
            raise dataspace.DataSpaceConfigurationError('Invalid dataspace configuration: '
                                                        'dataspace key must correspond to a dictionary')
        try:
            self._db_driver_name = config['dataspace']['datasource']['name']
            self._db_driver_module = config['dataspace']['datasource']['module']
            self._db_driver_config = config['dataspace']['datasource']['config']
            self.retention_interval = config['dataspace'].get('retention_interval_in_days', 0)
            if self.retention_interval < _MIN_RETENTION_INTERVAL_DAYS:
                raise ValueError("For safety the data retention interval has to be greater than {} days".
                                 format(_MIN_RETENTION_INTERVAL_DAYS))
        except KeyError as e:
            raise dataspace.DataSpaceConfigurationError('Invalid dataspace configuration: {}'.format(e))

        self.datasource = dataspace.DataSourceLoader().create_datasource(self._db_driver_module,
                                                                         self._db_driver_name,
                                                                         self._db_driver_config)

        self.stop_event = threading.Event()
        self.thread = None
        self.state = "IDLE"
        self.state_lock = threading.Lock()
                              
    def set_state(self, value):
        with self.state_lock:
            self.state = value

    def get_state(self):
        with self.state_lock:
            return self.state

    def reap(self):
        self.set_state("RUNNING")
        self.datasource.delete_old_data(self.retention_interval)

    def reaper_loop(self):
        while not self.stop_event:
            self.reap()
            self.set_state("SLEEPING")
            time.sleep(86400)
        else:
            self.set_state("STOPPED")

    def start(self):
        if not self.thread:
            self.thread = threading.Thread(group=None,
                                           target=self.reaper_loop,
                                           name="Reaper_loop_thread")
            self.thread.start()
    
    def stop(self):
        if self.thread and self.thread.isAlive() and not self.stop_event:
            self.stop_event.set()
            self.set_state("STOPPING")
            try:
                self.thread.join()
            finally:
                self.thread = None
                self.stop_event.clear()

    def __repr__(self):
        return "Reaper, retention interval {}, state {}".format(self.retention_interval,
                                                                 self.get_state())

    
        
import decisionengine.framework.configmanager.ConfigManager as Conf_Manager

if __name__ == "__main__":
    conf_manager = Conf_Manager.ConfigManager()
    conf_manager.load()
    reaper = dataspace.Reaper(config_manager.get_global_config())
