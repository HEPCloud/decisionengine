.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Installing and running HEPCloud's Decision Engine on EL8
========================================================

Decision engine uses a PostgreSQL database back-end and Redis as message broker and cache.

You need to install first PostgreSQL, Redis, and then the Decision engine framework (decisionengine) and install and add the standard channels (decisionengine_modules).

The following instructions assume a system installation, performed as ``root``.
decisionengine will run as the decisionengine user.


Install PostgreSQL
------------------

The default postgresql installed on RH8 is 9.2 which is outdated. Suggest to remove it and install 12 instead :

1. Disable the built-in PostgreSQL module ::

    sudo dnf -qy module disable postgresql

2. Install postgresql 12 ::

    dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
    dnf install -y postgresql12 postgresql12-server
    # optional, also: postgresql12-devel

3. Enable postgresql ::

    systemctl enable postgresql-12

4. Init the database ::

    /usr/pgsql-12/bin/postgresql-12-setup initdb

5. edit ``/var/lib/pgsql/12/data/pg_hba.conf`` like the following::

    [root@fermicloud371 ~]# diff  /var/lib/pgsql/12/data/pg_hba.conf~ /var/lib/pgsql/12/data/pg_hba.conf
    80c80
    < local   all             all                                     peer
    ---
    > local   all             all                                     trust
    82c82
    < host    all             all             127.0.0.1/32            ident
    ---
    > host    all             all             127.0.0.1/32            trust
    84c84
    < host    all             all             ::1/128                 ident
    ---
    > host    all             all             ::1/128                 trust


   This is setting the authentication method to `trust`

6. start the database ::

    systemctl start postgresql-12

7. create decisionengine ::

    createdb -U postgres decisionengine

The schema and the connection will be created and configured during the Decision engine framework installation.

To use the database you have to add it to the environment::

    export PG_VERSION=12
    export PATH="/usr/pgsql-${PG_VERSION}/bin:~/.local/bin:$PATH"
    # you may also add these lines to ~/.bashrc


Install Redis
-------------

Install and start the message broker (Redis) container on your system. You can find more details on the :doc:`redis document <redis>`

1. Install Padman ::

    dnf install -y podman

2. Run the Redis container ::

    podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning
    # When prompted to select an image, pick "docker.io/library/redis:6".


Install Decision Engine and the standard modules
------------------------------------------------

1. Prerequisites setup. Make sure that the required packages (python39, gcc, ...) are installed and up to date. ::

    # gcc, swig and make are needed for dependencies (jsonnet)
    dnf install python39 python39-pip python39-setuptools python39-wheel \
        gcc gcc-c++ make \
        python39-devel swig openssl-devel git rpm-build
    python3.9 -m pip install --upgrade --user pip
    python3.9 -m pip install --upgrade --user setuptools wheel setuptools-scm[toml]

    # To install the modules you will also need GlideinWMS Frontend, which is in the OSG repository.
    # Assuming the use of OSG 3.6, here is a brief summary of the setup:
    dnf install -y https://repo.opensciencegrid.org/osg/3.6/osg-3.6-el8-release-latest.rpm
    # HTCondor 8.9.x or 9.x, required by GlideinWMS, is in the osg-upcoming repository. It should be enabled to find the dependency
    # GlideinWMS 3.9.x is in osg-contrib. The repository should be enabled to find the dependency
    # In both the following files set: enabled=1
    vi /etc/yum.repos.d/osg-upcoming.repo
    vi /etc/yum.repos.d/osg-contrib.repo
    # Change the Epel repository priority to make sure that comes after the OSG repositories, which are 98. Make sure that epel has:
    priority=99
    vi /etc/yum.repos.d/epel.repo

  The complete version of the GlideinWMS installation instructions is available `here<https://opensciencegrid.org/docs/other/install-gwms-frontend/>`.
  For a minimal installation, you can use the following command:

    dnf install glideinwms-vofrontend-libs glideinwms-vofrontend-glidein glideinwms-userschedd glideinwms-usercollector

2. Setup the decision engine user and git repositories ::

    useradd decisionengine
    sudo -u decisionengine git clone https://github.com/HEPCloud/decisionengine.git ~decisionengine/decisionengine
    sudo -u decisionengine git clone https://github.com/HEPCloud/decisionengine_modules.git ~decisionengine/decisionengine_modules

3. Install the decision engine from the git repositories ::

    # Install the decisionengine framework and modules using setuptools
    su - decisionengine
    pushd decisionengine
    python3.9 setup.py develop --user
    popd
    pushd decisionengine_modules
    python3.9 setup.py develop --user
    popd
    exit

    # Create the required system files and directories (as root)
    mkdir /etc/decisionengine
    mkdir /var/log/decisionengine/
    cp ~decisionengine/decisionengine/config/decision_engine.jsonnet /etc/decisionengine
    cp -r ~decisionengine/decisionengine/src/decisionengine/framework/tests/etc/decisionengine/config.d /etc/decisionengine
    chown -R decisionengine:decisionengine /etc/decisionengine
    chown -R decisionengine:decisionengine /var/log/decisionengine

Now you can type ``decisionengine --help`` while logged in as decisionengine to print the help message.
To do more you need first to configure Decision Engine.


Configure Decision Engine
-------------------------

The default configuration file lives in ``/etc/decisionengine/decision_engine.jsonnet``.

A number of defaults are set for you.

Selecting your datasource
~~~~~~~~~~~~~~~~~~~~~~~~~

You need a datasource to store in the database the channel's data (datablocks).
Each datasource has its own unique schema and cannot be used with a different datasource.

**The SQLAlchemy Data Source**

SQLAlchemy is the default Data Source after v1.7 and is setup with a configuration like::

    "datasource": {
      "module": "decisionengine.framework.dataspace.datasources.sqlalchemy_ds",
      "name": "SQLAlchemyDS",
      "config": {
        "url": "postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_dbname}",
        }
      }

Any extra keywords you can pass to the ``sqlalchemy.engine.Engine`` constructor may be set under ``config``.

SQLAlchemy will create any tablespace objects it requires automatically.


**The PostgreSQL Data Source**

The postgresql Data Source is the only one supported pre v1.7 and is setup with a config like::

    "datasource": {
      "module": "decisionengine.framework.dataspace.datasources.postgresql",
     "name": "Postgresql",
      "config": {
        "user": "postgres",
        "blocking": true,
        "host": "localhost",
        "port": 5432,
        "database": "decisionengine",
        "maxconnections": 100,
        "maxcached": 10
        }
      }

If you use this datasource you must also load the database schema by hand.
To load the database schema run::

    psql -U postgres decisionengine -f /usr/share/doc/decisionengine/datasources/postgresql.sql


Start decision engine
---------------------

Start the service ::

    # As decisionengine user
    decisionengine --no-webserver &


Add channels to decision engine
-------------------------------

Decision engine decision cycles happen in channels.
You can add channels by adding configuration files in ``/etc/decisionengine/config.d/``
and restarting the decision engine.

Here is a simple test channel configuration.
This test channel is using some NOP classes currently defined in the unit tests and not distributed.

The following configuration has been added as an example to ``/etc/decisionengine/config.d/test_channel.jsonnet`` during the installation process::

    {
      sources: {
        source1: {
          module: "decisionengine.framework.tests.SourceNOP",
          parameters: {},
          schedule: 1,
        }
      },
      transforms: {
        transform1: {
          module: "decisionengine.framework.tests.TransformNOP",
          parameters: {},
          schedule: 1
        }
      },
      logicengines: {
        le1: {
          module: "decisionengine.framework.logicengine.LogicEngine",
          parameters: {
            facts: {
              pass_all: "True"
            },
            rules: {
              r1: {
                expression: 'pass_all',
                actions: ['publisher1']
              }
            }
          }
        }
      },
      publishers: {
        publisher1: {
          module: "decisionengine.framework.tests.PublisherNOP",
          parameters: {}
        }
      }
    }

Once the decisionengine is running, ``de-client --status`` should show the active test channel.
