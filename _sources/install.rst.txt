.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Installing and running HEPCloud's Decision Engine on EL9
========================================================

Currently the only version supporting EL9 is the development version, DE 2.0.x, which corresponds to the master branch in Git.

Decision engine uses a PostgreSQL database back-end and Redis as message broker and cache.

You need to install first PostgreSQL, Redis, and then the Decision engine framework (decisionengine) and install and add the standard channels (decisionengine_modules).

The following instructions assume Alma Linux 9. You may need to adapt them slightly for other EL9 flavors.

These also assume a system installation, performed as ``root``.
decisionengine will run as the decisionengine user.


Install PostgreSQL
------------------

Install the default postgresql distributed on RHEL9, Postgress 13:

1. Install postgresql ::

    dnf install -y postgresql postgresql-server
    # optional, also: postgresql-devel

2. Enable postgresql ::

    systemctl enable postgresql

3. Init the database ::

    postgresql-setup --initdb -k

4. edit ``/var/lib/pgsql/data/pg_hba.conf`` like the following::

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


   This is setting the authentication method to `trust`

5. start the database ::

    systemctl start postgresql

6. create decisionengine ::

    createdb -U postgres decisionengine

The schema and the connection will be created and configured during the Decision engine framework installation.

To use the database you have to add it to the environment::

    export PG_VERSION=13
    export PATH="~/.local/bin:$PATH"
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


Install needed RPMs prerequisites
---------------------------------

1. Make sure the correct repositories and priorities are set. ::

    # CRB ("Code Ready Builder" - PowerTools ) is used for swig and other dependencies
    dnf install -y yum-utils
    dnf config-manager --set-enabled crb
    # EPEL is used for OSG dependencies
    dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
    # OSG is used for GlideinWMS, HTCSS and others
    dnf install https://repo.opensciencegrid.org/osg/3.6/osg-3.6-el9-release-latest.rpm
    dnf repolist
    # Make sure all the above repos are enabled
    # And change the Epel repository priority to make sure that comes after the OSG repositories, which are 98 by default.
    # Make sure that epel has:
    #  priority=99
    vi /etc/yum.repos.d/epel.repo

2. Install the following prerequisites. Make sure that the required packages are installed and up to date. ::

    # RPMs
    # gcc, swig and make are needed for dependencies (jsonnet)
    dnf install -y python3 python3-devel python3-cryptography python3-pip
    dnf install -y gettext git make openssl-devel gcc gcc-c++ swig
    # Install also these for RPM building:
    dnf install -y python3-setuptools python3-wheel rpm-build
    # Update Python pip
    python3 -m pip install --upgrade --user pip
    python3 -m pip install --upgrade --user setuptools wheel setuptools-scm[toml]


..

  Use PIP installation below - Install via RPMs - coming soon
  -----------------------------------------------------------

  You can install using the provided RPMs (recommended for production) or via PIP install (recommended for development whnen you want to clone the Git repository and change the code).
  This section is for the RPM installation, the next one for the PIP installation. Use one or the other.

  1. The yum repositories are available only within Fermilab. From the outside you will have to download the RPMs from `GitHub<https://github.com/HEPCloud/decisionengine/releases>` or use the PIP installarion (below).
   Setup the decision engine yum repositories ::

    # You need the development version wget -O /etc/yum.repos.d/ssi-hepcloud.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud.repo
    wget -O /etc/yum.repos.d/ssi-hepcloud-dev.repo http://ssi-rpm.fnal.gov/hep/ssi-hepcloud-dev.repo
    # This is the same as the EL9 development repo: http://ssi-rpm.fnal.gov/hep/hepcloud-el9/ssi-hepcloud-dev.repo (http://ssi-rpm.fnal.gov/hep/hepcloud-el9/development/)

  2. Install the decision engine and add ``--enablerepo=ssi-hepcloud-dev`` for the latest development version ::

    dnf install decisionengine
    dnf install decisionengine_modules

  3. Not all packages are available as RPM. It is necessary to install directly some Python dependencies.
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
    python3 -m pip install --user jsonnet==0.17.0 tabulate toposort structlog
    python3 -m pip install --user wheel DBUtils sqlalchemy
    python3 -m pip install --user pandas==2.0.0 numpy==1.24.2
    python3 -m pip install --user "psycopg2-binary >= 2.9.6; platform_python_implementation == 'CPython'"
    python3 -m pip install --user "psycopg2cffi >= 2.9.0; platform_python_implementation == 'PyPy'"
    python3 -m pip install --user "cherrypy>=18.8.0" "kombu[redis]>=5.3.0b3" "prometheus-client>=0.16.0"
    python3 -m pip install --user "psutil>=5.8.0" "typing_extensions==4.1.1"
    # from decisionengine_modules setup.py
    python3 -m pip install --user boto3 google-api-python-client
    python3 -m pip install --user "google_auth<2dev,>=1.16.0" "urllib3>=1.26.2"
    python3 -m pip install --user gcs-oauth2-boto-plugin
    # Condor should be already there from the RPM, if not add: python3 -m pip install htcondor
    python3 -m pip install --user bill-calculator-hep

    # The following are additional requirements for v1.6 and earlier
    python3 -m pip install --user boto packaging
    # This is not in pypi
    python3 -m pip install --user https://test-files.pythonhosted.org/packages/f4/a5/17a14b4ef85bc412a0ddb771771de3f562430328b0d83da6091a4131bb26/bill_calculator_hep_mapsacosta-0.0.10-py3-none-any.whl

    exit

  Now you can type ``decisionengine --help`` to print the help message.
  To do more you need first to configure Decision Engine.
  Skip the PIP installation and go to the configuration section.

..


Install via PIP
---------------

Skip this if you did the RPM installation. This PIP installation is recommended for development whnen you want to clone the Git repository and change the code.
There are a few extra steps (dependencies installation ansd setups) that are automated in the RPM installation.

1. GlideinWMS (3.10.x) and HTCondor (aka HTCSS) are needed for Decision Engine. The ``glideinwms`` packages will pull all the other dependencies.
  The complete version of the GlideinWMS installation instructions is available `here<https://opensciencegrid.org/docs/other/install-gwms-frontend/>`.
  For a minimal installation, you can use the following command: ::

    dnf install glideinwms-vofrontend-libs glideinwms-vofrontend-glidein glideinwms-userschedd glideinwms-usercollector
    dnf install glideinwms-vofrontend-core glideinwms-vofrontend-httpd

2. Setup the decision engine user and git repositories ::

    useradd decisionengine
    sudo -u decisionengine git clone https://github.com/HEPCloud/decisionengine.git ~decisionengine/decisionengine
    sudo -u decisionengine git clone https://github.com/HEPCloud/decisionengine_modules.git ~decisionengine/decisionengine_modules

3. Install the decision engine from the git repositories ::

    # Install the decisionengine framework and modules using setuptools
    su - decisionengine -s /bin/bash
    # Now you should be the decisionengine user in its home directory
    pushd decisionengine
    python3 setup.py develop --user
    popd
    pushd decisionengine_modules
    python3 setup.py develop --user
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

**- Configure the pressure-based submisison**
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

  # If you istalled via RPMs run
  systemctl stop decisionengine.service
  # Run de-client --stop as decisionengine if you installed w/ PIP
  podman stop decisionengine-redis | xargs podman rm


Troubleshooting
---------------

There is a known podman bug.
``podman`` is leaking volumes each time it starts a container, in the long run this is exhausting system resources.
To check current volumes used by podman user can run ``podman volume list``.
To clean up volumes user can run ``podman volume prune -f`` after all podman container have been stopped and removed.
