{
  logger: {
    log_file: "/var/log/decisionengine/decision_engine_log",
    max_file_size: 200000000,
    max_backup_count: 6,
    log_level: "DEBUG",
    global_channel_log_level: "DEBUG",
  },

  channels: "/etc/decisionengine/config.d",

  dataspace: {
    reaper_start_delay_seconds: 1818,
    retention_interval_in_days: 365,
    datasource: {
      module: "decisionengine.framework.dataspace.datasources.postgresql",
      name: "Postgresql",
      config: {
        user: "postgres",
        blocking: true,
        host: "localhost",
        port: 5432,
        database: "decisionengine",
        maxconnections: 100,
        maxcached: 10,
      },
    },
  },

  webserver: {
    port: 8000,
  },

}
