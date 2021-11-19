Installing and running HEPCloud's Decision Engine
=================================================

Decision engine uses a PostgreSQL database back-end and Redis as message broker and cache.

You need to install first PostgreSQL, Redis, and then the Decision engine framework (decisionengine) and install and add the standard channels (decisionengine_modules).

The following instructions assume a system installation, performed as ``root``.
decisionengine will run as the decisionengine user.

Install PostgreSQL
------------------

The default postgresql installed on RH7 is 9.2 which is outdated. Suggest to remove it and install 12 instead :

1. Remove old postgresql ::

    yum erase -y postgresql*

2. Install postgresql 12 ::

    yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
    yum install -y postgresql12 postgresql12-server
    # optional, also: postgresql11-devel

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


Install Redis
-------------

Install and start the message broker (Redis) as explained in
the :doc:`redis document <redis>`

Install Decision Engine and the standard modules
------------------------------------------------


1. Prerequisites setup. Make sure that the required yum repositories and some required packages (python3, gcc, ...) are installed and up to date. ::

    yum install -y http://ftp.scientificlinux.org/linux/scientific/7x/repos/x86_64/yum-conf-softwarecollections-2.0-1.el7.noarch.rpm
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
    # gcc, swig and make are needed for dependencies (jsonnet)
    yum -y install python3 python3-pip python3-setuptools python3-wheel \
        gcc gcc-c++ make \
        python3-devel swig openssl-devel git rpm-build
    python3 -m pip install --upgrade --prefix=/usr pip
    python3 -m pip install --upgrade --prefix=/usr setuptools wheel setuptools-scm[toml]

    # To install the modules you will also need GlideinWMS Frontend, which is in the OSG repository.
    # Assuming the use of OSG 3.5 that supports both GSI and tokens, here is a brief summary of the setup:
    yum install -y yum-priorities
    yum install -y https://repo.opensciencegrid.org/osg/3.5/osg-3.5-el7-release-latest.rpm
    # HTCondor 8.9.x or 9.x, required by GlideinWMS, is in the osg-upcoming repository. It should be enabled to find the dependency
    # GlideinWMS 3.9.x is in osg-contrib. The repository should be enabled to find the dependency
    # In both the following files set: enabled=1
    vi /etc/yum.repos.d/osg-upcoming.repo
    vi /etc/yum.repos.d/osg-contrib.repo
    # Change the Epel repository priority to make sure that comes after the OSG repositories, which are 98. Make sure that epel has:
    priority=99
    vi /etc/yum.repos.d/epel.repo

  The complete version of the GlideinWMS installation instructions is available `here<https://opensciencegrid.org/docs/other/install-gwms-frontend/>`

2. Setup the decision engine yum repositories ::

    wget -O /etc/yum.repos.d/ssi-hepcloud.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud.repo
    wget -O /etc/yum.repos.d/ssi-hepcloud-dev.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud-dev.repo

3. Install the decision engine (add ``--enablerepo=ssi-hepcloud-dev`` for the latest development version) ::

    yum install decisionengine
    yum install decisionengine_modules
    # The modules RPM was renamed. For versions <1.7 use instead
    yum install decisionengine-standard-library

4. Not all packages are available as RPM. It is necessary to install directly some Python dependencies.
   To avoid to pollute the system Python we will install them for the ``decisionengine`` user,
   the user the service is running as.
   Install the required Python packages (these are taken from setup.py) ::

    su decisionengine -s /bin/bash
    python3 -m pip install --upgrade pip setuptools wheel --user
    python3 /path/to/decisionengine/setup.py develop --user
    python3 /path/to/decisionengine/setup.py develop --user --uninstall
    python3 /path/to/decisionengine_modules/setup.py develop --user
    python3 /path/to/decisionengine_modules/setup.py develop --user --uninstall
    exit

   The commands above should be sufficient. Anyway, here is an explicit list you can use in alternative::

    su decisionengine -s /bin/bash
    # from decisionengine setup.py
    python3 -m pip install jsonnet tabulate toposort structlog
    python3 -m pip install wheel DBUtils sqlalchemy
    python3 -m pip install pandas==1.1.5 numpy==1.19.5
    python3 -m pip install "psycopg2-binary >= 2.8.6; platform_python_implementation == 'CPython'"
    python3 -m pip install "psycopg2cffi >= 2.9.0; platform_python_implementation == 'PyPy'"
    # from decisionengine_modules setup.py
    python3 -m pip install boto3 google_auth google-api-python-client
    python3 -m pip install gcs-oauth2-boto-plugin
    # Condor should be already there from the RPM, if not add: python3 -m pip install htcondor
    # bill-calculator-hep is only for versions >= 1.7
    python3 -m pip install bill-calculator-hep

    # The following are additional requirements for v1.6 and earlier
    python3 -m pip install boto packaging
    # This is not in pypi
    python3 -m pip install https://test-files.pythonhosted.org/packages/f4/a5/17a14b4ef85bc412a0ddb771771de3f562430328b0d83da6091a4131bb26/bill_calculator_hep_mapsacosta-0.0.10-py3-none-any.whl

    exit

Now you can type ``decisionengine --help`` to print the help message.
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

    systemctl start decisionengine


Add channels to decision engine
-------------------------------

Decision engine decision cycles happen in channels.
You can add channels by adding configuration files in ``/etc/decisionengine/config.d/``
and restarting the decision engine.

Here is a simple test channel configuration.
This test channel is using some NOP classes currently defined in the unit tests and not distributed.
First, copy these classes from the Git repository::

    cd YOUR_decisionengine_REPO
    # OR download the files from GitHub
    mkdir /tmp/derepo
    cd /tmp/derepo
    wget https://github.com/HEPCloud/decisionengine/archive/refs/heads/master.zip
    unzip master.zip
    cd decisionengine-master
    # Now copy the files
    cp -r src/decisionengine/framework/tests /lib/python3.6/site-packages/decisionengine/framework/

Then, add the channel by placing this in ``/etc/decisionengine/config.d/test_channel.jsonnet``::

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

Finally, restart decision engine to start the new channel::

    systemctl restart decisionengine


``de-client --status`` should show the active test channel
