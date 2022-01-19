.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0


Release 2.0.0
-------------

This release series follows 1.7. A lot started to happen in 1.7.0 and has happened since, so we felt it was proper
to change the major version number.
We are proud to introduce Decision Engine 2.0.0 to outside users: it provides a
friendlier installation procedure and configuration samples to test it
on all resources supported by the GlideinWMS Factory, like OSG, some HPC resources and
commercial cloud providers.

- New architecture with redesigned source system using Kombu message passing with a Redis backend.
- Separation from the GlideinWMS Frontend. Decision Engine still shares some libraries with GlideinWMS but
  you don't need any more to install and configure the Frontend.
- Structured logging. Improved python logging and adoption of structured logs format that will increase the semantinc content of the messages and ease the export of information for dashboards and Elastic Search.
- Monitoring via Prometheus.
- SQLAlchemy object-relational mapper to increase the testability of DB interactions and to allow different database backends.
- Packaging via setuptools for both decisionengine and decisionengine_modules: Dependencies are not yet fully listed in the RPMs.
- Added support of CentOS8 (RHEL7 is still out main platform)
- Configuration example using HTC resources via GlideinWMS Factory
- Decision Engine is distributed under the Apache 2.0 license
- We increased our CI tests including also code auto-formatting and license compliance.
  We introduced integration tests and we are proud of our over 95% unit test coverage.

.. note::
    SQLAlchemy is required and is now the only datasource backend supported.
    Upgrading from a different datasource backend (1.6 or earlier were using direct PostgreSQL, 1.7 was supporting both)
    is a one-way change with a migration tool.
    We suggest dropping all objects if you wish to reuse the tablespace.
    You can preserve a copy of the old database to query historical information.
.. note::
    Added requirement on the Kombu library and a Redis server.
    We suggest to `install Redis using a container <redis.rst>`_.
.. note::
    Added requirement on prometheus-client.
    Prometheus is be used as optional monitoring component.



Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `528 <https://github.com/HEPCloud/decisionengine/issues/528>`_: Update license and add copyright notices
- `207 <https://github.com/HEPCloud/decisionengine/issues/207>`_: Under certain circumstances the fetch of the "consumes" information fails but the channel does not go offline operations
- `547 <https://github.com/HEPCloud/decisionengine/issues/547>`_: Update DE client libs to pgsql-12
- `459 <https://github.com/HEPCloud/decisionengine/issues/459>`_: Setuptools issues in decisionengine rpm
- `546 <https://github.com/HEPCloud/decisionengine/issues/546>`_: Request CentOS8 Stream support for Decision Engine
- `453 <https://github.com/HEPCloud/decisionengine/issues/453>`_: Struct Logging Self test errors with pytest-xdist
- `418 <https://github.com/HEPCloud/decisionengine/issues/418>`_: Add auto-formatting of the code
- `134 <https://github.com/HEPCloud/decisionengine/issues/134>`_: Yum update on decisionengine rpm doesn't restart the service
- `480 <https://github.com/HEPCloud/decisionengine/issues/480>`_: Request: Make postgresql migration script to migrate from old postgresql schema to new sqlalchemy schema


Full list of commits since version 1.7.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`7d6484ad <https://github.com/HEPCloud/decisionengine/commit/7d6484ad86bfc1c01c89c8648c2b41d23f5c710d>`_:   Test source shared between two channels.

`ae29d9d1 <https://github.com/HEPCloud/decisionengine/commit/ae29d9d17395f4d3742b127e7dd185a8bb837cba>`_:   Test same source types, separate channels

`6095d33f <https://github.com/HEPCloud/decisionengine/commit/6095d33fa86f8f736c43ddc32fe6e192e5defb74>`_:   Test LatestMessages utility.

`dfbf3e06 <https://github.com/HEPCloud/decisionengine/commit/dfbf3e06395404cef45b8206ec9492ef8ec0d42e>`_:   Separate sources from channels.

`2c10391e <https://github.com/HEPCloud/decisionengine/commit/2c10391e561ebfea309a40115972fc0fba560fb1>`_:   Remove source proxy

`afcc7cff <https://github.com/HEPCloud/decisionengine/commit/afcc7cff27bacad5cb823d04df56456deac307a1>`_:   Add some more logging to try and trace startup state

`dbd49a66 <https://github.com/HEPCloud/decisionengine/commit/dbd49a668c935e473830aac7282ea3c6a2220586>`_:   Explicitly pass .coveragerc to pytest.

`e6b03216 <https://github.com/HEPCloud/decisionengine/commit/e6b032162b9ce38a746c4ebc2311b063fc02abc4>`_:   Set max retry timeout for sqlite in unit tests.

`51bed3d6 <https://github.com/HEPCloud/decisionengine/commit/51bed3d6f0ae1784370a41b86f094dd548f28a08>`_:   Updated documentation for 1.7.1 release

`3829151f <https://github.com/HEPCloud/decisionengine/commit/3829151f5b8f1a9ca3f61e15e6a0f2201bfc2769>`_:   Allow duplicate keys if their values are the same.

`1ea288e0 <https://github.com/HEPCloud/decisionengine/commit/1ea288e068c7d053ecf79436c73a101d7ab02076>`_:   [pre-commit.ci] pre-commit autoupdate

`6b6611e5 <https://github.com/HEPCloud/decisionengine/commit/6b6611e5305b7fffc42f6be48928fdd9d2af1b2e>`_:   Use pre-commit.ci rather than local actions

`dedbe4bd <https://github.com/HEPCloud/decisionengine/commit/dedbe4bd41b9103026b5caca83f090cae933ccfa>`_:   Use local time for structlog timestamp

`461c506e <https://github.com/HEPCloud/decisionengine/commit/461c506e546ae743cca953f70b11c2e3e1b6f5ea>`_:   Make sure de_std.libsonnet is provided when packaged.

`f93b5963 <https://github.com/HEPCloud/decisionengine/commit/f93b59639fb814219104c048a4da565d590f4fd5>`_:   Update pre-commit hook versions and accommodate python-debian issue.

`bba51609 <https://github.com/HEPCloud/decisionengine/commit/bba51609c78f9d905ca254074d798f76b95d9c23>`_:   Reduce number of fixtures.

`a4510cb1 <https://github.com/HEPCloud/decisionengine/commit/a4510cb1589e8cc8e38c94866ad002f78c84f200>`_:   Segment the update for setuptools so it gets cached correctly

`40098f35 <https://github.com/HEPCloud/decisionengine/commit/40098f359deec4470da1fdb479d7bbe0cdd6c8c2>`_:   Merge pull request #584 from jcpunk/user-pip

`4e1b79a1 <https://github.com/HEPCloud/decisionengine/commit/4e1b79a1718e32fe4a8224f3a1d6fa9a53be6bb5>`_:   Merge pull request #583 from jcpunk/drop-dbutils

`72c8db4a <https://github.com/HEPCloud/decisionengine/commit/72c8db4a3ff5da0f81450012b08e22c50c044820>`_:   Recommend using the site user pip dir instead.

`ff604495 <https://github.com/HEPCloud/decisionengine/commit/ff604495b9afeea8c5f17daf52cf7208856c7e18>`_:   Drop unneeded module

`b203e2c4 <https://github.com/HEPCloud/decisionengine/commit/b203e2c493cf501562accf1013c6257c348711b7>`_:   remove extraneous 'import gc'

`ee2278e7 <https://github.com/HEPCloud/decisionengine/commit/ee2278e74b6d8d4203a1bef79f281bac37d5910c>`_:   replace needed import

`4b7dedf2 <https://github.com/HEPCloud/decisionengine/commit/4b7dedf2fa8998c13682870445714df32a38044e>`_:   add licensing info

`e5a56816 <https://github.com/HEPCloud/decisionengine/commit/e5a56816fa8ad7247443971b35ffd259080c8446>`_:   add licensing info

`a114abba <https://github.com/HEPCloud/decisionengine/commit/a114abbab70862bc2b2c8b0c84ed1b1d9a64c05f>`_:   add licensing info

`c2d511cd <https://github.com/HEPCloud/decisionengine/commit/c2d511cd616b56998eb84509316af95445d9338b>`_:   adding queue logging to de_logger

`77dd8d5a <https://github.com/HEPCloud/decisionengine/commit/77dd8d5a78c301ffe158f3966354e38e7f1b9ab7>`_:   Also run checks on backports to 1.7

`7c029578 <https://github.com/HEPCloud/decisionengine/commit/7c0295785a8f2ba11b8d3d1748b5469ef2adec02>`_:   Updated developers instructions w/ license maintenance via REUSE information

`e66b985d <https://github.com/HEPCloud/decisionengine/commit/e66b985d2c26c73a8987d327f3a892d4c90d072b>`_:   Fix faulty tests.

`d1a86c57 <https://github.com/HEPCloud/decisionengine/commit/d1a86c57cf1ba36dc0825f31a6dade5496e2c10a>`_:   Set Apache 2.0 license and added REUSE compliance

`e488030e <https://github.com/HEPCloud/decisionengine/commit/e488030ed4445be219baa46c4a4336f5eb135cb0>`_:   Ensure that redis is running.

`6c982c11 <https://github.com/HEPCloud/decisionengine/commit/6c982c11a0d4bb1367e3b7283bdceaa59310630c>`_:   Report PID for source process.

`3f844ca4 <https://github.com/HEPCloud/decisionengine/commit/3f844ca4a678dae0d0a10cb2c534f91ab552ea57>`_:   Further flesh out the documentation

`1d750001 <https://github.com/HEPCloud/decisionengine/commit/1d750001fac90b9ec3a5cd5781ae8e372f95f091>`_:   Simplifications and rearrangements.

`b85dca45 <https://github.com/HEPCloud/decisionengine/commit/b85dca452a03b5e5bb488c282c59a8110b788a96>`_:   Set state to error for exceptions caught before the thread start.

`c4727acb <https://github.com/HEPCloud/decisionengine/commit/c4727acb4d30f94541a11277679dc75a328c776f>`_:   Changed summaries to histograms in DecisionEngine and TaskManager modules

`6fa0bf4d <https://github.com/HEPCloud/decisionengine/commit/6fa0bf4d1f5169e144f57d783b185d9bd8a63c4c>`_:   Added install document and updated the index and development instructions accordingly

`e4de391e <https://github.com/HEPCloud/decisionengine/commit/e4de391e7a55bc077296ab726311eb411a6926c2>`_:   Do the build of the wheel as not-root per our requirements

`24ba5272 <https://github.com/HEPCloud/decisionengine/commit/24ba52729afb9bac7bd303d51a20a7d3405a48c7>`_:   Add a redis server to the CI testing containers

`c939a6ed <https://github.com/HEPCloud/decisionengine/commit/c939a6ed9ff021b9fbc8fde0b3eaa0ce0baa00d5>`_:   Address Pat's comments.

`1925a7b0 <https://github.com/HEPCloud/decisionengine/commit/1925a7b00165c92516577e57f7e85c8100ba2e00>`_:   First implementation using Kombu/redis to communicate data from sources to cycles.

`82faa271 <https://github.com/HEPCloud/decisionengine/commit/82faa27127aee458e40bc7e491f411a9b9c10727>`_:   Don't try to package obsolete sql file

`9cbffe94 <https://github.com/HEPCloud/decisionengine/commit/9cbffe94ac0a2c3b1b2cbffb53564588a1419a25>`_:   Drop redundant tests.

`ab0de9a5 <https://github.com/HEPCloud/decisionengine/commit/ab0de9a5012b368b5c3bc179372fef6b95c70592>`_:   Drop obsolete raw postgresql interface

`164b36d3 <https://github.com/HEPCloud/decisionengine/commit/164b36d3237ae5df4f3a87e76d9b8d155655dc88>`_:   Removed unnecessary comment

`91f7a76f <https://github.com/HEPCloud/decisionengine/commit/91f7a76f3e93f76cd8185af65e2b2dd0c6880afd>`_:   Fixed rebase errors

`e475fbd5 <https://github.com/HEPCloud/decisionengine/commit/e475fbd5b95d375d978f51146722e7e14721875f>`_:   Added import statement to fix MultiProcessCollector

`a409f126 <https://github.com/HEPCloud/decisionengine/commit/a409f12654d9301784b8cdc813c25a0cd7efaab7>`_:   Add no-webserver setting to all DE Test Workers

`39cca32e <https://github.com/HEPCloud/decisionengine/commit/39cca32efbda4887b11532b51bebe9d6d6a0e308>`_:   Moved multiprocess import to metrics to clean up imports.

`73762e90 <https://github.com/HEPCloud/decisionengine/commit/73762e90d4afeb5777183ee9266948d789cfcbbe>`_:   Added --no-webserver to invocations of DEServer

`303ee4be <https://github.com/HEPCloud/decisionengine/commit/303ee4be2544a4fcdffc7800a5b5e37ed60f59bd>`_:   Added __all__ global to control what is exported.

`5170224b <https://github.com/HEPCloud/decisionengine/commit/5170224bd9bbb1576a2458341f1f3e0ae451d9ae>`_:   Allow for metrics disabling from systemd unit file

`2cacef4f <https://github.com/HEPCloud/decisionengine/commit/2cacef4f4af23393e26e85630dd0af258031c92c>`_:   Added check for proper metrics environment and associated unit tests

`a637a088 <https://github.com/HEPCloud/decisionengine/commit/a637a088437ec33beb27224464db50fb02b86b52>`_:   Make webserver operation configurable

`b3d6445a <https://github.com/HEPCloud/decisionengine/commit/b3d6445ab93ad32cf3bc718d4e4bafd613013b0c>`_:   Changed set_to_function calls to set() calls for metrics

`5dccc7fa <https://github.com/HEPCloud/decisionengine/commit/5dccc7fabcf7a893cfeedeffd0cfc460c4c11c41>`_:   Changed metric names to match prometheus convention

`7371c2e8 <https://github.com/HEPCloud/decisionengine/commit/7371c2e8c013fd42887dafa0f9aa418101740fef>`_:   Added cherrypy requirement

`2c511cea <https://github.com/HEPCloud/decisionengine/commit/2c511ceaea911106c0fcbfbd2ca7153caa8eb2d1>`_:   Added metrics to record time to run Modules and DecisionEngine rpc calls

`c24d33bc <https://github.com/HEPCloud/decisionengine/commit/c24d33bc269d92a4d9d05b8e825394c6ccd065ef>`_:   Renamed prometheus.py to metrics.py

`2335134d <https://github.com/HEPCloud/decisionengine/commit/2335134dcda74c10878c42ffacdbb3a454a811a1>`_:   Moved TaskManager metrics to util/prometheus.py to avoid duplicates

`3c1b790c <https://github.com/HEPCloud/decisionengine/commit/3c1b790c671124dfb9179bc9c6fdad9385dbb598>`_:   Added metrics endpoint to RPC server, changed prometheus to multiprocess mode, and added CherryPy webserver for prometheus metrics

`d8972de0 <https://github.com/HEPCloud/decisionengine/commit/d8972de076afe9add8ed52368c5aed463f96cefa>`_:   Added unit tests for metrics API

`7b0f641b <https://github.com/HEPCloud/decisionengine/commit/7b0f641b49167e79b760b10662d45999dd2d9f6c>`_:   Add instructions for running the Redis container.

`8d0c4919 <https://github.com/HEPCloud/decisionengine/commit/8d0c491987e4da4fc36e91baf52ea30db055a067>`_:   Block pytest-postgresql 4

`d988f1a0 <https://github.com/HEPCloud/decisionengine/commit/d988f1a06ad317162646d71e81302b91121e318a>`_:   Lower timeout for actions.

`4f920dcc <https://github.com/HEPCloud/decisionengine/commit/4f920dcce3a2a6bcd39df36f25ffc198ca90f772>`_:   Simplifications in preparation for Kombu.

`eb9f4292 <https://github.com/HEPCloud/decisionengine/commit/eb9f429240dc647d97ac9da46d586a03227adb20>`_:   Make TaskManager not executable

`00c8f6e6 <https://github.com/HEPCloud/decisionengine/commit/00c8f6e68022218799ad0f544727c88a963c448d>`_:   Remove unused files.

`dd990d2c <https://github.com/HEPCloud/decisionengine/commit/dd990d2ccc8396e2bd3659a3537e56cbb9bc4137>`_:   Adding de-logparser, a tool to help parsing Decision Engine semi-structured logs

`1da0d61e <https://github.com/HEPCloud/decisionengine/commit/1da0d61eaed9d0a6d92c1c61a37233d7ab340f84>`_:   Added a comment to help developers with incomplete installation

`1cbc7334 <https://github.com/HEPCloud/decisionengine/commit/1cbc7334b15ca7f875d20f9e62320211a7eb804a>`_:   Drop testing/support for PyPy

`3ba3e8e6 <https://github.com/HEPCloud/decisionengine/commit/3ba3e8e6c7f013acefc3930145e8d561bc5b12e8>`_:   Ignoring E203, whitespace after ':', since black is adding the whitespace

`814669d5 <https://github.com/HEPCloud/decisionengine/commit/814669d5e1dd7f767c596fea1de75333e0e23c0b>`_:   Disable PyPy test that fails for PG_DE_DB_WITH_SCHEMA fixture value.

`8d68c287 <https://github.com/HEPCloud/decisionengine/commit/8d68c287247002320f19041914293e620f4bc39e>`_:   Fix debug message

`33db6425 <https://github.com/HEPCloud/decisionengine/commit/33db64256081fa0198752f317257fe4214d09bd2>`_:   Test composite workflows using source proxies and configuration combination.

`30951a5b <https://github.com/HEPCloud/decisionengine/commit/30951a5b5890c7e7dba6165841a2ff66e27c3386>`_:   EL7 doesn't ship with a new enough golang for jsonnetfmt

`e72eb3fd <https://github.com/HEPCloud/decisionengine/commit/e72eb3fdd169ebc92c468cd954510aa36ca1411d>`_:   Forbid inheritance from SourceProxy.

`e95071fd <https://github.com/HEPCloud/decisionengine/commit/e95071fdef61aa3216f7308453bd3222f0b5cf78>`_:   Automatically format jsonnet files with jsonnetfmt

`355ccd45 <https://github.com/HEPCloud/decisionengine/commit/355ccd45036155f71162d0ed522ea3ae14d1b425>`_:   Correct tests for python 3.10

`64119161 <https://github.com/HEPCloud/decisionengine/commit/641191610b5819c353e931e07bcd498231adf30f>`_:   Start testing python 3.10

`c1cb8258 <https://github.com/HEPCloud/decisionengine/commit/c1cb8258726042bb0217a0d89fde764baa0f965a>`_:   add dummy source and test

`31b0f30b <https://github.com/HEPCloud/decisionengine/commit/31b0f30b4e528518f70bf3012caa4122e7c99bfb>`_:   Check for duplicate keys after source proxies have been removed.

`140a4c47 <https://github.com/HEPCloud/decisionengine/commit/140a4c4748b61fb46d88cdab5b2cca31907f1700>`_:   Fix configuration-combination function signature.

`d4a05299 <https://github.com/HEPCloud/decisionengine/commit/d4a052991211a7daf85b44dfd57ac0122b27fa66>`_:   Remove now unnecessary blocking.

`1e78a889 <https://github.com/HEPCloud/decisionengine/commit/1e78a8894defdaf9120deb3d56890a164026bcd7>`_:   Don't run setup.py as root

`a71d5b0a <https://github.com/HEPCloud/decisionengine/commit/a71d5b0ab1de5524e67059c187798215c10bbcdb>`_:   Add error for running server as root

`cd345701 <https://github.com/HEPCloud/decisionengine/commit/cd345701539b9444eb09d6fece5b7445696b05f5>`_:   Incrase coverage in LogicEngine

`6c132924 <https://github.com/HEPCloud/decisionengine/commit/6c1329241181980d4fea546c10d5463987a02b3e>`_:   Fix out of sync devel requirements

`8bfab003 <https://github.com/HEPCloud/decisionengine/commit/8bfab003ab332a5a969839fd4e2be6a4dd29df75>`_:   Start running tests with xdist

`aebe7d49 <https://github.com/HEPCloud/decisionengine/commit/aebe7d49700ae5688278eaf70613197ca6deb4a1>`_:   Remove unnecessary conversion to Pandas dataframe.

`28919b16 <https://github.com/HEPCloud/decisionengine/commit/28919b169d600d3f073aa2e23bfb7db106b27756>`_:   Allow channels to boot in parallel.

`c4fc5997 <https://github.com/HEPCloud/decisionengine/commit/c4fc599723ab1e88d06206c158c346b80f86920e>`_:   Improve parameter and variable names.

`e021419b <https://github.com/HEPCloud/decisionengine/commit/e021419b856657bc0354198b08e07964eea88195>`_:   Encourage use of automatic nag hook

`cc4e469a <https://github.com/HEPCloud/decisionengine/commit/cc4e469a601ff5df8675927cbb4255ae8c4227ee>`_:   Update hooks to latest via `pre-commit autoupgrade`

`cef30b69 <https://github.com/HEPCloud/decisionengine/commit/cef30b6909a5f790c9575e8f6a8b4a9ed5c168c8>`_:   Further simplify some cases

`590bea3f <https://github.com/HEPCloud/decisionengine/commit/590bea3f0de1d262406762ac3d033544cabbdad6>`_:   Add channel-combination facilities.

`a4a7938c <https://github.com/HEPCloud/decisionengine/commit/a4a7938cbf72d179310ccfd999f455c642435a73>`_:   Various simplifications recommended by flake8-simple

`d5157416 <https://github.com/HEPCloud/decisionengine/commit/d51574165cab6c6cfd144824660d410054950565>`_:   Possible simplification to logging.

`81e3d1ee <https://github.com/HEPCloud/decisionengine/commit/81e3d1ee35a701c42a342e952aa2af3901903281>`_:   Fix pylint error on `create_runner` and `ProcessingState`

`2a328c25 <https://github.com/HEPCloud/decisionengine/commit/2a328c2599e187eaeb7efdb4d39a56c5fbe515e9>`_:   Added missing init file to make managers a package

`d7f44015 <https://github.com/HEPCloud/decisionengine/commit/d7f44015399b8e290a4c56529b37e3140777d18d>`_:   Rework tests for #454

`9521d3ce <https://github.com/HEPCloud/decisionengine/commit/9521d3cea71ac89a04c2dfa3a0e9b9006a31a673>`_:   Add debug statement when default logic-engine configuration is used.

`c6dc778c <https://github.com/HEPCloud/decisionengine/commit/c6dc778c29bc609903c93669e9ba18d0eb655e21>`_:   Unconditionally execute publishers with default configured logic engine.

`a48dd7d8 <https://github.com/HEPCloud/decisionengine/commit/a48dd7d89a341cc1351c86607d8508c877714e8c>`_:   Remove now-unnecessary Python-to-Jsonnet conversion.

`a6a81ce7 <https://github.com/HEPCloud/decisionengine/commit/a6a81ce789fdc68cd2ce44e9efaba3f5ef3c663a>`_:   Run autoformatters

`49dac1ec <https://github.com/HEPCloud/decisionengine/commit/49dac1ec884ec9754feb5e170ecd6fa6b98619fb>`_:   Setup pre-commit hooks for autoformatters

`3800cc2a <https://github.com/HEPCloud/decisionengine/commit/3800cc2a2883f4927b69c541a40cee43142d4ba0>`_:   Run the code style/standards checks early.

`1d42eb0d <https://github.com/HEPCloud/decisionengine/commit/1d42eb0d31a308227488126e1f80fae03c07709a>`_:   TaskManager now inherits from ComponentManager. Also added SourceManager, ChannelManager, and SourceSubscriptionManager files for future integration.

`85a16f3b <https://github.com/HEPCloud/decisionengine/commit/85a16f3b4495c86b96d72ce91e1fff63310eba1c>`_:   Python optimised byte code removes assert under some conditions

`bed2f5d9 <https://github.com/HEPCloud/decisionengine/commit/bed2f5d92a4eccdcf3380a0674be98bc67eeb154>`_:   Support latest setuptools_scm  release
