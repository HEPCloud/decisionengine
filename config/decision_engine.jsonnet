{
  logger: {
    log_file: "/var/log/decisionengine/decision_engine_log",
    max_file_size: 200000000,
    max_backup_count: 6,
    log_level: "DEBUG",
    global_channel_log_level: "DEBUG",
  },

  broker_url: "redis://localhost:6379/0",

  channels: "/etc/decisionengine/config.d",

  dataspace: {
    reaper_start_delay_seconds: 1818,
    retention_interval_in_days: 365,
    datasource: {
      module: "decisionengine.framework.dataspace.datasources.sqlalchemy_ds",
      name: "SQLAlchemyDS",
      config: {
        url: "postgresql://postgres:@localhost/decisionengine",
      },
    },
  },

  webserver: {
    port: 8000,
  },

}
