DROP INDEX IF EXISTS i_taskmanager_datestamp;
DROP INDEX IF EXISTS i_taskmanager_sequence;
DROP INDEX IF EXISTS i_taskmanager_taskmanager_id;
DROP TABLE IF EXISTS taskmanager;
CREATE TABLE taskmanager (
   sequence_id BIGSERIAL,
   taskmanager_id character varying(36),
   name text,
   datestamp timestamp with time zone default NOW()
);

ALTER TABLE ONLY taskmanager
      ADD CONSTRAINT pk_taskmanager PRIMARY KEY (sequence_id);

CREATE INDEX i_taskmanager_datestamp ON taskmanager using BRIN (datestamp);
CREATE INDEX i_taskmanager_sequence ON taskmanager(sequence_id);
CREATE INDEX i_taskmanager_taskmanager_id ON taskmanager using HASH (taskmanager_id);

DROP INDEX IF EXISTS i_header_taskmanager_id;
DROP INDEX IF EXISTS i_header_generation_id;
DROP INDEX IF EXISTS i_header_key;
DROP TABLE IF EXISTS header;
CREATE TABLE header (
    taskmanager_id BIGINT,
    generation_id INTEGER,
    key TEXT,
    create_time BIGINT,
    expiration_time BIGINT,
    scheduled_create_time BIGINT,
    creator TEXT,
    schema_id BIGINT
    );

ALTER TABLE ONLY header
    ADD CONSTRAINT header_taskmanager_id_fkey FOREIGN KEY (taskmanager_id)
    REFERENCES taskmanager(sequence_id)
    ON UPDATE CASCADE ON DELETE CASCADE;

CREATE INDEX i_header_taskmanager_id ON header(taskmanager_id);
CREATE INDEX i_header_generation_id ON header(generation_id);
CREATE INDEX i_header_key ON header using HASH (generation_id);

DROP TABLE IF EXISTS schema;
CREATE TABLE schema (
    schema_id SERIAL,
    schema BYTEA
    );

DROP INDEX IF EXISTS i_metadata_taskmanager_id;
DROP INDEX IF EXISTS i_metadata_generation_id;
DROP INDEX IF EXISTS i_metadata_key;
DROP TABLE IF EXISTS metadata;
CREATE TABLE metadata (
    taskmanager_id BIGINT,
    generation_id INTEGER,
    key TEXT,
    state TEXT,
    generation_time BIGINT,
    missed_update_count INTEGER
    );

ALTER TABLE ONLY metadata
    ADD CONSTRAINT metadata_taskmanager_id_fkey FOREIGN KEY (taskmanager_id)
    REFERENCES taskmanager(sequence_id)
    ON UPDATE CASCADE ON DELETE CASCADE;

CREATE INDEX i_metadata_taskmanager_id ON metadata(taskmanager_id);
CREATE INDEX i_metadata_generation_id ON metadata(generation_id);
CREATE INDEX i_metadata_key ON metadata using HASH (generation_id);

DROP INDEX IF EXISTS i_dataproduct_taskmanager_id;
DROP INDEX IF EXISTS i_dataproduct_generation_id;
DROP INDEX IF EXISTS i_dataproduct_key;
DROP TABLE IF EXISTS dataproduct;
CREATE TABLE dataproduct (
    taskmanager_id BIGINT,
    generation_id INTEGER,
    key TEXT,
    value BYTEA
    );

ALTER TABLE ONLY dataproduct
    ADD CONSTRAINT dataproduct_taskmanager_id_fkey FOREIGN KEY (taskmanager_id)
    REFERENCES taskmanager(sequence_id)
    ON UPDATE CASCADE ON DELETE CASCADE;

CREATE INDEX i_dataproduct_taskmanager_id ON dataproduct(taskmanager_id);
CREATE INDEX i_dataproduct_generation_id ON dataproduct(generation_id);
CREATE INDEX i_dataproduct_key ON dataproduct using HASH (generation_id);

DROP FUNCTION IF EXISTS f_id2sequence;
CREATE FUNCTION f_id2sequence(character varying) RETURNS BIGINT
    LANGUAGE sql
    AS $_$
                SELECT sequence_id FROM taskmanager WHERE taskmanager_id = $1;
            $_$;


DROP FUNCTION IF EXISTS f_get_current_task_sequence;
CREATE FUNCTION f_get_current_task_sequence(character varying) RETURNS BIGINT
    LANGUAGE sql
    AS $_$
                SELECT max(sequence_id) FROM taskmanager WHERE name = $1;
            $_$;

DROP FUNCTION IF EXISTS f_get_current_task_id;
CREATE FUNCTION f_get_current_task_id(character varying) RETURNS CHARACTER VARYING
    LANGUAGE sql
    AS $_$
                SELECT taskmanager_id FROM taskmanager
		WHERE sequence_id  = f_get_current_task_sequence($1);
            $_$;
