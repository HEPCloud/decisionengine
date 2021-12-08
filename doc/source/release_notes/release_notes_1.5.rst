.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.5.0
-------------

In this release:

* Introduce data product query interface
* Cleanup of Ligic Engine code
* Improvements in error handling
* Improvements in testing and CI

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `217 <https://github.com/HEPCloud/decisionengine/issues/217>`_ , `218 <https://github.com/HEPCloud/decisionengine/issues/218>`_ : Add option to de-client --print-product to only print the column names in a data block and-or to print one or more records in key/value format (`fe7abcf <https://github.com/HEPCloud/decisionengine/commit/fe7abcf858482fae8d966598ee57408b7995f52b>`_)

- `240 <https://github.com/HEPCloud/decisionengine/issues/240>`_ : Logic Engine call leads to immediate taskmanager segfault exit (`d855aa0 <https://github.com/HEPCloud/decisionengine/commit/d855aa04277c5d1ebbfeb427cdbda38877e29a3a>`_)

- `239 <https://github.com/HEPCloud/decisionengine/pull/239>`_ : implement data product browsing interface (`fe9faa9 <https://github.com/HEPCloud/decisionengine/commit/fe9faa9da15864c6c3c5d9aa10efc8086536a3a9>`_)


Full list of commits since version 1.4.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`d66c54b <https://github.com/HEPCloud/decisionengine/commit/d66c54b39be7b6d8d175d287c02d35e492afcaa4>`_
:   Add PEP-0396 metadata (#243)

`bfc91a6 <https://github.com/HEPCloud/decisionengine/commit/bfc91a616ede569436fd4c296817e002f79ec3de>`_
:   More compat between psycopg2/psycopg2cffi (#248)

`f5d31a6 <https://github.com/HEPCloud/decisionengine/commit/f5d31a6d735335ff8bc6dddbffc51a054a8798b0>`_
:   Cleanup Fixture FIXME (#249)

`0dfaf3c <https://github.com/HEPCloud/decisionengine/commit/0dfaf3ca9f1ec96a89ee68a9cf14cd16002c5806>`_
:   Adding docker documentation (#251)

`4b166a2 <https://github.com/HEPCloud/decisionengine/commit/4b166a26b8a72b0b5156c0d69c60667974a18188>`_
:   Since we are python3 only now, drop python-six compat layer (#252)

`fe7abcf <https://github.com/HEPCloud/decisionengine/commit/fe7abcf858482fae8d966598ee57408b7995f52b>`_
:   Add format support to de-client (#217) (#241)

`df5a3d7 <https://github.com/HEPCloud/decisionengine/commit/df5a3d7cd736429a7f4844fd221f1b2082ece6d5>`_
:   Add wheel support for easier testing (#247)

`7de970d <https://github.com/HEPCloud/decisionengine/commit/7de970d6cbd6dea24cd2b5f98ee13272f025aaaf>`_
:   Add place to inject env if need be (#242)

`84e2930 <https://github.com/HEPCloud/decisionengine/commit/84e293063fbfb02715e02010d081be804904ba46>`_
:   Fix race in test case (#250)

`d855aa0 <https://github.com/HEPCloud/decisionengine/commit/d855aa04277c5d1ebbfeb427cdbda38877e29a3a>`_
:   Fix fact-lookup to support duplicate names in separate rules. (#245)

`51370fb <https://github.com/HEPCloud/decisionengine/commit/51370fb576baabb725f596fc5d41d7bfb2ce3409>`_
:   Resolve fixture 'quickstart' issue (#238)

`3ea9129 <https://github.com/HEPCloud/decisionengine/commit/3ea91296a75ab66e00c72cb12bf4436111dfde35>`_
:   Move from TravisCI to raw actions (#235)

`fe9faa9 <https://github.com/HEPCloud/decisionengine/commit/fe9faa9da15864c6c3c5d9aa10efc8086536a3a9>`_
:   implement data product browsing interface (#239)

`cf0f3c0 <https://github.com/HEPCloud/decisionengine/commit/cf0f3c0be3c5cfcc86c6da0976dbdc1a8ebc075e>`_
:   Add support to use custom base docker container to run tests (#234)

`d91722f <https://github.com/HEPCloud/decisionengine/commit/d91722f677895b8eaf9c1157f1a1df9603ed0dd1>`_
:   Compat with psycopg2cffi (#233)

`7d15a8c <https://github.com/HEPCloud/decisionengine/commit/7d15a8c932b2fed1bbdfd523eb0c951d3814bd7a>`_
:   Test failing source proxy. (#232)

`b9a4bbb <https://github.com/HEPCloud/decisionengine/commit/b9a4bbb432ef585a951163d66b614f5045dab2f0>`_
:   Add debug logs for which threads are created #176 (#231)

`6e6f4c9 <https://github.com/HEPCloud/decisionengine/commit/6e6f4c931f953018ade808ef0c682080cd29fced>`_
:   Updated Jenkins configuration documentation (#229)

`2d9fd7b <https://github.com/HEPCloud/decisionengine/commit/2d9fd7b810654a912ad9929b97a48f61df41cfe9>`_
:   Log if config passed validation #117 (#230)

`60c46d3 <https://github.com/HEPCloud/decisionengine/commit/60c46d363e0390fab5f13103850810f4ce45e781>`_
:   Self-test needs a real namespace to 'import numpy' in new python eval (#228)

`a120077 <https://github.com/HEPCloud/decisionengine/commit/a12007704f633fedc68e57e646939f5a891eb11e>`_
:   Test that the doc actually builds during CI (#227)

`4b6240a <https://github.com/HEPCloud/decisionengine/commit/4b6240a5fee7601abf6b434ae26bd5110f445b81>`_
:   Extend timeout for coverage combine (#226)

`b059696 <https://github.com/HEPCloud/decisionengine/commit/b059696607857204c0572c4bf77e4d391c8682e1>`_
:   Update workflow per changes at github (#225)

`7a71cac <https://github.com/HEPCloud/decisionengine/commit/7a71cacd320b19e2eabad9e7cced535899750adf>`_
:   Use newer compilers/runtimes (#224)

`15ffd93 <https://github.com/HEPCloud/decisionengine/commit/15ffd93abc1cb4ccb393237d72aa547f3b586c87>`_
:   Add header for strict includes (#222)

`71b141a <https://github.com/HEPCloud/decisionengine/commit/71b141a4d432945b6aea79921d130a7ddeeeec8d>`_
:   Add special PyPy only requirement (#221)

`9dbb932 <https://github.com/HEPCloud/decisionengine/commit/9dbb93256293d50a52842dea193e6dde508b975f>`_
:   Move Python C extension to versioned .so file (#220)

`ea7ade5 <https://github.com/HEPCloud/decisionengine/commit/ea7ade57ca825afb0afbfa5ebd49820b16786d8b>`_
:   Migrate from boost-python to pybind11 (#215)

`e6b2eae <https://github.com/HEPCloud/decisionengine/commit/e6b2eae013f7d2b31c7bc45aeec99a2dfef227df>`_
:   Add python 3.9 to testing matrix (#219)

`04c8f9c <https://github.com/HEPCloud/decisionengine/commit/04c8f9ce2cce1dcfde27dc9dc3eaeb96e6c7b4b8>`_
:   Add the option to print columns types on de-client (#216)

`8815dc6 <https://github.com/HEPCloud/decisionengine/commit/8815dc6d7233fc3695b7d9bb3e33f142fb5ebeca>`_
:   Logic-engine cleanups (#211)

`086d0d5 <https://github.com/HEPCloud/decisionengine/commit/086d0d5fa5f2ff8c4ea5e1d575629d1244f2f588>`_
:   fix missing back tick

`54cc084 <https://github.com/HEPCloud/decisionengine/commit/54cc084e9277414ff4be54bd34e5894c3c0112eb>`_
:   modified release notes

`24744cf <https://github.com/HEPCloud/decisionengine/commit/24744cfab809d34fae830806c51d5adcbc69414a>`_
:   Synchronize access to the task managers (#214)

`87a7fda <https://github.com/HEPCloud/decisionengine/commit/87a7fda2c1985f477dcd4f7ce6a87393f2ab8800>`_
:   replde dash with underscore

`743d0fd <https://github.com/HEPCloud/decisionengine/commit/743d0fd8717cd8fce6aeca623b32f026bcb65350>`_
:   try sphinx_rtd_theme

`18c7909 <https://github.com/HEPCloud/decisionengine/commit/18c79095d1ffa61c7befdcdb704acb0ec5614380>`_
:   added 1.4.0 release notes

`ff3d491 <https://github.com/HEPCloud/decisionengine/commit/ff3d4914acc22d48940298095d4a6dbda32fe767>`_
:   force docker pull when building the docker container to make sure to use an updated base layer (#210)
