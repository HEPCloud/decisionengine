# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
    Code not written by us
"""
import os

import sqlalchemy
import structlog

from decisionengine.framework.modules.logging_configDict import LOGGERNAME

__all__ = ["orm_as_dict", "clone_model", "add_engine_pidguard"]


def orm_as_dict(obj):
    """Based on : https://stackoverflow.com/a/37350445"""
    return {c.key: getattr(obj, c.key) for c in sqlalchemy.inspect(obj).mapper.column_attrs}


def clone_model(model, **kwargs):
    """Based on https://stackoverflow.com/a/55991358"""
    # will raise AttributeError if data not loaded
    try:
        model.sequence_id  # taskmanager doesn't have an 'id' column
    except AttributeError:
        model.id  # pylint: disable=pointless-statement

    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.update(kwargs)

    return model.__class__(**data)


def add_engine_pidguard(engine):
    """
    Based on
    https://stackoverflow.com/questions/62920507/using-sqlalchemy-connection-pooling-queues-with-python-multiprocessing
    """
    structlog.getLogger(LOGGERNAME).debug(f"setting up add_engine_pidguard for {engine}")

    @sqlalchemy.event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        """
        Based on
        https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
        https://docs.sqlalchemy.org/en/14/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
        """
        if "sqlite" in str(type(dbapi_connection)):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA busy_timeout=5000")  # permit retrys for 5 seconds only
            cursor.close()
        connection_record.info["pid"] = os.getpid()

    @sqlalchemy.event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        """
        Based on
        https://docs.sqlalchemy.org/en/14/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
        """
        pid = os.getpid()
        if connection_record.info["pid"] != pid:
            connection_record.connection = connection_proxy.connection = None
            raise sqlalchemy.exc.DisconnectionError(
                f"Connection record belongs to pid {connection_record.info['pid']}, attempting to check out in pid {pid}"
            )
