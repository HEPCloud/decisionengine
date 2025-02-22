# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
The datasource layer for our abstraction
"""
import datetime

import sqlalchemy
import sqlalchemy.sql as sql
import structlog

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import scoped_session

import decisionengine.framework.dataspace.datasource as ds

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

from . import db_schema
from .utils import add_engine_pidguard, clone_model, orm_as_dict

__all__ = [
    "SQLAlchemyDS",
]

# setup queue hooks
add_engine_pidguard(sqlalchemy.pool.QueuePool)


class SQLAlchemyDS(ds.DataSource):
    """
    A DecisionEngine data source via the SQL Alchemy ORM

    .. code-block:: python

        {
            "dataspace": {
                "datasource": {
                    "module": "decisionengine.framework.dataspace.datasources.sqlalchemy_ds",
                    "name": "SQLAlchemyDS",
                    "params": {
                        "pool_size": 5,
                        "max_overflow": 10,
                        "timeout": 30,

                        # url is mandatory, but any `engine` keyword is accepted here.
                        "url": "dialect[+driver]://user:password@host/dbname"
                    }
                }
            }
        }

    Exceptions should be caught and logged by the caller.
    """

    def __init__(self, config_dict):
        super().__init__(config_dict)
        self.logger = structlog.getLogger(LOGGERNAME)
        self.logger = self.logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)

        if "echo" in config_dict and config_dict["echo"]:
            self.logger.debug(f"Initializing a SQLAlchemyDS datasource: {config_dict}")
        else:  # pragma: no cover
            # unit testing in "echo" mode for ease of debugging
            self.logger.debug("Initializing a SQLAlchemyDS datasource")

        self.config_dict = config_dict
        self.config_dict["future"] = True  # force 2.0 behavior
        self.engine = None
        self.sessionmaker = db_schema.SessionMaker

        self.connect()
        self.create_tables()

        # thread safe sessions
        self.session = scoped_session(self.sessionmaker)

    def create_tables(self):
        """
        Create database tables

        Returns:
            None
        """
        self.logger.info("datasource SQLAlchemyDS is creating the database tables (if needed)")

        # this is not smart enough to manage schema migrations
        db_schema.Base.metadata.create_all(bind=self.engine)

        self.logger.debug("datasource SQLAlchemyDS done creating the database tables")

    def store_taskmanager(self, name, taskmanager_id, datestamp=None):
        """
        Store TaskManager in database

        Args:
            name (str): name of taskmanager to retrieve
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            datestamp (datetime): datetime of created object, defaults to 'now'

        Returns:
            int: the primary key of the row in the database
        """
        my_tm = db_schema.Taskmanager(name=name, taskmanager_id=taskmanager_id)
        if datestamp:
            my_tm.datestamp = datestamp
        with self.session() as session:
            session.add(my_tm)
            session.commit()
            session.refresh(my_tm)

        return my_tm.sequence_id

    def get_taskmanager(self, taskmanager_name, taskmanager_id=None):
        """
        Find the task manager by name/uuid in the database
        get back the primary key.

        If multiples match, find highest primary key.

        Args:
            taskmanager_name (str): name of taskmanager to retrieve
            taskmanager_id (str/uuid): id of taskmanager to retrieve

        Returns:
            dict: the matching row, column names as keys
        """
        with self.session() as session:
            query = session.query(db_schema.Taskmanager).filter(db_schema.Taskmanager.name == taskmanager_name)

            if taskmanager_id:
                query = query.filter(db_schema.Taskmanager.taskmanager_id == taskmanager_id)
            else:
                max_id = (
                    session.query(sql.func.max(db_schema.Taskmanager.sequence_id).label("sequence_id"))
                    .filter(db_schema.Taskmanager.name == taskmanager_name)
                    .cte()
                )
                query = query.filter(db_schema.Taskmanager.sequence_id == max_id.c.sequence_id)

            return orm_as_dict(query.one())

    def get_taskmanagers(self, taskmanager_name=None, start_time=None, end_time=None):
        """
        Find taskmanagers that meet our search

        Args:
            taskmanager_name (str): name of taskmanager to retrieve
            start_time (datetime): Datetime to confine against
            end_time (datetime): Datetime to confine against

        Returns:
            list: each element is a dict() matching row, column names as keys
        """
        with self.session() as session:
            query = session.query(db_schema.Taskmanager).order_by(db_schema.Taskmanager.datestamp)

            if taskmanager_name:
                query = query.filter(db_schema.Taskmanager.name == taskmanager_name)
            if start_time:
                query = query.filter(db_schema.Taskmanager.datestamp >= start_time)
            if end_time:
                query = query.filter(db_schema.Taskmanager.datestamp <= end_time)

            return list(map(orm_as_dict, query.all()))

    def get_last_generation_id(self, taskmanager_name, taskmanager_id=None):
        """
        Return last generation id for current task manager
        or taskmanager w/ task_manager_id.

        Args:
            taskmanager_name (str): name of taskmanager to retrieve
            taskmanager_id (str/uuid): id of taskmanager to retrieve

        Returns:
            int: the largest generation stored within the database
        """
        with self.session() as session:
            query = (
                session.query(sql.func.max(db_schema.Dataproduct.generation_id).label("generation_id"))
                .join(db_schema.Taskmanager)
                .filter(db_schema.Taskmanager.name == taskmanager_name)
            )

            if taskmanager_id:
                query = query.filter(db_schema.Taskmanager.taskmanager_id == taskmanager_id)

            result = query.scalar()
            if result is None:
                raise NoResultFound("No matching entries found")
            return result

    def insert(self, taskmanager_id, generation_id, key, value, header, metadata):
        """
        Insert data into respective tables for the given
        taskmanager_id, generation_id, key

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to create
            key (str): key for the value
            value (obj): Value can be an object or dict or a binary
            header (datablock.Header): Header for the value
            metadata (datablock.Metadata): Metadata for the value

        Returns:
            None
        """
        my_dataproduct = db_schema.Dataproduct(
            taskmanager_id=taskmanager_id,
            generation_id=generation_id,
            key=key,
            value=value,
        )
        my_header = db_schema.Header(
            taskmanager_id=taskmanager_id,
            generation_id=generation_id,
            key=key,
            create_time=header.get("create_time"),
            scheduled_create_time=header.get("scheduled_create_time"),
            expiration_time=header.get("expiration_time"),
            creator=header.get("creator"),
            schema_id=header.get("schema_id"),
        )
        my_metadata = db_schema.Metadata(
            taskmanager_id=taskmanager_id,
            generation_id=generation_id,
            key=key,
            state=metadata.get("state"),
            generation_time=metadata.get("generation_time"),
            missed_update_count=metadata.get("missed_update_count"),
        )

        with self.session() as session:
            session.add_all([my_dataproduct, my_header, my_metadata])
            session.commit()
            session.refresh(my_dataproduct)
            session.refresh(my_header)
            session.refresh(my_metadata)

    def update(self, taskmanager_id, generation_id, key, value, header, metadata):
        """
        Update the data in respective tables for the given
        taskmanager_id, generation_id, key

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to update
            key (str): key for the value
            value (obj): Value can be an object or dict or a binary
            header (datablock.Header): Header for the value
            metadata (datablock.Metadata): Metadata for the value

        Returns:
            None
        """
        # fetch the records
        with self.session() as session:
            my_dataproduct = (
                session.query(db_schema.Dataproduct)
                .filter(db_schema.Dataproduct.taskmanager_id == taskmanager_id)
                .filter(db_schema.Dataproduct.generation_id == generation_id)
                .filter(db_schema.Dataproduct.key == key)
                .one()
            )
            my_header = (
                session.query(db_schema.Header)
                .filter(db_schema.Header.taskmanager_id == taskmanager_id)
                .filter(db_schema.Header.generation_id == generation_id)
                .filter(db_schema.Header.key == key)
                .one()
            )
            my_metadata = (
                session.query(db_schema.Metadata)
                .filter(db_schema.Metadata.taskmanager_id == taskmanager_id)
                .filter(db_schema.Metadata.generation_id == generation_id)
                .filter(db_schema.Metadata.key == key)
                .one()
            )

        # update the attribs

        # dataproduct
        my_dataproduct.value = value

        # header
        my_header.create_time = header.get("create_time", my_header.create_time)
        my_header.expiration_time = header.get("expiration_time", my_header.expiration_time)
        my_header.scheduled_create_time = header.get("scheduled_create_time", my_header.scheduled_create_time)
        my_header.creator = header.get("creator", my_header.creator)
        my_header.schema_id = header.get("schema_id", my_header.schema_id)

        # metadata
        my_metadata.state = metadata.get("state", my_metadata.state)
        my_metadata.generation_time = metadata.get("generation_time", my_metadata.generation_time)
        my_metadata.missed_update_count = metadata.get("missed_update_count", my_metadata.missed_update_count)

        # save the changes and validate we can fetch the results
        with self.session() as session:
            session.add_all([my_dataproduct, my_header, my_metadata])
            session.commit()
            session.refresh(my_dataproduct)
            session.refresh(my_header)
            session.refresh(my_metadata)

    def get_header(self, taskmanager_id, generation_id, key):
        """
        Return the header from the header table for the given
        taskmanager_id, generation_id, key

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to locate
            key (str): key for the value

        Returns:
            tuple: fields in order are:
                   taskmanager.taskmanager_id,
                   header.taskmanager_id,
                   header.generation_id,
                   header.key,
                   header.create_time,
                   header.expiration_time,
                   header.scheduled_create_time,
                   header.creator,
                   header.schema_id
        """
        with self.session() as session:
            my_header = (
                session.query(
                    db_schema.Taskmanager.taskmanager_id.label("tm_uuid"),
                    db_schema.Header.taskmanager_id,
                    db_schema.Header.generation_id,
                    db_schema.Header.key,
                    db_schema.Header.create_time,
                    db_schema.Header.expiration_time,
                    db_schema.Header.scheduled_create_time,
                    db_schema.Header.creator,
                    db_schema.Header.schema_id,
                )
                .join(db_schema.Taskmanager)
                .filter(db_schema.Header.taskmanager_id == taskmanager_id)
                .filter(db_schema.Header.generation_id == generation_id)
                .filter(db_schema.Header.key == key)
                .one()
            )

        return (
            my_header.tm_uuid,
            my_header.taskmanager_id,
            my_header.generation_id,
            my_header.key,
            my_header.create_time,
            my_header.expiration_time,
            my_header.scheduled_create_time,
            my_header.creator,
            my_header.schema_id,
        )

    def get_metadata(self, taskmanager_id, generation_id, key):
        """
        Return the metadata from the metadata table for the given
        taskmanager_id, generation_id, key

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to locate
            key (str): key for the value

        Returns:
            tuple: fields in order are:
                   taskmanager.taskmanager_id,
                   metadata.taskmanager_id,
                   metadata.generation_id,
                   metadata.key,
                   metadata.state,
                   metadata.generation_time,
                   metadata.missed_update_count
        """
        with self.session() as session:
            my_metadata = (
                session.query(
                    db_schema.Taskmanager.taskmanager_id.label("tm_uuid"),
                    db_schema.Metadata.taskmanager_id,
                    db_schema.Metadata.generation_id,
                    db_schema.Metadata.key,
                    db_schema.Metadata.state,
                    db_schema.Metadata.generation_time,
                    db_schema.Metadata.missed_update_count,
                )
                .join(db_schema.Taskmanager)
                .filter(db_schema.Metadata.taskmanager_id == taskmanager_id)
                .filter(db_schema.Metadata.generation_id == generation_id)
                .filter(db_schema.Metadata.key == key)
                .one()
            )

        return (
            my_metadata.tm_uuid,
            my_metadata.taskmanager_id,
            my_metadata.generation_id,
            my_metadata.key,
            my_metadata.state,
            my_metadata.generation_time,
            my_metadata.missed_update_count,
        )

    def get_dataproducts(self, taskmanager_id, key=None):
        """
        Return list of all data products associated with
        with taskmanager_id

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            key (str): key for the value

        Returns:
            tuple: each element is the matching row as a dict()
        """
        with self.session() as session:
            query = (
                session.query(
                    db_schema.Dataproduct.taskmanager_id,
                    db_schema.Dataproduct.generation_id,
                    db_schema.Dataproduct.key,
                    db_schema.Dataproduct.value,
                )
                .filter(db_schema.Dataproduct.taskmanager_id == taskmanager_id)
                .order_by(db_schema.Dataproduct.id)
            )

            if key:
                query = query.filter(db_schema.Dataproduct.key == key)

            rows = []
            for row in query.all():
                rows.append(
                    {
                        "generation_id": row.generation_id,
                        "key": row.key,
                        "taskmanager_id": row.taskmanager_id,
                        "value": row.value,
                    }
                )
            return rows

    def get_dataproduct(self, taskmanager_id, generation_id, key):
        """
        Return the data from the dataproduct table for the given
        taskmanager_id, generation_id, key

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to locate
            key (str): key for the value

        Returns:
            obj: The possibly binary value stored earlier
        """
        try:
            with self.session() as session:
                my_dataproduct = (
                    session.query(db_schema.Dataproduct.value)
                    .filter(db_schema.Dataproduct.taskmanager_id == taskmanager_id)
                    .filter(db_schema.Dataproduct.generation_id == generation_id)
                    .filter(db_schema.Dataproduct.key == key)
                    .one()
                )
        except NoResultFound as __e:
            raise KeyError("Converted to implementation agnostic exception").with_traceback(__e.__traceback__)

        return my_dataproduct.value

    def get_datablock(self, taskmanager_id, generation_id):
        """
        Return the entire datablock from the dataproduct table for the given
        taskmanager_id, generation_id

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to locate

        Returns:
            dict: with all set keys and their associated values
        """
        with self.session() as session:
            rows = (
                session.query(db_schema.Dataproduct.key, db_schema.Dataproduct.value)
                .filter(db_schema.Dataproduct.taskmanager_id == taskmanager_id)
                .filter(db_schema.Dataproduct.generation_id == generation_id)
                .all()
            )

        datablock = {}
        for row in rows:
            datablock[row.key] = row.value

        return datablock

    def duplicate_datablock(self, taskmanager_id, generation_id, new_generation_id):
        """
        For the given taskmanager_id, make a copy of the datablock with given
        generation_id, set the generation_id for the datablock copy

        Args:
            taskmanager_id (str/uuid): id of taskmanager to retrieve
            generation_id (int): generation id to clone
            new_generation_id (int): generation id to create

        Returns:
            None
        """

        existing_blocks = []

        # fetch the records
        with self.session() as session:
            existing_blocks.extend(
                session.query(db_schema.Dataproduct)
                .filter(db_schema.Dataproduct.taskmanager_id == taskmanager_id)
                .filter(db_schema.Dataproduct.generation_id == generation_id)
                .all()
            )
            existing_blocks.extend(
                session.query(db_schema.Header)
                .filter(db_schema.Header.taskmanager_id == taskmanager_id)
                .filter(db_schema.Header.generation_id == generation_id)
                .all()
            )
            existing_blocks.extend(
                session.query(db_schema.Metadata)
                .filter(db_schema.Metadata.taskmanager_id == taskmanager_id)
                .filter(db_schema.Metadata.generation_id == generation_id)
                .all()
            )

        new_blocks = []

        # match content with new generation id
        for block in existing_blocks:
            new_blocks.append(clone_model(block, generation_id=new_generation_id))

        # save the new records and validate we can fetch the results
        with self.session() as session:
            session.add_all(new_blocks)
            session.commit()
            map(session.refresh, existing_blocks)

    def delete_data_older_than(self, days):
        """
        Delete data older that interval

        Args:
            days (int): remove data older than this many days

        Returns:
            None
        """
        if days <= 0:
            # do not log stack trace, Exception thrown is handled by the caller
            raise ValueError(f"Argument has to be positive, non zero integer. Supplied {days}")

        to_old = datetime.datetime.now() - datetime.timedelta(days=days)
        with self.session() as session:
            session.query(db_schema.Taskmanager).filter(db_schema.Taskmanager.datestamp < to_old).delete(
                synchronize_session=False
            )
            session.commit()

    def close(self):
        """
        Close all connections to the database

        Returns:
            None
        """
        self.logger.debug("Terminating a SQLAlchemyDS datasource")
        self.engine.dispose()

    def reset_connections(self):
        """
        Reset the connection to the database.
        So long as self.engine isn't undef, the engine can still
        make new connections if new db actions happen.
        It just won't have any open at this time.

        Returns:
            None
        """
        self.logger.debug("Resetting the SQLAlchemyDS database connections")
        self.engine.dispose()

    def connect(self):
        """
        Create a pool of database connections

        Returns:
            None
        """
        # sqlite doesn't support the QueuePool connection class
        poolclass = sqlalchemy.pool.QueuePool
        if self.config_dict["url"].startswith("sqlite:/"):
            poolclass = sqlalchemy.pool.NullPool
        self.engine = sqlalchemy.create_engine(**self.config_dict, poolclass=poolclass)
        add_engine_pidguard(self.engine)
        self.logger.debug(
            f"Trying to connect as {self.engine.url.drivername}://{self.engine.url.username}@{self.engine.url.host}:{self.engine.url.port}/{self.engine.url.database}"
        )
        self.sessionmaker.configure(bind=self.engine)

    def get_schema(self, table=None):
        """
        Given the table name return it's schema
        """
        raise NotImplementedError("This doesn't seem to be used")
