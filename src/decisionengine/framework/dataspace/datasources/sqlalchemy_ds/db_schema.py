# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""
The table layout and utilities for our SQLAlchemy ORM
"""
from sqlalchemy import Column, ForeignKey, Index, sql, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.types import BigInteger, DateTime, Integer, LargeBinary, String, Text

__all__ = [
    "Base",
    "SessionMaker",
    "Schema",
    "Taskmanager",
    "Header",
    "Metadata",
    "Dataproduct",
]

Base = declarative_base()
SessionMaker = sessionmaker()

# sqlite doesn't like to make sequences out of BigInteger
# since we care about that for unit tests, make an alias
SBigInteger = BigInteger().with_variant(Integer, "sqlite")


class Schema(Base):
    """
    This table may not be in use

    Has a one-to-many relationship with:
     Header - may not be in use
    """

    __tablename__ = "schema"
    schema_id = Column(Integer, primary_key=True, index=True, unique=True)
    schema = Column(LargeBinary, nullable=False)

    # XXX:
    # don't seed relationship since we aren't using it
    # header = relationship("Header", backref='schema', cascade="all")


class Taskmanager(Base):
    """
    Has a one-to-many relationship with:
     Header
     Metadata
     Dataproduct

    changes cascade on:
     Header
     Metadata
     Dataproduct

    Existing code appears to depend on column order.
    """

    __tablename__ = "taskmanager"

    sequence_id = Column(SBigInteger, primary_key=True, index=True, unique=True, info="", comment="")
    taskmanager_id = Column(String(length=36), nullable=False, info="", comment="")
    name = Column(
        Text,
        nullable=False,
        info="",
        comment="most code calls this column taskmanager_name",
    )
    datestamp = Column(
        DateTime,
        server_default=sql.func.now(),
        nullable=False,
        info="",
        comment="",
    )

    # Indexes, etc
    __table_args__ = (
        Index("ix_taskmanager_taskmanager_id", "taskmanager_id", postgresql_using="hash"),
        Index("ix_taskmanager_name", "name", postgresql_using="hash"),
        Index(
            "ix_taskmanager_datestamp",
            "datestamp",
            postgresql_using="brin",
            postgresql_with={"autosummarize": "ON", "pages_per_range": 1024},
        ),
        UniqueConstraint("sequence_id", "taskmanager_id", name="uq_taskmanager_squence_id_taskmanager_id"),
    )

    task_header = relationship("Header", back_populates="taskmanager", cascade="delete")
    task_metadata = relationship("Metadata", back_populates="taskmanager", cascade="delete")
    task_dataproduct = relationship("Dataproduct", back_populates="taskmanager", cascade="delete")


class Header(Base):
    """
    The PRIMARY KEY on this table isn't used....

    The existing code has a hard expectation on the time
    columns being BIGINT rather than datetime objects
    buried within the classes.

    Looks like there was an initial goal of a relationship
     with the Schema table, but it may not be in use

    Existing code appears to depend on column order.
    """

    __tablename__ = "header"

    taskmanager_id = Column(
        ForeignKey("taskmanager.sequence_id", ondelete="CASCADE"),
        nullable=False,
        info="",
        comment="",
    )
    generation_id = Column(Integer, nullable=False, info="", comment="")
    key = Column(Text, nullable=False, info="", comment="")
    create_time = Column(BigInteger, nullable=False, info="", comment="")
    expiration_time = Column(BigInteger, nullable=False, info="", comment="")
    scheduled_create_time = Column(BigInteger, nullable=False, info="", comment="")
    creator = Column(Text, nullable=False, info="", comment="")
    schema_id = Column(Integer, info="", comment="")
    id = Column(SBigInteger, primary_key=True, index=True, unique=True, info="", comment="")

    taskmanager = relationship("Taskmanager", back_populates="task_header", passive_deletes=True)

    # Indexes, etc
    __table_args__ = (
        Index("ix_header_taskmanager_id", "taskmanager_id", postgresql_using="hash"),
        Index(
            "ix_header_generation_id",
            "generation_id",
        ),
        Index("ix_header_key", "key", postgresql_using="hash"),
        UniqueConstraint("taskmanager_id", "generation_id", "key", name="uq_header_taskmanager_id_generation_id_key"),
    )


class Metadata(Base):
    """
    The PRIMARY KEY on this table isn't used....

    The existing code has a hard expectation on the state
    field as a 'text' element.

    The existing code has a hard expectation on the time
    columns being BIGINT rather than datetime objects
    buried within the classes.

    Existing code appears to depend on column order.
    """

    __tablename__ = "metadata"

    taskmanager_id = Column(
        ForeignKey("taskmanager.sequence_id", ondelete="CASCADE"),
        nullable=False,
        info="",
        comment="",
    )
    generation_id = Column(Integer, nullable=False, info="", comment="")
    key = Column(Text, nullable=False, info="", comment="")
    state = Column(Text, nullable=False, info="", comment="")
    generation_time = Column(BigInteger, nullable=False, info="", comment="")
    missed_update_count = Column(Integer, default=0, info="", comment="")
    id = Column(SBigInteger, primary_key=True, index=True, unique=True, info="", comment="")

    taskmanager = relationship("Taskmanager", back_populates="task_metadata", passive_deletes=True)

    # Indexes, etc
    __table_args__ = (
        Index("ix_metadata_taskmanager_id", "taskmanager_id", postgresql_using="hash"),
        Index(
            "ix_metadata_generation_id",
            "generation_id",
        ),
        Index("ix_metadata_key", "key", postgresql_using="hash"),
        Index("ix_metadata_state", "state", postgresql_using="hash"),
        UniqueConstraint("taskmanager_id", "generation_id", "key", name="uq_metadata_taskmanager_id_generation_id_key"),
    )


class Dataproduct(Base):
    """
    The PRIMARY KEY on this table isn't used....

    Existing code appears to depend on column order.
    """

    __tablename__ = "dataproduct"

    taskmanager_id = Column(
        ForeignKey("taskmanager.sequence_id", ondelete="CASCADE"),
        nullable=False,
        info="",
        comment="",
    )
    generation_id = Column(Integer, nullable=False, info="", comment="")
    key = Column(Text, nullable=False, info="", comment="")
    value = Column(LargeBinary, nullable=False, info="", comment="")
    id = Column(SBigInteger, primary_key=True, index=True, unique=True, info="", comment="")

    taskmanager = relationship("Taskmanager", back_populates="task_dataproduct", passive_deletes=True)

    # Indexes, etc
    __table_args__ = (
        Index("ix_dataproduct_taskmanager_id", "taskmanager_id", postgresql_using="hash"),
        Index(
            "ix_dataproduct_generation_id",
            "generation_id",
        ),
        Index("ix_dataproduct_key", "key", postgresql_using="hash"),
        UniqueConstraint(
            "taskmanager_id", "generation_id", "key", name="uq_dataproduct_taskmanager_id_generation_id_key"
        ),
    )
