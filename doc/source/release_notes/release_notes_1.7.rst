.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.7.5
-------------

Fixed source logging. Pinned some dependencies to maintain Python 3.6 compatibility.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugs fixed

- `DE 522 <https://github.com/HEPCloud/decisionengine/issues/522>`_: Decision engine log files get split between several different processes with several different versions open: (`fd1e99ce <https://github.com/HEPCloud/decisionengine/commit/fd1e99ce77a82dbe478c2c7d15f4b100300b2e5d>`_)

Full list of commits since version 1.7.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`0c90cdfb6 <https://github.com/HEPCloud/decisionengine/commit/0c90cdfb632a213537cdd12f4ff4bfc0ad56c05b>`_:   fix source logging by defining logger in Sources after PR670 plus missing adjustments

`670a618f2 <https://github.com/HEPCloud/decisionengine/commit/670a618f260b721acd4d4a1daa985171fef5563a>`_:   Updated release notes for 1.7.5

`ea6ef79d <https://github.com/HEPCloud/decisionengine/commit/ea6ef79d7a6ce5f5ebe0b65efc121702a0211fe0>`_:   pin ubuntu version to 20.04 to get python versions we use to run DE 1.7 tests and set upper limit for python modules to be used by tests

`a1af36f5 <https://github.com/HEPCloud/decisionengine/commit/a1af36f5e91f42da018169388e9b61b0f1b68d8c>`_:   For branch 1.7 pin pytest version to 6.2.5

`352eab54 <https://github.com/HEPCloud/decisionengine/commit/352eab540e9260969542ffc669b5499738b3b1bc>`_:   For branch 1.7 pin jsonnet version to 0.17.0

`bfcfef2f <https://github.com/HEPCloud/decisionengine/commit/bfcfef2f013a41f8e0e87bfdfcfb7a659ba232b2>`_:   Updated release notes for 1.7.4

`4ff9db91 <https://github.com/HEPCloud/decisionengine/commit/4ff9db9104a3226f1ff83a77abcbf9d07739d984>`_:   Updated release notes for 1.7.3

`53aba118 <https://github.com/HEPCloud/decisionengine/commit/53aba118683ccb5106365c66ecd9b319d97c48c6>`_:   Updated release notes, ready for 1.7.2

`a461a8f9 <https://github.com/HEPCloud/decisionengine/commit/a461a8f979a2e46d169f8a7fa52e690e87311bb4>`_:   Updated documentation for 1.7.1 release


Release 1.7.4
-------------

Same as 1.7.1 release. Dome to maintain the same version number as decisionengine_modules.


Release 1.7.3
-------------

Same as 1.7.1 release. Dome to maintain the same version number as decisionengine_modules.

Release 1.7.2
-------------

Same as 1.7.1 release. Done to maintain the same version number as decisionengine_modules.

Release 1.7.1
-------------

Patch level (bug fix) release.


Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Bugs fixed

- `DE 522 <https://github.com/HEPCloud/decisionengine/issues/522>`_: Decision engine log files get split between several different processes with several different versions open: (`fd1e99ce <https://github.com/HEPCloud/decisionengine/commit/fd1e99ce77a82dbe478c2c7d15f4b100300b2e5d>`_)

Enhancements:

- Added dummy sources (`de1536fa <https://github.com/HEPCloud/decisionengine/commit/de1536fae56f2cd1bf03d4c65ece67d1ea2d4c18>`_)


Full list of commits since version 1.7.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`606e1e9f <https://github.com/HEPCloud/decisionengine/commit/606e1e9fdd56b17e51fef92da679bfbb90485747>`_:   Merge pull request #585 from vitodb/fix/1.7/vito_port_PR527

`538cf940 <https://github.com/HEPCloud/decisionengine/commit/538cf9400748c29c9ea865914be54ad20e7f3be6>`_:   Merge pull request #586 from HEPCloud/goodenou-patch-remove-gc

`67febfd0 <https://github.com/HEPCloud/decisionengine/commit/67febfd040973cd00278723f127c144d8b6db7e9>`_:   remove unnecessary 'import gc'

`9da797d3 <https://github.com/HEPCloud/decisionengine/commit/9da797d3bce862787cdba61955543b8175bf43c9>`_:   Improve parameter and variable names.

`55a5b547 <https://github.com/HEPCloud/decisionengine/commit/55a5b5474409d42942dbc07e348fa5fed0f726fb>`_:   porting #PR515 into 1.7 (simplifications to logging in Modules) cherry-picked from commit d515741

`fd1e99ce <https://github.com/HEPCloud/decisionengine/commit/fd1e99ce77a82dbe478c2c7d15f4b100300b2e5d>`_:   porting #PR563 into 1.7 (adding queue logging into de_logger)

`c75deef4 <https://github.com/HEPCloud/decisionengine/commit/c75deef4456ea28f306957666b26353487cdc138>`_:   Also run tests on PRs for backports to 1.7

`de1536fa <https://github.com/HEPCloud/decisionengine/commit/de1536fae56f2cd1bf03d4c65ece67d1ea2d4c18>`_:   add dummy source and test


Release 1.7.0
-------------

This release features:

- New produces-consumes structure using decorators. This will improve the code quality, improving static checks and reducing the lines of code by removing repetitive boilerplates, especially in the modules.
- Added structured logging. Improved python logging and adoption of structured logs format that will increase the semantinc content of the messages and ease the export of information for dashboards and Elastic Search.
- Added SQLAlchemy object-relational mapper to increase the testability of DB interactions and to allow different database backends.
  Switching between datasource backends requires dropping all objects if you wish to reuse the tablespace.
- Packaging via setuptools for both decisionengine and decisionengine_modules: Dependencies are not yet fully listed in the RPMs.
- A new, optional, configuration parameter called "channel_name" is available. "channel_name" is one of the keys in the output dictionary of the structured logging and will be used in the upcoming monitoring. If the variable is not defined in the configuration file, then it is taken from the name of the file, e.g. the job_classification.jsonnet config file gives a default "channel_name" value of "job_classification".

.. note::
    Added requirement on SQLAlchemy (for new datasource backend).
    Non-SQLAlchemy users should ensure the indexes from `13c2f283 <https://github.com/HEPCloud/decisionengine/commit/13c2f28325d697701d9417fb2116364f018da535>`_ are in their database.
.. note::
    Added requirement on prometheus-client.
    Prometheus will be used as optional monitoring component.
.. note::
    The "channel_name" key in the Source Proxy config dictionaries needs to be changed to "source_channel". "channel_name" is now being used to describe the name of the channel itself, not the name of the channel the Source Proxy is getting information from.



Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `481 <https://github.com/HEPCloud/decisionengine/issues/481>`_: Channel name should be available to all worker types in TaskManager
- `456 <https://github.com/HEPCloud/decisionengine/issues/456>`_: Logic engine messages show in the main DE log (1.6.99 post4) prj_testing
- `458 <https://github.com/HEPCloud/decisionengine/issues/458>`_: Exception in new SQLAlchemy data source 1.6.99post4
- `455 <https://github.com/HEPCloud/decisionengine/issues/455>`_: New postgresql exception in 1.6.99post4 (aka Fixed databese inconsistency silently ignored in v1.6)
- `456 <https://github.com/HEPCloud/decisionengine/issues/456>`_: Logic engine messages show in the main DE log (1.6.99 post4)
- `451 <https://github.com/HEPCloud/decisionengine/issues/451>`_: Transforms executed in wrong order in 1.6.99.post3
- `367 <https://github.com/HEPCloud/decisionengine/issues/367>`_: Test race conditions bug
- `406 <https://github.com/HEPCloud/decisionengine/issues/406>`_: Taskmanager doesn't use/honor global log level
- `379 <https://github.com/HEPCloud/decisionengine/issues/379>`_: Add postgresql.sql to distributed decisionengine rpm
- `329 <https://github.com/HEPCloud/decisionengine/issues/329>`_: Docker container is missing pylint
- `293 <https://github.com/HEPCloud/decisionengine/issues/293>`_: Drop requirements.txt setup mode
- `285 <https://github.com/HEPCloud/decisionengine/issues/285>`_: Unify ProcessingState with Reaper state management code
- `253 <https://github.com/HEPCloud/decisionengine/issues/253>`_: Decision engine can sometimes start up at boot time before network name resolution is working (`ae04db5 <https://github.com/HEPCloud/decisionengine/commit/ae04db544599c6777d63cb315ddac169e586809d>`_)


Full list of commits since version 1.6.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`f42558df <https://github.com/HEPCloud/decisionengine/commit/f42558dfed16033be5f4f610b5972000803742f3>`_:   Updated documentation for 1.7.0 release

`029d118a <https://github.com/HEPCloud/decisionengine/commit/029d118a928520b9bf031e42e99670b7666b66c5>`_:   Updated release notes for 1.7.0 RC4 (1.6.99.post8)

`0e19c754 <https://github.com/HEPCloud/decisionengine/commit/0e19c7544bad188bc02d59b149f793ecee48c33e>`_:   fix SP

`810994af <https://github.com/HEPCloud/decisionengine/commit/810994af7fd5e8516eb2fc9a3ce2b3ea348c3358>`_:   Update release_notes_1.7.rst

`fbee95e7 <https://github.com/HEPCloud/decisionengine/commit/fbee95e7afd7029755ccd229e2493ec5edb14551>`_:   Update release_notes_1.7.rst

`68b955b0 <https://github.com/HEPCloud/decisionengine/commit/68b955b030dc32adddbc69855141615142507b4a>`_:   Make sure product is a string

`ef7a8b96 <https://github.com/HEPCloud/decisionengine/commit/ef7a8b96ddb9a27020c6212f95afedca7b017647>`_:   Automatically adjust PYTHONPATH for tests

`e292d388 <https://github.com/HEPCloud/decisionengine/commit/e292d388e0f072474e244f5560dfe8973d24b145>`_:   Updated release notes for 1.7.0 RC3 (1.6.99.post7)

`d60b6e4e <https://github.com/HEPCloud/decisionengine/commit/d60b6e4e8e83b2be96fea44022b1b33107337958>`_:   new changes for logging with common logger name "channel"

`8cdeb67e <https://github.com/HEPCloud/decisionengine/commit/8cdeb67ea8a5020f381aa9eaa1a16221fe3c9a99>`_:   Simplify return expression

`8fb128d3 <https://github.com/HEPCloud/decisionengine/commit/8fb128d3e4c9a93c61959625c3db23cfb024ffdc>`_:   Ensure file is "flushed" so name is fully established

`7806aa00 <https://github.com/HEPCloud/decisionengine/commit/7806aa00cc2463f51c6177c142a97b9c33aa18b1>`_:   Add github CodeQL analysis

`9f09bca9 <https://github.com/HEPCloud/decisionengine/commit/9f09bca92c85234891969efa9b85c49d26f7b9b2>`_:   removed modules/LogicEngine.py and corresponding test

`b9d28fbf <https://github.com/HEPCloud/decisionengine/commit/b9d28fbf7bb81ec1ab18976b15fc743311cf49d0>`_:   Cleaner check for `Any`

`cc91aa24 <https://github.com/HEPCloud/decisionengine/commit/cc91aa2433663f795c352f9d98f2b1503dd95810>`_:   Switch to fstring formatting

`7bb5b64f <https://github.com/HEPCloud/decisionengine/commit/7bb5b64fc8f33f6d66055f65fd0b940f6fd33b1a>`_:   Just return created value rather than store then return

`f4847fbe <https://github.com/HEPCloud/decisionengine/commit/f4847fbe64a3a600aa361ac92155b70ceee59201>`_:   Combine nested `with` blocks

`4ba38bcd <https://github.com/HEPCloud/decisionengine/commit/4ba38bcd4326d4c8eac3c82407bd80bcd9185016>`_:   Drop redundant brackets

`bdcfe8c9 <https://github.com/HEPCloud/decisionengine/commit/bdcfe8c951e4eae72efbcc6fe44eb11aa26bf665>`_:   By convention, pandas is usually imported as `pd`

`1dd904ff <https://github.com/HEPCloud/decisionengine/commit/1dd904ff91a659b65e58278ef521647a0cd15c9c>`_:   Use more traditional expression order

`cccd31bc <https://github.com/HEPCloud/decisionengine/commit/cccd31bc13c66074ee7777132d32824b06728d48>`_:   Unused loop vars should start with `_`

`c055a5cd <https://github.com/HEPCloud/decisionengine/commit/c055a5cdf4a321fe52c52cf53a435650ce5d4076>`_:   Drop `_keys` in favor of DB backed `keys`

`e8c689b4 <https://github.com/HEPCloud/decisionengine/commit/e8c689b4ef78f13d971b0273d2ebe5ea5a5015e2>`_:   Moved prometheus-client requirement to proper place in list

`5391500d <https://github.com/HEPCloud/decisionengine/commit/5391500d5efadbe8e54fce5db7a29ee1fadcca9b>`_:   Added metrics API module

`c2d7835c <https://github.com/HEPCloud/decisionengine/commit/c2d7835c1d22129d134be91e7eedf1290265d1f1>`_:   Drop unnecessary timeout

`c167fc50 <https://github.com/HEPCloud/decisionengine/commit/c167fc5016f494eb567494866fec5c091f4e7c32>`_:   Add tests for de-query-tool entry point

`efabfeb3 <https://github.com/HEPCloud/decisionengine/commit/efabfeb30541332b3476a9e77f4166e64f011a51>`_:   Updated release notes for 1.7.0 RC2 (1.6.99.post6)

`b2739c14 <https://github.com/HEPCloud/decisionengine/commit/b2739c14b965f6fc1de6c0621ae391581a4d127a>`_:   moved logging of LogicEngine from decisionengine logger to channel loggers

`0c0532f3 <https://github.com/HEPCloud/decisionengine/commit/0c0532f37786db32e6200eb50903fe9c32fe0a93>`_:   Add locks to help ensure data changes are "atomic"

`ae63c6ee <https://github.com/HEPCloud/decisionengine/commit/ae63c6ee2cb6914056d93f452fe103fa30c68921>`_:   Use DB generated known keys so it always matches DB state

`b2259e9e <https://github.com/HEPCloud/decisionengine/commit/b2259e9e2b131362684c271e8b0164b6b665faf1>`_:   Use public .keys() rather than internal implementation

`85b6c3ba <https://github.com/HEPCloud/decisionengine/commit/85b6c3baaa30a216b17ac38d771c3bf35ca2401f>`_:   Real world data shows the defaults are fine

`95fb3fdf <https://github.com/HEPCloud/decisionengine/commit/95fb3fdff34c430f452d687dc5bc6668fd19ddfb>`_:   Further constrain tablespace

`3ebe8619 <https://github.com/HEPCloud/decisionengine/commit/3ebe861967c88fde491ac7c63e5ad06807bf5d09>`_:   Finish implementation of get_datablock

`edbb3568 <https://github.com/HEPCloud/decisionengine/commit/edbb35683b38b77dc8efb356424f514ae4d0f57d>`_:   Add entry point for de-query-tool

`fed95c62 <https://github.com/HEPCloud/decisionengine/commit/fed95c62237902f86cb54d4c03a5dc672e906689>`_:   adding logging of importlib imports of modules

`53e62f03 <https://github.com/HEPCloud/decisionengine/commit/53e62f03426586a2fbe987113ffe4ea03461fb2b>`_:   Sometimes pypy times out on the cleanup.

`a44d4bc4 <https://github.com/HEPCloud/decisionengine/commit/a44d4bc4b1d8e6a7744bc16261ed19487d04e4d1>`_:   Don't test sqlite on pypy it isn't necessary

`b13aa8a9 <https://github.com/HEPCloud/decisionengine/commit/b13aa8a9573f739dc632fa6513ba722fd28ac78a>`_:   Some corrections

`94c14110 <https://github.com/HEPCloud/decisionengine/commit/94c141107710f9480d20c762310c81942956d972>`_:   Fix missing defines

`5f102095 <https://github.com/HEPCloud/decisionengine/commit/5f102095422246cc8bf185198b656ad3d5512f12>`_:   More detailed testing of datablock

`b6c99021 <https://github.com/HEPCloud/decisionengine/commit/b6c99021c6a26275be1f68081d6fb2a02bd8ac88>`_:   Make sure our sqlite tests have ForeignKeyConditional support

`6b76ba7c <https://github.com/HEPCloud/decisionengine/commit/6b76ba7cda7f23bdaf07b4a412739157cbb0c666>`_:   Fix typo

`6694369d <https://github.com/HEPCloud/decisionengine/commit/6694369dd7cfe369de07616924ce3306d07ab6ce>`_:   Ensure dbutils uses transactions

`1df400ae <https://github.com/HEPCloud/decisionengine/commit/1df400ae183829c8f0d53f1310af45bfdc63354f>`_:   Fix spaces

`5278fd99 <https://github.com/HEPCloud/decisionengine/commit/5278fd996382965469f002adfb35d5901b585a63>`_:   Raise timeout for numpy on pypy

`6d0a1a74 <https://github.com/HEPCloud/decisionengine/commit/6d0a1a7419883495fb44b17ef2b78091df100a1c>`_:   Release notes ready for v1.7.0

`084f74e1 <https://github.com/HEPCloud/decisionengine/commit/084f74e1228f7d174ae89cdb69dcf42eb893ef71>`_:   Initial SQLAlchemy Datasource

`3353aa00 <https://github.com/HEPCloud/decisionengine/commit/3353aa00111a1933ce263fb0e853b5fe87e30794>`_:   Make sure our jsonnet is json syntax valid

`402b1c26 <https://github.com/HEPCloud/decisionengine/commit/402b1c264c9959f35a5bdef103fb4a827259a5bf>`_:   Fix transform-ordering problem.

`49297573 <https://github.com/HEPCloud/decisionengine/commit/4929757322b1b55e56ad8f83eff6184a80503c2f>`_:   Fix incorrect packaging of tests at top level

`fbfae499 <https://github.com/HEPCloud/decisionengine/commit/fbfae499a9d366ac573fecd3ae82607ad3bede21>`_:   The test_channel loads data once per second.

`33f9ade1 <https://github.com/HEPCloud/decisionengine/commit/33f9ade1700ffb376027bd3763a62c67058907dc>`_:   Rename taskmanager test nodb

`308343e9 <https://github.com/HEPCloud/decisionengine/commit/308343e9358075ea423b4494aa4b4e2ccf5eaef3>`_:   Initial modifications for addition of structured logging

`6f337b75 <https://github.com/HEPCloud/decisionengine/commit/6f337b757ec55754297e64a78c35bf34dff03cfa>`_:   Add missing error message

`23a4b770 <https://github.com/HEPCloud/decisionengine/commit/23a4b770abe07e2de382998eae1dec19688baad7>`_:   Call fixtures in a cleaner manner for xdist

`1f2fe8c4 <https://github.com/HEPCloud/decisionengine/commit/1f2fe8c4eff4bc2ced625b927f6dcce27b63ff5f>`_:   Add self.config so I can introspect the fixtures later

`689c0020 <https://github.com/HEPCloud/decisionengine/commit/689c0020fb325e0c062582ed9284bacfe66be034>`_:   Add missing `config` attrib test

`d2732816 <https://github.com/HEPCloud/decisionengine/commit/d2732816fa685ecf1c3c69c396eb2cd4503d9e1b>`_:   Best practices are for fixtues to `yield` vs `return`

`accef50a <https://github.com/HEPCloud/decisionengine/commit/accef50a90f98cfa3838481e4c08a127d4c00b79>`_:   Seed SQLAlchemy fixtures for later activation

`31002bc5 <https://github.com/HEPCloud/decisionengine/commit/31002bc5d8b4feaa5fddfe4156bd43c8e6210d3e>`_:   Help define the fixture interlocking

`0f5fb129 <https://github.com/HEPCloud/decisionengine/commit/0f5fb129f4b6f52a665a5d90fbdb6ebe41a07704>`_:   The pandas 1.3.0 doesn't build against PyPy any longer

`a7d18a41 <https://github.com/HEPCloud/decisionengine/commit/a7d18a41cb6114b2e40bed4adaa4dff313ec4a21>`_:   Correctly test datablock construction paths

`9af4c144 <https://github.com/HEPCloud/decisionengine/commit/9af4c1441fe45d1467843a5ceb2c5fa9dccf8eb0>`_:   the `mock` package was a backport for python2.

`5ddaff8f <https://github.com/HEPCloud/decisionengine/commit/5ddaff8f07a0ded735a2190ac411654c1566a3e5>`_:   Add another constructor test

`9ae9ad13 <https://github.com/HEPCloud/decisionengine/commit/9ae9ad13565ad529187c945e094274874a231bf4>`_:   Make sure if the client says to stop we don't override it

`a581cd2b <https://github.com/HEPCloud/decisionengine/commit/a581cd2bbcb8a4f093a39058bfcaa9c83e30f616>`_:   run pyupgrade against codebase for python3.6

`09e4e79c <https://github.com/HEPCloud/decisionengine/commit/09e4e79c42049ec74955d82ef8ff662329e91df1>`_:   Handle reaper duplicate shutdowns more cleanly

`64d29dc5 <https://github.com/HEPCloud/decisionengine/commit/64d29dc54903345e6d3cb710c9e41f613e0c0adb>`_:   Drop pointless cache restore

`1c6b2588 <https://github.com/HEPCloud/decisionengine/commit/1c6b2588c4f137050d2e9c290371a37c8f283dfd>`_:   Update PyPy to 3.7 for testing

`2bae173e <https://github.com/HEPCloud/decisionengine/commit/2bae173e7923e04ceb31dc9aa48e43c6f99ddbad>`_:   Increase wait for overloaded test workers, update log messages

`b67c185c <https://github.com/HEPCloud/decisionengine/commit/b67c185ccf4387e0de348b62fe74a4f79d6b6f76>`_:   When aborting CI builds cleanup all processes

`6c5d6306 <https://github.com/HEPCloud/decisionengine/commit/6c5d6306852dcf2152dfed72e97bc1410f70fc9d>`_:   Trim pytest fast functions, add required plugin

`8c63ca6b <https://github.com/HEPCloud/decisionengine/commit/8c63ca6b086592d48eee999c4bc755dadd289d29>`_:   note why we're ignoring this line

`2bd4ecbc <https://github.com/HEPCloud/decisionengine/commit/2bd4ecbc9bb067cd18500b4d43cca89553e90b5f>`_:   Add a syntax check for the toml files

`e2dca404 <https://github.com/HEPCloud/decisionengine/commit/e2dca404d2ce841f683bf56b4e4d3bdc074f4b27>`_:   Sometimes these get stuck

`6d012fab <https://github.com/HEPCloud/decisionengine/commit/6d012fab956c2f1c1cd526adb4bb71f931db1515>`_:   Add in Jenkinsfile pipeline configuration a timeout at stage level

`baf07973 <https://github.com/HEPCloud/decisionengine/commit/baf07973e3c5ab6afec7e4ea0209acb4228493ba>`_:   Add timeout option to block-while/until

`970faf92 <https://github.com/HEPCloud/decisionengine/commit/970faf929ccd4333c63a9d521617bc7b010c1224>`_:   Make pre-commit happy

`0cea2285 <https://github.com/HEPCloud/decisionengine/commit/0cea22855f26bf53453add616dfba2cb3aef2a7e>`_:   Fix alignment issue

`5620c65b <https://github.com/HEPCloud/decisionengine/commit/5620c65be6910a30b8b34f2baa914c596f2c94ea>`_:   List why we aren't checking

`88611d90 <https://github.com/HEPCloud/decisionengine/commit/88611d9004df6541959aa40c3c33fe761fada3ef>`_:   Ensure fixtures are cleaned up between invocations

`0ba135d2 <https://github.com/HEPCloud/decisionengine/commit/0ba135d2eed04f9f419e318a408555d591696f1d>`_:   Setup blank DB for SQLAlchemy tests and prep fixtures

`3793e674 <https://github.com/HEPCloud/decisionengine/commit/3793e674eeb495229fea43caefc2057d1092c0e7>`_:   Setup pre-commit

`9e6d1317 <https://github.com/HEPCloud/decisionengine/commit/9e6d13170adc2476a07df89a9df106312545241a>`_:   Migrate test_Reaper to pytest fixtures

`51df43bf <https://github.com/HEPCloud/decisionengine/commit/51df43bfd48340cf18df44043a71aa1c25548ac4>`_:   Cleanup a bunch of pointless whitespace

`96e5d069 <https://github.com/HEPCloud/decisionengine/commit/96e5d06997e53975d5baff0ab86e19951075c023>`_:   Fix typo

`9f96f418 <https://github.com/HEPCloud/decisionengine/commit/9f96f4181b0301d1a7b0a69e0ca10b5ce0baeeac>`_:   Setup datablock to use our parameterized fixture

`36ebc66c <https://github.com/HEPCloud/decisionengine/commit/36ebc66c19a8d20c001447c78744d978a9e3bbf2>`_:   Add config for LGTM

`c6032e5f <https://github.com/HEPCloud/decisionengine/commit/c6032e5f78da2d4ace093f810dd5ca695bfb25cc>`_:   Use topologically sorted transforms to remove some multi-threading.

`e063f82a <https://github.com/HEPCloud/decisionengine/commit/e063f82a813f93f7e7fcf2cb31cdb5484699b405>`_:   Drop pointless comma

`bfd6689e <https://github.com/HEPCloud/decisionengine/commit/bfd6689e123df23f69636b9fb43e59cc6f3abd45>`_:   Begin prepwork for PEP517

`72c5725f <https://github.com/HEPCloud/decisionengine/commit/72c5725faa3bc24b5fa73d63765cd8281d873503>`_:   Stub out null source rather than more complex mocking

`3b65e5e2 <https://github.com/HEPCloud/decisionengine/commit/3b65e5e2eed5ac2025c08d3b7145f8d90ee64d76>`_:   Push Singleton into its own space

`fb5b177e <https://github.com/HEPCloud/decisionengine/commit/fb5b177efa968c16717689a17aa8c35d1b285aac>`_:   Put fixtures in central location

`5ab3cbaa <https://github.com/HEPCloud/decisionengine/commit/5ab3cbaa5ea29dde26b319336dd4f3e6a5aa9de8>`_:   Add more details to channel startup logs

`afe7f7d7 <https://github.com/HEPCloud/decisionengine/commit/afe7f7d79e84f3c6bd3181eb99475e3cd922f881>`_:   Add log about what DB we are hitting

`38034b2c <https://github.com/HEPCloud/decisionengine/commit/38034b2c3ca21f1811a15a32d32870f626a1b76d>`_:   Let the datasource handle the connections internally

`5e03b6fe <https://github.com/HEPCloud/decisionengine/commit/5e03b6fefa953b5806e6ca6785cf71ee3c0e20cd>`_:   Since we are opening an IPv4 socket, just use 127.0.0.1 to check

`cac2bef3 <https://github.com/HEPCloud/decisionengine/commit/cac2bef32d3b503402b5e25503a63acee18c6921>`_:   Fix missing version requirements

`3be8f84f <https://github.com/HEPCloud/decisionengine/commit/3be8f84f36044e2a289197883b852149c4ae1ae9>`_:   Add line length for autoformater

`90e2baad <https://github.com/HEPCloud/decisionengine/commit/90e2baadaa3197f2a0bf277273c081b2f442b76d>`_:   Protect against inappropriate wait under error condition.

`943a17a7 <https://github.com/HEPCloud/decisionengine/commit/943a17a70dca5169c137fabb122c1f27104e291d>`_:   Fix de-client typo and adjust tests accordingly.

`3b104eba <https://github.com/HEPCloud/decisionengine/commit/3b104ebabca7bd4fd1c349e8cd0513a3e6105fee>`_:   Set the logs to DEBUG for testing

`4c5564d4 <https://github.com/HEPCloud/decisionengine/commit/4c5564d4b15096235776e230d8c64cb8f68979f5>`_:   Add another sync method to try and make tests less spotty

`66bd81f2 <https://github.com/HEPCloud/decisionengine/commit/66bd81f2b854c0465026ae13042f20db929edebe>`_:   Make sure to encourage updates to tools

`d16f04cc <https://github.com/HEPCloud/decisionengine/commit/d16f04cc0dbbd832877eabf0655dcdd2d6b6ff9f>`_:   Put postgresql datasource schema into RPM

`62b97e79 <https://github.com/HEPCloud/decisionengine/commit/62b97e79c900920f9613cbf9039b8bf6042aa4a3>`_:   Fix __str__ so it includes all the data

`611ef1f8 <https://github.com/HEPCloud/decisionengine/commit/611ef1f8124126f06de1e94d898a121ad060b5c5>`_:   Drop pointless lines

`5b9e2fb6 <https://github.com/HEPCloud/decisionengine/commit/5b9e2fb6adcf489e1d42dc027446e1a9950b9806>`_:   Drop unreachable excepts

`6991f65f <https://github.com/HEPCloud/decisionengine/commit/6991f65f4ed6cea21198bd623180ffe9c9a086f9>`_:   Restore product-name translation required for some source-proxy cases.

`f6258c09 <https://github.com/HEPCloud/decisionengine/commit/f6258c09a6452e1e2de324c828d8f4c990bd9664>`_:   Fixed formatting and updated content

`104a0446 <https://github.com/HEPCloud/decisionengine/commit/104a04469ff8c7254ce39073b62b64f4487bac45>`_:   Update index.rst

`2ed61289 <https://github.com/HEPCloud/decisionengine/commit/2ed61289c5539a7666754774659487a74a794359>`_:   Update index.rst

`cb687150 <https://github.com/HEPCloud/decisionengine/commit/cb687150f4237e421df9bf25a2bbf3f0d2c45739>`_:   Create release_notes.rst

`3b57d4a2 <https://github.com/HEPCloud/decisionengine/commit/3b57d4a20dfb0162bae4f181ce86832eb16c0c63>`_:   Note new requirement

`871af08b <https://github.com/HEPCloud/decisionengine/commit/871af08bdea2edaa33f942a4f8adffae1a6f9abf>`_:   Added 1.7.0 release notes

`ce42b802 <https://github.com/HEPCloud/decisionengine/commit/ce42b8022742cc1f78cf5216126b015293c9f766>`_:   improved 1.6 release note

`583c10fb <https://github.com/HEPCloud/decisionengine/commit/583c10fb470f7ae1da284dd12abbd179b71e2a0b>`_:   fixed rst error

`96d4dc1e <https://github.com/HEPCloud/decisionengine/commit/96d4dc1ed123606cee0318f1b71421e68ff361df>`_:   Added 1.6.2 release notes, from branch 1.6

`13c2f283 <https://github.com/HEPCloud/decisionengine/commit/13c2f28325d697701d9417fb2116364f018da535>`_:   Add some helpful indexes to our default schema

`29c32571 <https://github.com/HEPCloud/decisionengine/commit/29c32571e837ac51f238360be6f8208a49996ebb>`_:   Log as workers are started

`619021c2 <https://github.com/HEPCloud/decisionengine/commit/619021c24df6a51818ea067b9c33b07a3a579f0f>`_:   One of these tests seems to be spotty, break them out to find which one

`29a2c72d <https://github.com/HEPCloud/decisionengine/commit/29a2c72d55fa71bbdbbc787e90b05e98529a70dc>`_:   Run the test in a way that gives us colors

`4e36bfd2 <https://github.com/HEPCloud/decisionengine/commit/4e36bfd25d7f94730e4412f27c7cc550848c7c2d>`_:   Drop unused table create logic

`5511f69e <https://github.com/HEPCloud/decisionengine/commit/5511f69edbe0720f25edda7c09ca780007747572>`_:   Stronger notify state for when we've a lot of watchers.

`b6cc7a46 <https://github.com/HEPCloud/decisionengine/commit/b6cc7a461c375b4360133c9ae26dd2ad759f3aa7>`_:   Test the dataspace abstractions

`e3b1f594 <https://github.com/HEPCloud/decisionengine/commit/e3b1f594cd1b9462fc5d44372243640f0c2ceb6d>`_:   Better messages about our state

`2d2feab9 <https://github.com/HEPCloud/decisionengine/commit/2d2feab9a9b42339263df6d81c1ada359cc875cf>`_:   Drop duplicate tests, leave specifics

`8e737329 <https://github.com/HEPCloud/decisionengine/commit/8e7373298fcb5869d2137ed13d157a0f65a31946>`_:   Add parameter based datasource api tests

`5c023aa5 <https://github.com/HEPCloud/decisionengine/commit/5c023aa5e4ae9aa68cb69a7edb175f7f8a7318d5>`_:   Don't do debug logs for flake8, they aren't helpful

`f5d1a12f <https://github.com/HEPCloud/decisionengine/commit/f5d1a12fba958c1ecc077575c9b39f7c979fc963>`_:   Setup list of public exports for dataspace.py

`7158b422 <https://github.com/HEPCloud/decisionengine/commit/7158b422c73f51c367e07c59c3cfa88006a61c67>`_:   Merge pull request #365 from jcpunk/bad-update-is-error

`cd98cc4a <https://github.com/HEPCloud/decisionengine/commit/cd98cc4a09dc655417d67cab3a1ffb7e0c455e16>`_:   Update should error out if you try to do it wrongly

`eb7907fe <https://github.com/HEPCloud/decisionengine/commit/eb7907fee07e5866cb193bf1d5b1acfa0a943d54>`_:   Add option to set taskmanager datestamp and sample usage

`e124532c <https://github.com/HEPCloud/decisionengine/commit/e124532cc9c7ac98522dce507962460cfd75e6fb>`_:   Make sure the fixture uses the production flow

`a8241b6e <https://github.com/HEPCloud/decisionengine/commit/a8241b6ee2e938b14ee514d84e49e43f0c844b7c>`_:   Make sure RPM also owns the .egg-info so we don't confuse the namespaces

`da87376e <https://github.com/HEPCloud/decisionengine/commit/da87376e0bcecc0142bd7f651fbde74658563035>`_:   Ensure the DE server is fully started before running query

`622bfacf <https://github.com/HEPCloud/decisionengine/commit/622bfacfab41f6ae477ddb4b95fab86b7d86c0c2>`_:   Simplify use of our PG fixtures

`df98ecdf <https://github.com/HEPCloud/decisionengine/commit/df98ecdf07fa082beb98a5bcce24a290c48a760a>`_:   Fixed flake8 issue

`061ff6cf <https://github.com/HEPCloud/decisionengine/commit/061ff6cff934eadc4e9e7a39bce78a0752b628a6>`_:   decisionengine/framework: stop_channel runs Publisher shutdown methods

`3727b80b <https://github.com/HEPCloud/decisionengine/commit/3727b80beb49ec314579d8c822c94c4c5f37e5e6>`_:   Fixup comment to avoid assuming this test uses the DB

`d45aaf6b <https://github.com/HEPCloud/decisionengine/commit/d45aaf6b160652b021e935b38566558023420b70>`_:   Fix script path typo

`a25a4a30 <https://github.com/HEPCloud/decisionengine/commit/a25a4a3064c879b9e415ec8ece8cc813a3cf7c51>`_:   Fix ABC to match our actual usage

`1510b2d1 <https://github.com/HEPCloud/decisionengine/commit/1510b2d134165b9752101c9b981514ba5b4f8093>`_:   Address minor linting issues

`945e4b16 <https://github.com/HEPCloud/decisionengine/commit/945e4b16a8246d72a65a023501b84258e3d10e66>`_:   Fix missing attribute insert

`5eace9d5 <https://github.com/HEPCloud/decisionengine/commit/5eace9d51c4032585cc8821ccba1c59b36b8a730>`_:   Add note for how to get modules in place

`50a8e268 <https://github.com/HEPCloud/decisionengine/commit/50a8e2688987152523d83d4a8ac2e4d9435fb192>`_:   Add list of packages in the CI env to output

`b9cb197d <https://github.com/HEPCloud/decisionengine/commit/b9cb197d102f4755fb6ad074903ef1ceda983aa9>`_:   Sanity check the home directory

`cd17223c <https://github.com/HEPCloud/decisionengine/commit/cd17223c367ca692a94a3481c91b1c4d3b081abc>`_:   Have client provide a hint when you ask for no behavior

`95b02365 <https://github.com/HEPCloud/decisionengine/commit/95b02365d88e7d3a9f3a69f62491a4016ac77fc5>`_:   Fix de-query-tool to support produce/consume model

`e660ca72 <https://github.com/HEPCloud/decisionengine/commit/e660ca726b3457d4aecf4ae2f18b3e03419cc2f3>`_:   Update required versions for bugfixes

`6863cb81 <https://github.com/HEPCloud/decisionengine/commit/6863cb81174aff1598ac51b723070a1f1bd851f8>`_:   Fix path error

`bb52e8b1 <https://github.com/HEPCloud/decisionengine/commit/bb52e8b1659dea39aa3b853056893d7d85c343e0>`_:   Merge pull request #340 from jcpunk/service-stop

`6d7aba95 <https://github.com/HEPCloud/decisionengine/commit/6d7aba953ffce34d27685029b05f03977c4baf5f>`_:   Drop obsolete files

`168ae7aa <https://github.com/HEPCloud/decisionengine/commit/168ae7aa0cc136a56b064e2a4d4f81aab746fa92>`_:   Name the tests better

`0f60c4e3 <https://github.com/HEPCloud/decisionengine/commit/0f60c4e3911686a47a12819c2276801e7868fa8e>`_:   Support new produces/consumes/configuration-description infrastructure.

`81912469 <https://github.com/HEPCloud/decisionengine/commit/819124695fbf8cb75ccbd7bf861d07b85fa1ab32>`_:   Add de-query-tool

`2a26c944 <https://github.com/HEPCloud/decisionengine/commit/2a26c9442938a376aa070c03fe6e12d4f744c9f0>`_:   ExecStopPre is not supported on all systemd instances

`67a54d5c <https://github.com/HEPCloud/decisionengine/commit/67a54d5cceeb9d4e5c6c7eaff8fa0e312d252f7a>`_:   Merge pull request #338 from jcpunk/fix-pytest-postgres

`70ab133f <https://github.com/HEPCloud/decisionengine/commit/70ab133ff92a82972bcefd36e989c1b373688b74>`_:   Fixup use of pytest_postgresql for version 3.0.0

`f8f4255e <https://github.com/HEPCloud/decisionengine/commit/f8f4255eb3dee4ab92e20df7f72e840c643f02a5>`_:   Merge pull request #337 from jcpunk/thread-names

`5f49a4f6 <https://github.com/HEPCloud/decisionengine/commit/5f49a4f63a1bd24e24ef91e2d870b8af5585f943>`_:   Set names for the various parallel code

`64da77c6 <https://github.com/HEPCloud/decisionengine/commit/64da77c6de71787386911e41b120627427c87fc8>`_:   Merge pull request #327 from jcpunk/datablock-expire

`de33a60a <https://github.com/HEPCloud/decisionengine/commit/de33a60a19510d1cbfea47c01c19eea7aef78e1c>`_:   Merge pull request #336 from knoepfel/use-toposort

`31a8a905 <https://github.com/HEPCloud/decisionengine/commit/31a8a9053a2067c6a14485bcaf96fb3724a42547>`_:   Merge pull request #328 from knoepfel/de-class-inference

`410e383d <https://github.com/HEPCloud/decisionengine/commit/410e383de712bdd5fcd5a6cc6e04deca8ce923bb>`_:   Merge pull request #331 from jcpunk/reaper-interval-tests

`719ff0c8 <https://github.com/HEPCloud/decisionengine/commit/719ff0c85a77376c19d7681bdf18c7abfc1f9c5d>`_:   Test datablock expire functions

`e14c49d8 <https://github.com/HEPCloud/decisionengine/commit/e14c49d80537b549fea884546378fc5917c1591b>`_:   The 'name' parameter is optional.

`7846c9f3 <https://github.com/HEPCloud/decisionengine/commit/7846c9f3f9a0a83b0de168b30569138763691a21>`_:   Enable DE class inference based on configuration.

`32ab7e44 <https://github.com/HEPCloud/decisionengine/commit/32ab7e44c4c748938d7837ac96d12bf7a92525fc>`_:   Use third-party topological sort.

`01aa8ae6 <https://github.com/HEPCloud/decisionengine/commit/01aa8ae678f598f0b1b1941b63dcc6df66852304>`_:   Merge pull request #325 from jcpunk/channel-tests

`52b48479 <https://github.com/HEPCloud/decisionengine/commit/52b48479094c37acc5422301cc0ebce721db65bc>`_:   Merge pull request #326 from jcpunk/valid-config-tests

`8c4749e7 <https://github.com/HEPCloud/decisionengine/commit/8c4749e7d61727b820fee8b86ca572b4fe68585f>`_:   Merge pull request #330 from jcpunk/pylint-actions

`a37770c9 <https://github.com/HEPCloud/decisionengine/commit/a37770c9527932f81d754119524ffff6f8406c4d>`_:   Ensure validation testing is tested

`d8ab5eb6 <https://github.com/HEPCloud/decisionengine/commit/d8ab5eb6fd0998167635923a391d94785ab6a53f>`_:   Add missing test to ensure the run interval is actually used

`0cd9c42b <https://github.com/HEPCloud/decisionengine/commit/0cd9c42b708179a25cb4998466a39c86db66e069>`_:   Also run pylint for extra sanity checks

`c5cf1fff <https://github.com/HEPCloud/decisionengine/commit/c5cf1fff9e5b191c4fd913d185805b5d3dbabecd>`_:   Ensure our errors error out

`baf01700 <https://github.com/HEPCloud/decisionengine/commit/baf01700d8bb6cf4f8aca28e7fdd0726e3f617e0>`_:   Merge pull request #324 from jcpunk/cleanup-trivial-tests

`2a0133aa <https://github.com/HEPCloud/decisionengine/commit/2a0133aadfba0fef2a70fcf43528bb60b7ed01bb>`_:   Try to cleanup trivial missing coverage

`44e0ad6f <https://github.com/HEPCloud/decisionengine/commit/44e0ad6f039dc2982f8e72cd56bcf0caf6737e5c>`_:   Merge pull request #323 from jcpunk/about-coverage

`d811f617 <https://github.com/HEPCloud/decisionengine/commit/d811f6174ecd77e40e84fac8b5eabe1d24aaa69d>`_:   Merge pull request #322 from knoepfel/fix-fail-on-error

`cb426262 <https://github.com/HEPCloud/decisionengine/commit/cb42626213ffed843eae5916c2b1fd535d9883f1>`_:   Merge pull request #312 from jcpunk/finish-setuptools

`8f6d407d <https://github.com/HEPCloud/decisionengine/commit/8f6d407de53f95602a3dce29603d23ab0ea4390c>`_:   Merge pull request #316 from jcpunk/abc-coverage

`4d0676bb <https://github.com/HEPCloud/decisionengine/commit/4d0676bbe82d9b3adf89b0b660734755b5f14168>`_:   Merge pull request #317 from vitodb/pylint

`d7c43b96 <https://github.com/HEPCloud/decisionengine/commit/d7c43b961dbc4f092fdd39a73277be5d73dc9c2c>`_:   Use regular expression to support fail_on_error feature.

`ada66925 <https://github.com/HEPCloud/decisionengine/commit/ada6692533280d4171804ae2cc26f5337d721f0f>`_:   add support to run pylint tests

`efb1e57b <https://github.com/HEPCloud/decisionengine/commit/efb1e57bfdb7c03420440d34ad679eb5da618bc4>`_:   Finish migration to pure setuptools

`bc4720cf <https://github.com/HEPCloud/decisionengine/commit/bc4720cf0e65f1df2b73958cbd64c5dabf84764c>`_:   We aren't testing 'unversioned" releases

`e4dc35e3 <https://github.com/HEPCloud/decisionengine/commit/e4dc35e36f75b14c71e0626afc7e1376adbac3df>`_:   Merge pull request #314 from jcpunk/jsonnet_syntax

`87e32c22 <https://github.com/HEPCloud/decisionengine/commit/87e32c228376bbe5a3cf513ac2890b2a8b7b793b>`_:   Merge pull request #294 from jcpunk/move-reaper

`dec85d5e <https://github.com/HEPCloud/decisionengine/commit/dec85d5ebb7cf9b8fb19c73ac5a68e9855503dba>`_:   Merge pull request #319 from jcpunk/task-loop

`4108472a <https://github.com/HEPCloud/decisionengine/commit/4108472afc04def8c35f7aaa569fd76568cf162f>`_:   Merge pull request #320 from jcpunk/container-swig

`920af1c9 <https://github.com/HEPCloud/decisionengine/commit/920af1c985f84896d92a1f5fe28ee8072d654247>`_:   Merge pull request #321 from knoepfel/include-init-files

`650dffa7 <https://github.com/HEPCloud/decisionengine/commit/650dffa70ea4bcca0022adb79823d53d81849d70>`_:   Don't forget __init__.py files.

`1b412e03 <https://github.com/HEPCloud/decisionengine/commit/1b412e03067216451d0552f434277d6069300ae3>`_:   The latest m2crypto seems to need swig now

`a6e3ab1c <https://github.com/HEPCloud/decisionengine/commit/a6e3ab1c283e5ec596cde771db9fd3fc6d97125d>`_:   Merge pull request #313 from jcpunk/conf-test

`1205636a <https://github.com/HEPCloud/decisionengine/commit/1205636a69763ef71d1baa273c92d0dbc51e46db>`_:   Simplify run loop

`30e59dc9 <https://github.com/HEPCloud/decisionengine/commit/30e59dc967285d13221dfee7b807f446f9fbfac2>`_:   fix test_client_with_no_server_verbose unit test for Jenkins CI (#315)

`10384a8c <https://github.com/HEPCloud/decisionengine/commit/10384a8cf3167bbadc0bfea08291c9eeb20cb01c>`_:   Move reaper into its own place and reuse state logic

`940584e4 <https://github.com/HEPCloud/decisionengine/commit/940584e446d9841e006b87dc5a0446cc52e664d8>`_:   No real way to test abstract base classes

`250c14b1 <https://github.com/HEPCloud/decisionengine/commit/250c14b151ba273417c09306556e591e9981d768>`_:   The `_validate` function doesn't permit missing 'PRODUCES'

`5ae1ce9f <https://github.com/HEPCloud/decisionengine/commit/5ae1ce9fc748a146777dd8f5bd63a96a7bc09fac>`_:   Make sure syntax error in config names the problem

`b899fa23 <https://github.com/HEPCloud/decisionengine/commit/b899fa237d20f949f1adf147fa7d6da55381b4b2>`_:   Add SourceProxy module test. (#307)

`7b3df14c <https://github.com/HEPCloud/decisionengine/commit/7b3df14c7a26c9d3ba2b0e56ac4598ed8d3c4d80>`_:   Increase coverage of utils (#304)

`ddba2a31 <https://github.com/HEPCloud/decisionengine/commit/ddba2a312884208b80682c7ecf3162234cf434e7>`_:   Fix duplicate entry warning (#311)

`915673fa <https://github.com/HEPCloud/decisionengine/commit/915673fac5b37ccce0804fb2c2df969a92726f6b>`_:   Test modules minimally (#298)

`bc0c21a9 <https://github.com/HEPCloud/decisionengine/commit/bc0c21a924e097bfda51769228c787f69ae474e6>`_:   Some repos may error out, don't let them kill the build (#297)

`924a7047 <https://github.com/HEPCloud/decisionengine/commit/924a7047a31d2fe69de04f5c97ef89eefc600fa3>`_:   doc: add 1.6.1 release notes

`b1ab4d31 <https://github.com/HEPCloud/decisionengine/commit/b1ab4d31d3b935929b39c553dd71135732bb9922>`_:   doc: fix typo

`85e5d714 <https://github.com/HEPCloud/decisionengine/commit/85e5d71454c018c84e30a81edd256f24c23e9fd9>`_:   postgresql: do not print stack trace for low level library (#309)

`255c6415 <https://github.com/HEPCloud/decisionengine/commit/255c641505fce253ac3c854cbda3287e15e0524b>`_:   Setuptools uses entry return value as an error msg (#303)

`2fd8db45 <https://github.com/HEPCloud/decisionengine/commit/2fd8db454e1329b72eac292df9176c2a4c820261>`_:   Fix name to match expectations (#305)

`9cddb70a <https://github.com/HEPCloud/decisionengine/commit/9cddb70a5a6d74553868b8940139db00d59f2429>`_:   updated release notes

`7fe0358e <https://github.com/HEPCloud/decisionengine/commit/7fe0358eedae19e2bb0d33a5fa6a908a17424e28>`_:   Error in more clean methods (#300)

`84aa506c <https://github.com/HEPCloud/decisionengine/commit/84aa506cfa8d3838a30039eb7d47b62f64d23db9>`_:   Fix a bug in setup.py parsing of requirements. (#301)

`a58b61bb <https://github.com/HEPCloud/decisionengine/commit/a58b61bb421e41404532e9182ab3f28da8a77837>`_:   fix typo in release notes
