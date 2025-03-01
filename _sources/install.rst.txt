.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Installing and running HEPCloud's Decision Engine on EL9
========================================================

Currently the only version supporting EL9 is the development version, DE 2.0.x, which corresponds to the master branch in Git.

Decision Engine uses a PostgreSQL database back-end and Redis as message broker and cache.

The first one is installed as RPM requirement, the second is used as container. You need to install the pre-requisites RPM and then the Python packages for Decision Engine framework (decisionengine) and install and add the standard channels (decisionengine_modules).

The following instructions assume Alma Linux 9. You may need to adapt them slightly for other EL9 flavors.

These also assume a system installation, performed as ``root``.
decisionengine will run as the decisionengine user.


Install Decision Engine and the standard modules
------------------------------------------------

RPM installation

1. Prerequisites setup. Make sure that the required yum repositories and some required packages (python3, gcc, ...) are installed and up to date. ::

    # Possible OSG versions: 24, 23, 24-upcoming
    OSG_VERSION=24
    # YUM repo for Decision Engine
    GWMS_REPO=osg-development
    dnf install -y epel-release yum-utils sed
    dnf config-manager --set-enabled crb
    /bin/sed -i '/^enabled=1/a priority=99' /etc/yum.repos.d/epel.repo
    dnf -y install "https://repo.osg-htc.org/osg/$OSG_VERSION-main/osg-$OSG_VERSION-main-el9-release-latest.rpm"

2. Setup the decision engine yum repositories ::

    wget -O /etc/yum.repos.d/ssi-hepcloud.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud.repo
    wget -O /etc/yum.repos.d/ssi-hepcloud-dev.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud-dev.repo
    # Note the above repos are only accessible within Fermilab.  There is an alternative place on github to get the RPMs if you are off-site.

3. Install the decision engine (add `--enablerepo=ssi-hepcloud-dev` for the latest development version) ::

    DE_REPO=ssi-hepcloud-dev
    dnf install -y --enablerepo="$DE_REPO" decisionengine-onenode
    # Individual packages are: decisionengine-deps (framework req) decisionengine-modules-deps (modules req) decisionengine-standalone (2 deps+httpd)

4. Install the required Python packages (these are taken from setup.py) ::

    decisionengine-install-python --de-git-ref 2.0.4
    # This shell script (included in decisionengine-deps) installs the Decision Engine Python code.
    # You can run it as root or as the decisionengine user
    # To see all the options:  decisionengine-install-python --help
    # Double check that pip added $HOME/.local/bin to the PATH of user decisionengine

5. Start and enable HTCondor::

    systemctl start condor
    systemctl enable condor

6. Optionally install these extra packages ::

    # htgettoken - if you need it to generate SciTokens
    dnf -y install htgettoken


Fix the GlideinWMS Frontend installation
----------------------------------------

We will make HEPCloud's Decision Engine using some GlideinWMS libraries but independent from the Frontend.
The codebases, though, are still intertwined, so there are some adjustments needed to the GlideinWMS installation.

Create the condor password and change to decisionengine the ownership of the frontend directories: ::

    # Create or copy the FRONTEND condor password file
    # If POOL is not there, do start condor (systemctl start condor)
    pushd  /etc/condor/passwords.d/
    cp POOL FRONTEND
    cp FRONTEND /var/lib/gwms-frontend/passwords.d/
    popd
    chown -R decisionengine: /var/lib/gwms-frontend
    chown -R decisionengine: /etc/gwms-frontend
    # The permission of /var/lib/gwms-frontend/passwords.d/FRONTEND should be 0600


Set up PostgreSQL
-----------------

PostgreSQL is installed by the requirements RPM, Postgresql 13:

1. Enable postgresql ::

    systemctl enable postgresql

2. Init the database ::

    postgresql-setup --initdb

3. edit ``/var/lib/pgsql/data/pg_hba.conf`` like the following::

    [root@fermicloud371 ~]# diff  /var/lib/pgsql/data/pg_hba.conf~ /var/lib/pgsql/data/pg_hba.conf
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


   (difference of the correct file from the default one - `pg_hba.conf~`)
   This is setting the authentication method to `trust`

4. Fix the PostgreSQL installation. Not sure why, but the run directory was missing and causing the startup to fail. ::

   # Without this the systemctl start was failing and the error was in /var/lib/pgsql/data/log/postgresql-*.log
   mkdir -p /var/run/postgresql
   chown postgres: /var/run/postgresql

5. start the database ::

    systemctl start postgresql

6. create decisionengine ::

    createdb -U postgres decisionengine

The schema and the connection will be created and configured during the Decision Engine framework initialization.

RHEL also provides other PostgreSQL versions via streams. These may require changes to environment variables like PG_VERSION and PATH to use the database.


Install Redis
-------------

Install and start the message broker (Redis) container on your system. You can find more details on the :doc:`redis document <redis>`

1. You may need to fix the firewall used ::

   dnf rm iptables-legacy
   dnf install iptables-nft

2. Install Padman ::

    dnf install -y podman

3. Run the Redis container ::

    podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning
    # When prompted to select an image, pick "docker.io/library/redis:6".


Test
----

Now you can type ``decisionengine --help`` while logged in as decisionengine to print the help message.
To do more you need first to configure Decision Engine.

Remember that all the times that you start a new shell as decisionengine you need to add the PIP binary directory to the PATH::

    export PATH="~/.local/bin:$PATH"

Configure Decision Engine
-------------------------

The default configuration file lives in ``/etc/decisionengine/decision_engine.jsonnet``.

A number of defaults are set for you.

Selecting your datasource
~~~~~~~~~~~~~~~~~~~~~~~~~

You need a datasource to store in the database the channel's data (datablocks).
Each datasource has its own unique schema and cannot be used with a different datasource.

**The SQLAlchemy Data Source**

SQLAlchemy is the default Data Source and is setup with a configuration like::

    "datasource": {
      "module": "decisionengine.framework.dataspace.datasources.sqlalchemy_ds",
      "name": "SQLAlchemyDS",
      "config": {
        "url": "postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_dbname}",
        }
      }

Any extra keywords you can pass to the ``sqlalchemy.engine.Engine`` constructor may be set under ``config``.

SQLAlchemy will create any tablespace objects it requires automatically.


The PostgreSQL data source, used until v1.7, is no more supported.


Start decision engine
---------------------

Start the service ::

    # For the RPM install, as root:
    systemctl start decisionengine
    # For the PIP install, as decisionengine user (Python packages are installed in ~decisionengine/.local/bin/):
    export PATH="~/.local/bin:$PATH"
    decisionengine --no-webserver &


Stop decision engine
--------------------

To stop the service and remove the Redis container once you are done run the following::

    # If you are in a RPM installation, as root:
    systemctl stop decisionengine
    # If you installed via PIP, as decisionengine:
    export PATH="~/.local/bin:$PATH"
    de-client --stop
    # Run the following as root (root started the container)
    podman stop decisionengine-redis | xargs podman rm


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


Finally, start or restart decision engine to start the new channel::

    # For the RPM install:
    systemctl restart decisionengine
    # For the PIP install, as decisionengine user
    decisionengine --no-webserver &


Once the decisionengine is running, ``de-client --status`` should show the active test channel.



Setup pressure-based pilot submission
-------------------------------------

| At this point Decision Engine, GlideinWMS and HTCondor are supposed to be installed and able to run.
| We assume that the Frontend proxy and the VO proxy are already available.
|

**- Configure the pressure-based submission**
| Write the configuration for the Decision Engine glideinwms module
| To ease the process you can use the templates available in the `config_template contrib repo <https://github.com/HEPCloud/contrib/tree/master/config_template>`_.
| Copy the files from the ``EL9`` folder into ``/etc/decisionengine``, and the files in ``EL9/config.d/`` into ``/etc/decisionengine/config.d``.
| If you made changes to ``decision_engine.jsonnet`` please merge it with the version form the repository.
| The important part  from the is the glideinwms import ``decision_engine.jsonnet`` template is the line: ``glideinwms: import 'glideinwms.libsonnet',``.
| Those configuration files have a placeholder field ``@TEMPLATE...@``
| that needs to be replaced with the proper parameters according to your specific system setup. The README file has some suggestions.

Once those configuration files have been updated, we are ready to finalize the Decision Engine configuration.

**- Setup Redis**

Start the message broker (Redis) as pod container::

  podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning

**- Create GWMS frontend configuration**
For this step you need first to restart the Decision Engine and then to run a configuration script. To do so, run::

  # as root (fix the ownership of the frontend library files)
  chown -R decisionengine: /var/lib/gwms-frontend
  # for RPM installation as root
  systemctl staop decisionengine
  systemctl start decisionengine
  ksu decisionengine -e /usr/bin/python3 /usr/lib/python3.9/site-packages/decisionengine_modules/glideinwms/configure_gwms_frontend.py
  # for PIP installation as decisionengine
  de-client --stop
  decisionengine --no-webserver &
  python3 ~decisionengine/decisionengine_modules/src/decisionengine_modules/glideinwms/configure_gwms_frontend.py

This command will create the file ``/var/lib/gwms-frontend/vofrontend/de_frontend_config``

To allow a fresh start stop and reset everything:

1. stop the decisionengine (service)::

  # If you are in a RPM installation, as root:
  systemctl stop decisionengine
  # If you installed via PIP, as decisionengine:
  de-client --stop

2. remove the Redis container::

  # Run the following as root (root started the container)
  podman stop decisionengine-redis | xargs podman rm

3. and reset the decisionengine DB in PostgreSQL::

    dropdb -U postgres decisionengine
    createdb -U postgres decisionengine


**- Run Decision Engine**
Now all should be ready to run Decision Engine with a fresh start.
Start the Redis container and the decisionengine service.

* Run Redis container::

    podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning

* Start decisionengine service and check its status::

    # For RPM installations as root:
    systemctl start decisionengine
    sleep 5
    systemctl status decisionengine
    # For PIP installations as decisionengine:
    decisionengine --no-webserver &
    sleep 5
    de-client --status


**- Submit a test job**
Finally you can submit a test job to trigger Glidein requests and test the system.

* Switch to ``decisionengine`` user and make sure channel and sources are ``STEADY``::

  ksu decisionengine -e /bin/bash
  de-client --status


* prepare a Condor submission file ``mytest.submit`` with the following content::

    #  A test Condor submission file - mytest.submit
    executable = /bin/hostname
    universe = vanilla
    +DESIRED_Sites = "@CHANGEME@"
    log = test.log
    output = test.out.$(Cluster).$(Process)
    error = test.err.$(Cluster).$(Process)
    queue 1

* submit the test job::

    condor_submit mytest.submit

* check jobs in the queue::

    condor_q

* check for available glideins::

    condor_status

after test jobs are submitted it will take few minutes (usually no more than 10 minutes) to get some glideins and then get the job running.

Now the ``decisionengine`` user session can be closed to get back to the ``root`` session.

**- Stop Decision Engine service**

Finally stop Decision Engine service and remove the Redis container::

  # If you installed via RPMs run
  systemctl stop decisionengine.service
  # Run de-client --stop as decisionengine if you installed w/ PIP
  podman stop decisionengine-redis | xargs podman rm


Troubleshooting
---------------

There is a known podman bug.
``podman`` is leaking volumes each time it starts a container, in the long run this is exhausting system resources.
To check current volumes used by podman user can run ``podman volume list``.
To clean up volumes user can run ``podman volume prune -f`` after all podman container have been stopped and removed.
