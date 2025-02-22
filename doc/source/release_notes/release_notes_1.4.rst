.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.4.1
-------------

In this release:

* Bug fixes to 1.4.0 release

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `213 <https://github.com/HEPCloud/decisionengine/issues/213>`_ : de-client hangs under certain circumstances in version 1.4 and greater (race condition) (`84ecfe2 <https://github.com/HEPCloud/decisionengine/commit/84ecfe2501a09aa1375552c1afe16576cc9ee80f>`_)


Full list of commits since version 1.4.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`9799b9a <https://github.com/HEPCloud/decisionengine/commit/9799b9abe4c6c900819248b4143f7f0f93876a3c>`_
:   update release version to 1.4.1

`84ecfe2 <https://github.com/HEPCloud/decisionengine/commit/84ecfe2501a09aa1375552c1afe16576cc9ee80f>`_
:   Synchronize access to the task managers (#214)

`751b6b8 <https://github.com/HEPCloud/decisionengine/commit/751b6b8f8a4bf8407b1b0cc8c5416682dc98ce8c>`_
:   Address data races; remove need to sleep in unit tests (#205)



Release 1.4.0
-------------

In this release:


* Improvements in error handling and client/server interactions
* Added log rotation by time
* Improvements in code coverage

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `153 <https://github.com/HEPCloud/decisionengine/issues/153>`_ : Have de-client --print-product return different error message if product does not exist (`18a950c <https://github.com/HEPCloud/decisionengine/commit/18a950c9ac9cd16cc05659178bc49c0ef0dd5147>`_)
- `171 <https://github.com/HEPCloud/decisionengine/issues/171>`_ : yum update on decision engine rpm from python2 to python3 doesn't undo the symlinks (`eb85c97 <https://github.com/HEPCloud/decisionengine/commit/eb85c97f0436097a754dd8baa8870194a5d64531>`_)
- `188 <https://github.com/HEPCloud/decisionengine/issues/188>`_ : Channel debug info now leaks into startup.log (`99d20a5 <https://github.com/HEPCloud/decisionengine/commit/99d20a5117ee87ee6fcd16c4dc85673c2118ffdd>`_)
- `208 <https://github.com/HEPCloud/decisionengine/issues/208>`_ : Error when trying to run reaper in version 1.4.0 (`84eccf3 <https://github.com/HEPCloud/decisionengine/commit/84eccf37f24837fd188f7e93103a67ef5fde2aeb>`_)


Full list of commits since version 1.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`84eccf3 <https://github.com/HEPCloud/decisionengine/commit/84eccf37f24837fd188f7e93103a67ef5fde2aeb>`_
:   Fix typo in reaper script. (#209)

`d836abf <https://github.com/HEPCloud/decisionengine/commit/d836abfb72b3d26d5d9401cb532bd3093e597399>`_
:   next RC

`926944a <https://github.com/HEPCloud/decisionengine/commit/926944ac2f9ca3a30790109f2bdac6181b295d5b>`_
:   Fix coveralls reporting (#198)

`b95c323 <https://github.com/HEPCloud/decisionengine/commit/b95c3232dec1308b539846118fd8afd3f3c179ea>`_
:   Updating base Dockerfile (#199)

`d302e31 <https://github.com/HEPCloud/decisionengine/commit/d302e31cd16032a79a2f2b4fb2d8bf5825bc248b>`_
:   Help jsonnet, which doesn't understand PosixPath objects. (#204)

`2d791a7 <https://github.com/HEPCloud/decisionengine/commit/2d791a79b3aad37eda19a7cf89b6a3dd78d585de>`_
:   Test configuration policies. (#197)

`236e27a <https://github.com/HEPCloud/decisionengine/commit/236e27aff03a411c3a292a7d11cd8f7fb389511b>`_
:   Ensure items are returned in a stable order (#202)

`e974f5f <https://github.com/HEPCloud/decisionengine/commit/e974f5faa13d99ebd2634e4141490c7025e8fbe4>`_
:   add pylinit and pycodestyle (#203)

`fbe7616 <https://github.com/HEPCloud/decisionengine/commit/fbe7616265244aabf08d3718df044b0d3cbdfe9d>`_
:   Test task manager (#196)

`686ca80 <https://github.com/HEPCloud/decisionengine/commit/686ca802fc9bbb3f8e782a757120c31c41a3c9f2>`_
:   require more recent version of pytest-postgresql (#195)

`99d20a5 <https://github.com/HEPCloud/decisionengine/commit/99d20a5117ee87ee6fcd16c4dc85673c2118ffdd>`_
:   Fix double-logging problem. (#192)

`4ce3d17 <https://github.com/HEPCloud/decisionengine/commit/4ce3d173626f141afc1561ba2602218751925953>`_
:   A set of fixtures to simplify unit tests (#183)

`65f8052 <https://github.com/HEPCloud/decisionengine/commit/65f805299d901039d08a1e1f4345660df35e6120>`_
:   Fix typo (#190)

`f3a4be8 <https://github.com/HEPCloud/decisionengine/commit/f3a4be859e71659104fb05351502a182dd0a6f39>`_
:   Protect against None workers (#187)

`ec310fb <https://github.com/HEPCloud/decisionengine/commit/ec310fb96a6dcfa53c33f13561184523385a55e3>`_
:   remove py3 from package name

`7006489 <https://github.com/HEPCloud/decisionengine/commit/7006489f9af4bb3d894973d0dc5728e078fa0125>`_
:   bump version to 1.4.0rc

`158d835 <https://github.com/HEPCloud/decisionengine/commit/158d83501c2c353514fe2221f31fa41ee50aa8ae>`_
:   decisionengine/framework/modules: Fix SourceProxy retries (#184)

`1356bf1 <https://github.com/HEPCloud/decisionengine/commit/1356bf1e8c1695db5d57a4dded5f8fc8188f6607>`_
:   Add support to test any branch in Jenkins (#182)

`692fa8e <https://github.com/HEPCloud/decisionengine/commit/692fa8ee77909a02dcc630095812744b6f4c9759>`_
:   Add timeout support for unit test on Jenkins (#181)

`e3d6e6a <https://github.com/HEPCloud/decisionengine/commit/e3d6e6af290996ae0c499bfb3c120d2f510d0a31>`_
:   Updated Jenkins documentation to take into account unit tests timeout parameter (#180)

`2586a3e <https://github.com/HEPCloud/decisionengine/commit/2586a3e9b861b9987017e25293bef7cbbde26413>`_
:   Configuration redesign (#168)

`fac984d <https://github.com/HEPCloud/decisionengine/commit/fac984d53429eb69af7d556d1c9622d13416a8db>`_
:   Fix error with DBUtils import. Looks like names of modules changed (#175)

`7d661ee <https://github.com/HEPCloud/decisionengine/commit/7d661ee325be6f4efc368bdc61a54952321df34f>`_
:   Move postgres-specific implementation to postgres source. (#174)

`eb85c97 <https://github.com/HEPCloud/decisionengine/commit/eb85c97f0436097a754dd8baa8870194a5d64531>`_
:   Rpm (#173)

`10fe843 <https://github.com/HEPCloud/decisionengine/commit/10fe8432c607adbf5791cc38e3fee9b9a4402058>`_
:   Adding log rotation by time (#170)

`a8d239b <https://github.com/HEPCloud/decisionengine/commit/a8d239bf34facd1f405ed7e0cd4c502f8240ad5a>`_
:   Various improvements. (#167)

`d9b92ee <https://github.com/HEPCloud/decisionengine/commit/d9b92eeb445f70453fab7ec9a67b3269008b139e>`_
:   Ignore vim's \*.swp files (#166)

`d9f72ef <https://github.com/HEPCloud/decisionengine/commit/d9f72efa1ceac1da2eaeb1e6dc1360b8ca612dbb>`_
:   Fix call to shutdown_timeout (and add sample entry to config) (#165)

`3161795 <https://github.com/HEPCloud/decisionengine/commit/3161795f52bce858b87fb1025abc654740977d19>`_
:   Add drops for items using tables being dropped (#164)

`77d186d <https://github.com/HEPCloud/decisionengine/commit/77d186df20baf72c27dbe45ace1fd6580bcd4b7f>`_
:   Show output of test runtimes in travis (#163)

`81820a4 <https://github.com/HEPCloud/decisionengine/commit/81820a4a8f16c8c6433692de1fdd182ce19ad03b>`_
:   Allow server to start with no channels. (#161)

`49879a6 <https://github.com/HEPCloud/decisionengine/commit/49879a6e4f51d032c69c2032cceec6788816a3ed>`_
:   DE server and client usability improvements (#160)

`de91c4f <https://github.com/HEPCloud/decisionengine/commit/de91c4f42f7e4a0d1a5aaf49f45dbb0af7207411>`_
:   Add tests to default and override config (#158)

`14df1f6 <https://github.com/HEPCloud/decisionengine/commit/14df1f6a49f5975e2b3eba2eab153cd9ba8eabe9>`_
:   Use python fallthrough for options (#159)

`ac64a92 <https://github.com/HEPCloud/decisionengine/commit/ac64a92bf0059b9c3a80bedc5daa199b4fb7aab1>`_
:   Drop python 2.7 integration tests since we are python3 only (#157)

`d963301 <https://github.com/HEPCloud/decisionengine/commit/d963301489cc60a254d07061a5a581af08a8290d>`_
:   Update Jenkins pipeline to properly test closing PR (#156)

`64248cb <https://github.com/HEPCloud/decisionengine/commit/64248cb12e9c9a3fab5d586576cd7624d450e587>`_
:   Merge 'runtime' tests into running channel tests (#150)

`065ad77 <https://github.com/HEPCloud/decisionengine/commit/065ad77549a040d48f4bf3e750b057bfc6b25124>`_
:   Adding Jenkins pipeline documentation (#155)

`18a950c <https://github.com/HEPCloud/decisionengine/commit/18a950c9ac9cd16cc05659178bc49c0ef0dd5147>`_
:   fix print-product to report non-existing product as such (#154)

`6493735 <https://github.com/HEPCloud/decisionengine/commit/6493735e031950501abce2c3a82f4cb5d83b1204>`_
:   Fix invalid attribute name (#152)

`d953c6a <https://github.com/HEPCloud/decisionengine/commit/d953c6a3d431370cd5aa6fb8fafdf0b61684202a>`_
:   Remove unnecessary set_start_method call (#149)

`c8c9b65 <https://github.com/HEPCloud/decisionengine/commit/c8c9b65447511222c1aae74ddcaf07cca2afd3dc>`_
:   guarantee that process is killed so test never hang (#147)

`f1542b6 <https://github.com/HEPCloud/decisionengine/commit/f1542b63033c931682577dd6896c0d4cb8dcef95>`_
:   Channel test (#146)

`7f349a8 <https://github.com/HEPCloud/decisionengine/commit/7f349a86130015e0b465e9c00103a1b967e5e3e2>`_
:   Fix faulty TaskManager state type (#145)

`d50f1c4 <https://github.com/HEPCloud/decisionengine/commit/d50f1c4856397f613400af02aebc1e473dcc5b19>`_
:   fix logging regression introduced in f5e299969e0611e3480e9fa2782052df… (#142)

`becfa26 <https://github.com/HEPCloud/decisionengine/commit/becfa26641fdca6b8368e27ab171973cedbd6e49>`_
:   Pass the correct type. (#144)

`1a60daf <https://github.com/HEPCloud/decisionengine/commit/1a60daf37128f7239a115a0a19b4aa7bfef93d9f>`_
:   DecisionEngine: fix typo (#143)

`9e7b867 <https://github.com/HEPCloud/decisionengine/commit/9e7b867b7971ec5697a852af5d3259525a91a29d>`_
:   Updating Jenkins pipeline configuration (#140)

`e3a6703 <https://github.com/HEPCloud/decisionengine/commit/e3a67031adff5de3807344a4080d57ce3c1333aa>`_
:   fix regression introduced in f5e299969e0611e3480e9fa2782052df86d7c4ed (#141)

`4900bc6 <https://github.com/HEPCloud/decisionengine/commit/4900bc6a7b56ed776998f78d0883d76cfba022be>`_
:   Restore runtime test. (#139)

`0823f3d <https://github.com/HEPCloud/decisionengine/commit/0823f3d5f340dbf242100c651be82fe86778c7bd>`_
:   Consolidate DE server/client tests into one file. (#138)

`4f84435 <https://github.com/HEPCloud/decisionengine/commit/4f84435f1c2d8bfd03ff4f87fad130a659f3aabb>`_
:   A few more access fixes.

`160cfd1 <https://github.com/HEPCloud/decisionengine/commit/160cfd15d2006efa2c798747d4a54d9081243a64>`_
:   Fix task manager state access.

`c00d819 <https://github.com/HEPCloud/decisionengine/commit/c00d819dd85c2c1d36ac541c88810fa8908659c1>`_
:   A few more cleanups.

`ec087e2 <https://github.com/HEPCloud/decisionengine/commit/ec087e264079042cd910507746d39a48096db882>`_
:   Various cleanups

`a309ffe <https://github.com/HEPCloud/decisionengine/commit/a309ffecc673d9531480582ca11b1e4919fdb2c5>`_
:   Improvements to DE client CLI.
