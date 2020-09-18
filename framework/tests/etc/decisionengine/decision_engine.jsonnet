{
  'logger' : {
    'log_file': '/tmp/decisionengine.log',
    'max_file_size': 200*1000000,
    'max_backup_count': 6,
    'log_level': "WARNING",
    'global_channel_log_level':"WARNING",
  },

  'server_address' : ["localhost",8888],
  'shutdown_timeout' : 10,

  'dataspace': {
    'reaper_start_delay_seconds': 1818,
    'retention_interval_in_days': 370,

    'datasource' : {
      'module' : 'decisionengine.framework.dataspace.datasources.postgresql',
      'name' : 'Postgresql',
      'config' : {
        'user' : 'postgres',
        'blocking' : true,
        'host' : 'localhost',
        'port' : 5432,
        'database' : 'decisionengine',
        'maxconnections' : 100,
        'maxcached' : 10
      }
    }
  }
}
