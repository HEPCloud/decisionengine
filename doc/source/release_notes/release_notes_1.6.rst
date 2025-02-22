.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.6.2
-------------

Patch level (bug fix) release.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugs fixed

- `DEM 200 <https://github.com/HEPCloud/decisionengine_modules/issues/200>`_ (part of it): Invoke correctly channels shutdown: (`75eaa90 <https://github.com/HEPCloud/decisionengine/commit/75eaa90d4585e82d0569d79d0d59a7078450a9df>`_)
- no issue: Use regular expression to support fail_on_error feature (`1386d20 <https://github.com/HEPCloud/decisionengine/commit/1386d20b26f02fcbf7c50c7cddfbff6ff7da8934>`_)

Enhancements:

- Improved CI support (e.g. added pylint tests)
- `217 <https://github.com/HEPCloud/decisionengine/issues/217>`_: Add option to de-client --print-product to only print the column names in a data block and-or to print one or more records in key/value format. (`c4c7681 <https://github.com/HEPCloud/decisionengine/commit/c4c7681ccb391acdca1da79a972f2cbf8b31b87a>`_)



Full list of commits since version 1.6.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`c4c7681 <https://github.com/HEPCloud/decisionengine/commit/c4c7681ccb391acdca1da79a972f2cbf8b31b87a>`_:   Updated de-query-tool w/ cherry pick of fixes from latest version of PR#332

`f964d4b <https://github.com/HEPCloud/decisionengine/commit/f964d4bda01cfd16396c0a6afaa3baab3fb9cb8c>`_:   Fixup use of pytest_postgresql for version 3.0.0

`635ffd1 <https://github.com/HEPCloud/decisionengine/commit/635ffd1b08203a7b38d81858470f2b46f0e915cf>`_:   Also run pylint for extra sanity checks

`11676ff <https://github.com/HEPCloud/decisionengine/commit/11676ff1c0ddc76f9b7eb99fabdcd71cc974b405>`_:   Fixed function w/ the same name

`b8278f6 <https://github.com/HEPCloud/decisionengine/commit/b8278f6fdabdecc7c4ad79834dd7e1c41975cd60>`_:   Add de-query-tool

`75eaa90 <https://github.com/HEPCloud/decisionengine/commit/75eaa90d4585e82d0569d79d0d59a7078450a9df>`_:   Merge pull request #335 from shreyb/publisher_shutdown_from_1.6

`77e3d79 <https://github.com/HEPCloud/decisionengine/commit/77e3d79d4a9418dd5cde9ffc694e7271b1e11e9f>`_:   Added set_to_shutdown method to TaskManager and accompanying test

`1386d20 <https://github.com/HEPCloud/decisionengine/commit/1386d20b26f02fcbf7c50c7cddfbff6ff7da8934>`_:   Merge branch 'knoepfel-fix-fail-on-error' into 1.6

`73a18b1 <https://github.com/HEPCloud/decisionengine/commit/73a18b1332f461840932f660ef71842e05d775e3>`_:   Merge branch 'fix-fail-on-error' of https://github.com/knoepfel/decisionengine into knoepfel-fix-fail-on-error

`4f49fb7 <https://github.com/HEPCloud/decisionengine/commit/4f49fb7b6604b181487c990fcf8236e929bde86b>`_:   Merge branch 'jcpunk-finish-setuptools' into 1.6

`a5e5d39 <https://github.com/HEPCloud/decisionengine/commit/a5e5d39d5f54042c196e79a228f87f3ffdc5da0b>`_:   Merge branch 'finish-setuptools' of https://github.com/jcpunk/decisionengine into jcpunk-finish-setuptools

`a1ed252 <https://github.com/HEPCloud/decisionengine/commit/a1ed252dec3ca9aa0c0852bdbc9ec3526f9f3959>`_:   Merge branch 'vitodb-pylint' into 1.6

`c8eddda <https://github.com/HEPCloud/decisionengine/commit/c8edddafa05aa18b7ec931b79c5701ba8904543e>`_:   Merge branch 'pylint' of https://github.com/vitodb/decisionengine into vitodb-pylint Meerging PR#317 to release branch 1.6

`d7c43b9 <https://github.com/HEPCloud/decisionengine/commit/d7c43b961dbc4f092fdd39a73277be5d73dc9c2c>`_:   Use regular expression to support fail_on_error feature.

`ada6692 <https://github.com/HEPCloud/decisionengine/commit/ada6692533280d4171804ae2cc26f5337d721f0f>`_:   add support to run pylint tests

`efb1e57 <https://github.com/HEPCloud/decisionengine/commit/efb1e57bfdb7c03420440d34ad679eb5da618bc4>`_:   Finish migration to pure setuptools

`e4dc35e <https://github.com/HEPCloud/decisionengine/commit/e4dc35e36f75b14c71e0626afc7e1376adbac3df>`_:   Merge pull request #314 from jcpunk/jsonnet_syntax

`87e32c2 <https://github.com/HEPCloud/decisionengine/commit/87e32c228376bbe5a3cf513ac2890b2a8b7b793b>`_:   Merge pull request #294 from jcpunk/move-reaper

`dec85d5 <https://github.com/HEPCloud/decisionengine/commit/dec85d5ebb7cf9b8fb19c73ac5a68e9855503dba>`_:   Merge pull request #319 from jcpunk/task-loop

`4108472 <https://github.com/HEPCloud/decisionengine/commit/4108472afc04def8c35f7aaa569fd76568cf162f>`_:   Merge pull request #320 from jcpunk/container-swig

`920af1c <https://github.com/HEPCloud/decisionengine/commit/920af1c985f84896d92a1f5fe28ee8072d654247>`_:   Merge pull request #321 from knoepfel/include-init-files

`650dffa <https://github.com/HEPCloud/decisionengine/commit/650dffa70ea4bcca0022adb79823d53d81849d70>`_:   Don't forget __init__.py files.

`1b412e0 <https://github.com/HEPCloud/decisionengine/commit/1b412e03067216451d0552f434277d6069300ae3>`_:   The latest m2crypto seems to need swig now

`a6e3ab1 <https://github.com/HEPCloud/decisionengine/commit/a6e3ab1c283e5ec596cde771db9fd3fc6d97125d>`_:   Merge pull request #313 from jcpunk/conf-test

`1205636 <https://github.com/HEPCloud/decisionengine/commit/1205636a69763ef71d1baa273c92d0dbc51e46db>`_:   Simplify run loop

`de553a7 <https://github.com/HEPCloud/decisionengine/commit/de553a7e1f199f553db452b2a5d9ab9e21796286>`_:   fix test_client_with_no_server_verbose unit test for Jenkins CI (#315)

`30e59dc <https://github.com/HEPCloud/decisionengine/commit/30e59dc967285d13221dfee7b807f446f9fbfac2>`_:   fix test_client_with_no_server_verbose unit test for Jenkins CI (#315)

`10384a8 <https://github.com/HEPCloud/decisionengine/commit/10384a8cf3167bbadc0bfea08291c9eeb20cb01c>`_:   Move reaper into its own place and reuse state logic

`250c14b <https://github.com/HEPCloud/decisionengine/commit/250c14b151ba273417c09306556e591e9981d768>`_:   The `_validate` function doesn't permit missing 'PRODUCES'

`5ae1ce9 <https://github.com/HEPCloud/decisionengine/commit/5ae1ce9fc748a146777dd8f5bd63a96a7bc09fac>`_:   Make sure syntax error in config names the problem

`b899fa2 <https://github.com/HEPCloud/decisionengine/commit/b899fa237d20f949f1adf147fa7d6da55381b4b2>`_:   Add SourceProxy module test. (#307)

`7b3df14 <https://github.com/HEPCloud/decisionengine/commit/7b3df14c7a26c9d3ba2b0e56ac4598ed8d3c4d80>`_:   Increase coverage of utils (#304)

`ddba2a3 <https://github.com/HEPCloud/decisionengine/commit/ddba2a312884208b80682c7ecf3162234cf434e7>`_:   Fix duplicate entry warning (#311)

`915673f <https://github.com/HEPCloud/decisionengine/commit/915673fac5b37ccce0804fb2c2df969a92726f6b>`_:   Test modules minimally (#298)

`bc0c21a <https://github.com/HEPCloud/decisionengine/commit/bc0c21a924e097bfda51769228c787f69ae474e6>`_:   Some repos may error out, don't let them kill the build (#297)

`924a704 <https://github.com/HEPCloud/decisionengine/commit/924a7047a31d2fe69de04f5c97ef89eefc600fa3>`_:   doc: add 1.6.1 release notes

`b1ab4d3 <https://github.com/HEPCloud/decisionengine/commit/b1ab4d31d3b935929b39c553dd71135732bb9922>`_:   doc: fix typo

`85e5d71 <https://github.com/HEPCloud/decisionengine/commit/85e5d71454c018c84e30a81edd256f24c23e9fd9>`_:   postgresql: do not print stack trace for low level library (#309)

`255c641 <https://github.com/HEPCloud/decisionengine/commit/255c641505fce253ac3c854cbda3287e15e0524b>`_:   Setuptools uses entry return value as an error msg (#303)

`2fd8db4 <https://github.com/HEPCloud/decisionengine/commit/2fd8db454e1329b72eac292df9176c2a4c820261>`_:   Fix name to match expectations (#305)

`9cddb70 <https://github.com/HEPCloud/decisionengine/commit/9cddb70a5a6d74553868b8940139db00d59f2429>`_:   updated release notes

`7fe0358 <https://github.com/HEPCloud/decisionengine/commit/7fe0358eedae19e2bb0d33a5fa6a908a17424e28>`_:   Error in more clean methods (#300)

`84aa506 <https://github.com/HEPCloud/decisionengine/commit/84aa506cfa8d3838a30039eb7d47b62f64d23db9>`_:   Fix a bug in setup.py parsing of requirements. (#301)

`a58b61b <https://github.com/HEPCloud/decisionengine/commit/a58b61bb421e41404532e9182ab3f28da8a77837>`_:   fix typo in release notes

`33660bf <https://github.com/HEPCloud/decisionengine/commit/33660bf3a3d3740611d8fb469ba7025a6cd552cf>`_:   fixed a typo[locuser@fermicloud462 decisionengine]


Release 1.6.1
-------------

Patch level (bug fix) release.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `306 <https://github.com/HEPCloud/decisionengine/issues/306>`_ : /etc/decisionengine/decision_engine.conf as shipped in RPM is wrong format (`de0aef3 <https://github.com/HEPCloud/decisionengine/commit/de0aef35e73de120f4e869091a630a14f4c11be1>`_)
- `275 <https://github.com/HEPCloud/decisionengine/issues/275>`_ : Running de-client --stop-channel <channel> results in KeyError (`59fb44e <https://github.com/HEPCloud/decisionengine/commit/59fb44e793d8a66d079e63079c5a4b8032446df0>`_)

Full list of commits since version 1.6.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`d7ccd8a <https://github.com/HEPCloud/decisionengine/commit/d7ccd8a723bc537bf2378526a722f53baed2702f>`_
:   doc: fix typo

`ac48e50 <https://github.com/HEPCloud/decisionengine/commit/ac48e50ca1d6a286cc8327cb49d896be9c1e9303>`_
:   updated release notes

`de0aef3 <https://github.com/HEPCloud/decisionengine/commit/de0aef35e73de120f4e869091a630a14f4c11be1>`_
:   Fix name to match expectations (#305)

`59fb44e <https://github.com/HEPCloud/decisionengine/commit/59fb44e793d8a66d079e63079c5a4b8032446df0>`_
:   postgresql: do not print stack trace for low level library (#309) (#310)

`2162bbe <https://github.com/HEPCloud/decisionengine/commit/2162bbe356fad51263224f1ce0bcfa8fb2ac6f24>`_
:   Setuptools uses entry return value as an error msg (#308)

`b0fd9fb <https://github.com/HEPCloud/decisionengine/commit/b0fd9fbc1533d4ef4736c77e52ac42e104ea1ece>`_
:   1.6.0 package backports (#302)


Release 1.6.0
-------------

In this release:

* The logic engine has been rewritten in pure python. This removes the last C++ dependency the decision engine had. The build system has been updated accordingly.
* Migrated to setuptools package development library. This build system is the standard vanilla python build system provided with the python distribution. Build configurations have been updated and rpm packaging remains the primary distribution method.
* Completed logging implementation.
* Improvements in error handling and code coverage.
* Improvements in Jenkins and GitHub actions CI/CD pipelines.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `44 <https://github.com/HEPCloud/decisionengine/issues/44>`_ : Logic Engine doesn't handle missing values gracefully (`743effc <https://github.com/HEPCloud/decisionengine/commit/743effcb1cee09ea73c0f3f48166882d533dfcbb>`_)

- `253 <https://github.com/HEPCloud/decisionengine/issues/253>`_ : Decision engine can sometimes start up at boot time before network name resolution is working (`ae04db5 <https://github.com/HEPCloud/decisionengine/commit/ae04db544599c6777d63cb315ddac169e586809d>`_)


Full list of commits since version 1.5.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`2551e07 <https://github.com/HEPCloud/decisionengine/commit/2551e071a0a02c3683d26452e4d6f2964b783e09>`_
:   More coverage for de-client (#296)

`dde3945 <https://github.com/HEPCloud/decisionengine/commit/dde39450441fde230d1a231b63a1051e8b9ecebd>`_
:   Make sure actions either complete in time or die (#295)

`381861c <https://github.com/HEPCloud/decisionengine/commit/381861cb9e20adb9fadae0c24cee813839a5e432>`_
:   Update Jenkins pipeline configuration (#292)

`eb771f4 <https://github.com/HEPCloud/decisionengine/commit/eb771f43c3cda641297c8f4d41357038f070df9d>`_
:   Try to cleanup Dockerfile PATH issue (#291)

`780cb56 <https://github.com/HEPCloud/decisionengine/commit/780cb5688436802fdf2c52221e0a454358412e9b>`_
:   fix unittest doc

`8680942 <https://github.com/HEPCloud/decisionengine/commit/8680942a796d6c29fdc3b30c97cfcc892ab776d3>`_
:   update unittest documentation

`8154b24 <https://github.com/HEPCloud/decisionengine/commit/8154b2439ea7c68324e9720dc4663d5525febd15>`_
:   Fixup sphinx doc (#290)

`5f7e13a <https://github.com/HEPCloud/decisionengine/commit/5f7e13ae53b832c7fad67b994cf50333c56f0952>`_
:   enhancements in logging and error handling in dataspace dir (#283)

`3d92725 <https://github.com/HEPCloud/decisionengine/commit/3d92725049308dbff9767db49bb9e10f5342d29c>`_
:   Add missing runtime requirement (#286)

`743effc <https://github.com/HEPCloud/decisionengine/commit/743effcb1cee09ea73c0f3f48166882d533dfcbb>`_
:   Allow conversion from errors to false values in logic-engine expressions. (#284)

`124dcab <https://github.com/HEPCloud/decisionengine/commit/124dcab90b697b9b1d95ec0ac1a5bb8d455794f9>`_
:   Inherit version from setuptools_scm if possible (#287)

`3669803 <https://github.com/HEPCloud/decisionengine/commit/366980358d74c43e0e8fde93bab0d02ebbe658aa>`_
:   added missing "\" as line continuation

`761f1d9 <https://github.com/HEPCloud/decisionengine/commit/761f1d936b5a6cefcc2da81139bb64451303b160>`_
:   Drop invalid **init**.py

`dc0e71b <https://github.com/HEPCloud/decisionengine/commit/dc0e71b68aae6365219d349c61e30d71b9abf895>`_
:   migrate to setuptools (#264)

`3b6f1bf <https://github.com/HEPCloud/decisionengine/commit/3b6f1bf8e0851c4e03e223ea26ef334146ce7b3a>`_
:   Make reaper reset state when starting from stopped proc (#280)

`b2f9061 <https://github.com/HEPCloud/decisionengine/commit/b2f9061a6c7b853e4f47f675162532745a8926a6>`_
:   added ISO-8601 format to time in logging. changed name of function for better clarity. (#279)

`0a74fe1 <https://github.com/HEPCloud/decisionengine/commit/0a74fe1286bf7f1905f874aac8a73615418b2d8a>`_
:   Improved DE client usage (#281)

`ebf53e3 <https://github.com/HEPCloud/decisionengine/commit/ebf53e3efdffdf56b1e2029629cc74eca81614fb>`_
:   Added shutdown method to Publisher class (#278)

`f95ab6d <https://github.com/HEPCloud/decisionengine/commit/f95ab6da25aceca93215e460e0cd2db84468617c>`_
:   Address some flake8/black reports (#274)

`1c383b7 <https://github.com/HEPCloud/decisionengine/commit/1c383b7f09147d5086aeb6edc447f1a2ef95efb1>`_
:   Automatically pull in our settings from about.py (#273)

`e71f186 <https://github.com/HEPCloud/decisionengine/commit/e71f186e4a78c743778240af3661c6cff7c9c305>`_
:    logging and error handling enhancements to taskmanager directory (#277)

`7de9ab9 <https://github.com/HEPCloud/decisionengine/commit/7de9ab9ac6739762f80329f19607d3c007dc6e49>`_
:   Increase Reaper log verbosity (#267)

`019d245 <https://github.com/HEPCloud/decisionengine/commit/019d24574b0a4528cb903a861aee5da0a1b6d20a>`_
:   Update actions to follow new best practices (#272)

`b84e847 <https://github.com/HEPCloud/decisionengine/commit/b84e847685a622a91ab2a681698a5e343055ba99>`_
:   Avoid possible sync issues in reaper startup (#271)

`891975f <https://github.com/HEPCloud/decisionengine/commit/891975fd4785bfb72fe9ff47f6ef93356eddf0ec>`_
:   Remove vestigial C++ files. (#270)

`42e5e1f <https://github.com/HEPCloud/decisionengine/commit/42e5e1fc74fdf11cc3b80bdc1d98ac35f9d4de76>`_
:   enhancements in logging and exception handling in newly added logicengine files (#265)

`38effe6 <https://github.com/HEPCloud/decisionengine/commit/38effe62dfe891ddd7488dfc2b6708b3c07c8126>`_
:   Ensure the scheduler has started the thread before returning (#269)

`db54fa1 <https://github.com/HEPCloud/decisionengine/commit/db54fa1bd628b18c9e7880561fbf23672cf3b968>`_
:   Start testing on PyPy with psycopg2cffi (#223)

`cc44058 <https://github.com/HEPCloud/decisionengine/commit/cc44058d715e60dab1223b653a5414e7a8e4964d>`_
:   Squashed commit of the following: (#263)

`d6548e9 <https://github.com/HEPCloud/decisionengine/commit/d6548e9dfb566386ffa65c2f149f662989b19d36>`_
:   Enhanced logging in the logicengine directory files (#261)

`c341bf7 <https://github.com/HEPCloud/decisionengine/commit/c341bf7a3d62462fa0778c30e2cf3aa2fd5ecf02>`_
:   Better match our workflow with codecov (#260)

`1fbe44d <https://github.com/HEPCloud/decisionengine/commit/1fbe44d8fa4adda988a1492a5bff161dd45589d0>`_
:   Use 'new' syntax for forward compat (#259)

`2294b0b <https://github.com/HEPCloud/decisionengine/commit/2294b0bd049f7a99d10a6ce72a22c36fa6d26673>`_
:   Do a limited pin on version requirements (#256)

`bcda470 <https://github.com/HEPCloud/decisionengine/commit/bcda4704d5c7cd79a50e97a4651c4e19e4f1e802>`_
:   Python implementation of logic engine (#246)

`c6721b4 <https://github.com/HEPCloud/decisionengine/commit/c6721b46c7b4b37a409d6422cbf90d91751a5e9a>`_
:   address comment on RB

`ae04db5 <https://github.com/HEPCloud/decisionengine/commit/ae04db544599c6777d63cb315ddac169e586809d>`_
:   Add Wants and After (network-online.target) dependency

`1a96b14 <https://github.com/HEPCloud/decisionengine/commit/1a96b14b21f910e6d335080af635eb46dd623833>`_
:   Fix action repodata

`a70cee8 <https://github.com/HEPCloud/decisionengine/commit/a70cee82c0e837e5ce931b37a5a1d74cbba346b5>`_
:   Move to CodeCov.io

`7b16b4e <https://github.com/HEPCloud/decisionengine/commit/7b16b4e6efc1b4ed3913972c30ede47719d26706>`_
:   Add Wants and Requires dependencies (#258)

`76c3670 <https://github.com/HEPCloud/decisionengine/commit/76c367045f8c0bfae99108790232ac5c25ef8ae1>`_
:   Move to CodeCov.io (#254)

`e7ba013 <https://github.com/HEPCloud/decisionengine/commit/e7ba0130a710d7c79512afb7fabb414bca54a6e9>`_
:   Fix action repodata (#255)

`d7e72f2 <https://github.com/HEPCloud/decisionengine/commit/d7e72f2642235d965d0267622015120a0e30ff3f>`_
:   revert 3.9 test

`b04154b <https://github.com/HEPCloud/decisionengine/commit/b04154b0c960dde3241739b9c33b36dd969460f8>`_
:   added 1.5.0 release notes

`a03da29 <https://github.com/HEPCloud/decisionengine/commit/a03da29ee1373c7ec3697781875b9a7d283594ac>`_
:   remove 3.9 to see if documentatoin gets generated
