{
  logger: {
    log_file: "/tmp/decisionengine.log",
    max_file_size: 200000000,
    max_backup_count: 6,
    rotation_time_unit: "D",
    rotation_time_interval: 1,
    file_rotate_by: "size",
    log_level: "DEBUG",
    global_channel_log_level: "DEBUG",
    global_source_log_level: "DEBUG",
    start_q_logger: "False",
  },

  server_address: ["localhost", 8888],
  shutdown_timeout: 10,

  dataspace: {
    reaper_start_delay_seconds: 1818,
    retention_interval_in_days: 370,

    datasource: {
      module: "decisionengine.framework.dataspace.datasources.sqlalchemy_ds",
      name: "SQLAlchemyDS",
      config: {
        url: "postgresql://postgres:@localhost/decisionengine",
      },
    },
  },
}
