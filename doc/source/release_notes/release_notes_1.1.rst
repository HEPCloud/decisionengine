.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.1.0
-------------

In this release:


* Fixed. https://github.com/HEPCloud/decisionengine_modules/issues/108 "Supply Postgres script to delete fields in main database before a certain date"
* significant code cleanup and pep8 compliance
* unit test work
* CI (GitHub actions and Travis) is introduced

commits

`f894b1d <https://github.com/HEPCloud/decisionengine/commit/f894b1d13acc9d5ba3759c5c5ba1533b09253b16>`_
:   Skip unittest (#77)

`632e64b <https://github.com/HEPCloud/decisionengine/commit/632e64b898cafd0db95fb0c7eecd31595ef19b2d>`_
:   Add ipython

`f681a79 <https://github.com/HEPCloud/decisionengine/commit/f681a7957154114dae5ca551635a4fddb46437de>`_
:   Make python 2.7 tests run on 1.1 branch

`d6a32c0 <https://github.com/HEPCloud/decisionengine/commit/d6a32c0ee35e1172cb3741a330f90590f4af28b5>`_
:   implementation of data reaper (#75)

`2ad8614 <https://github.com/HEPCloud/decisionengine/commit/2ad861452220e38ad9bf9e446a5087b73ed37a9d>`_
:   Use sparse checkout for first checkout to get .github/actions (#65)

`812f032 <https://github.com/HEPCloud/decisionengine/commit/812f03248d9b5fbc7fe079dc250b5ad25585a824>`_
:       Cat output of pytest log     Exit pylint entrypoint with the line count of pep8 and pylint logs     Deal with (detach from ...)     Only tar up (S)RPMS dirs for rpm build.

`6b05ec7 <https://github.com/HEPCloud/decisionengine/commit/6b05ec74c1e265bcd42d72317a7e604e46992eba>`_
:   Fix errors reported by run_pylint (#62)

`d9f5b66 <https://github.com/HEPCloud/decisionengine/commit/d9f5b6624de7e6be04a1bcfaebb4d005d8e197c3>`_
:   Setup pep8speaks

`c3b8ac2 <https://github.com/HEPCloud/decisionengine/commit/c3b8ac2054d673c13ed3230529f3905d6ec0d288>`_
:   Run github actions as non-root uid. Install packages in virtualenv and remove system rpms.

`ae01f9e <https://github.com/HEPCloud/decisionengine/commit/ae01f9ec18adfeb913fc37b3923815605b00d4d5>`_
:   Support Python 3 for Boost Python

`579761c <https://github.com/HEPCloud/decisionengine/commit/579761c898537837e2ee9152409b5c8235720b64>`_
:   Support Python 3 for Boost Python

`044b979 <https://github.com/HEPCloud/decisionengine/commit/044b979297ce0e02062a366f98d5af0731f06899>`_
:   Remove unnecessary using declarations.

`00f6d00 <https://github.com/HEPCloud/decisionengine/commit/00f6d00b1c22d02377d97960f6ccf4a47f6e3b2f>`_
:   Add extra header dependency due to Boost Python omission.

`24e0795 <https://github.com/HEPCloud/decisionengine/commit/24e0795c349fddc3276b66c535dffc6d5f97efda>`_
:   Apply clang-format

`17c17f9 <https://github.com/HEPCloud/decisionengine/commit/17c17f9bec0a4a2402362424268514ef07d33e79>`_
:   Remove JSON dependency.

`faa0b22 <https://github.com/HEPCloud/decisionengine/commit/faa0b22f1ff193dd0e111d72ed3b890e2bf9ac54>`_
:   Massive cleanup.

`07b555f <https://github.com/HEPCloud/decisionengine/commit/07b555f195f6ba6c2a5c77906807c066f64df6be>`_
:   Updates to Github Actions to allow building with python3.6

`fef6c11 <https://github.com/HEPCloud/decisionengine/commit/fef6c11ed26612482d4b84484a8a9e299a8654b6>`_
:   Fix errors when running pylint.sh multiple times

`da6f077 <https://github.com/HEPCloud/decisionengine/commit/da6f0774ba765e453ab54fd533c62798f0e96fe1>`_
:   Autopep8 -i fixes

`39fe5b3 <https://github.com/HEPCloud/decisionengine/commit/39fe5b33ea41295752d931e7772d453ac69b4a3f>`_
:   TaskManager: fix calling log_exception with correct number of arguments and minor format changes to reduce PEP8 warnings

`17396da <https://github.com/HEPCloud/decisionengine/commit/17396da81cce534c9f17af5c211649fb733a45de>`_
:   logicengine: get rid of compiler warnings

`01dc3d1 <https://github.com/HEPCloud/decisionengine/commit/01dc3d1352065f8986832d03fee6595e362c5056>`_
:   Only track what we need

`b609d73 <https://github.com/HEPCloud/decisionengine/commit/b609d7361fb745cc2c399f20cfc2c8504e89b9d3>`_
:   Configure coveralls (and some minor cleanup)

`bd9ed5e <https://github.com/HEPCloud/decisionengine/commit/bd9ed5edd0d25830b697be737f15e7f2358796dd>`_
:   Many C++ cleanups

`2a61876 <https://github.com/HEPCloud/decisionengine/commit/2a61876cdef98fed5b7d8f851dfa26258da176d2>`_
:   Add Badges

`c864f27 <https://github.com/HEPCloud/decisionengine/commit/c864f27fda4ba73b851b5231cfa5d7f36f999f72>`_
:   Do not call pytest fixtures directly.

`307db5f <https://github.com/HEPCloud/decisionengine/commit/307db5f6ee45c93d4126429514ad90cb74376a8f>`_
:   white space fix

`882b58f <https://github.com/HEPCloud/decisionengine/commit/882b58fb3033f6bce31d594d486ae93859084461>`_
:   fix unit tests

`1da687c <https://github.com/HEPCloud/decisionengine/commit/1da687c3a391862a114c9ef54ad9dffeed7c4f9c>`_
:   Replace Boost facilities with C++ STL ones.

`5a6e6b1 <https://github.com/HEPCloud/decisionengine/commit/5a6e6b11d02a102f0b2d7ce03b8d1a5bf3fb4fc3>`_
:   Run tests on push

`8404245 <https://github.com/HEPCloud/decisionengine/commit/8404245d95e8554366579378057787b3466b05de>`_
:   Add missing Boost regex library dependency.

`ceb5fe7 <https://github.com/HEPCloud/decisionengine/commit/ceb5fe7ad9c117ea251014d513fedd4b78e7d58a>`_
:   Apply clang-format to files that were missed earlier.

`3de9940 <https://github.com/HEPCloud/decisionengine/commit/3de99403d2416d5b0eaaeb943dbc0552da468bc2>`_
:   Apply clang-format to C++ code.

`8a8f560 <https://github.com/HEPCloud/decisionengine/commit/8a8f560b07805600e55cf01a38d9e4520e9034bb>`_
:   Cache venv directory instead

`ad017ce <https://github.com/HEPCloud/decisionengine/commit/ad017ce5eb27277b2fd20609d77687b200f74956>`_
:   Build private boost for testing

`928c64a <https://github.com/HEPCloud/decisionengine/commit/928c64a1a5a0605390351a2e2eafd8366fb76620>`_
:   Test pip cache

`358939a <https://github.com/HEPCloud/decisionengine/commit/358939ad3551a94392871c25584f09329de848e6>`_
:   Adjust CMakeLists.txt files to use correct Python versions

`9f0ddb3 <https://github.com/HEPCloud/decisionengine/commit/9f0ddb37b05cc2147aa5244242f344dbd3ca44d8>`_
:           Add pylint github action.

`5e6ce4a <https://github.com/HEPCloud/decisionengine/commit/5e6ce4aa6a3713dcf64fd055148815de347c0bde>`_
:   Remove more unused C++ files.

`63717fe <https://github.com/HEPCloud/decisionengine/commit/63717fe17f1519791d720907b7492efcce67b50c>`_
:   Setup travis to use new cmake var

`74fab2a <https://github.com/HEPCloud/decisionengine/commit/74fab2ae8c779b8dc252de880674de55e39cfff8>`_
:   Use cmake argument -DPYVER=3.6 to build python3 library https://fermicloud140.fnal.gov/reviews/r/31/

`843f30c <https://github.com/HEPCloud/decisionengine/commit/843f30cccc35a5bf73af4a3a460bf33a2820ada6>`_
:   Minor cleanups per travis-lint

`a538cac <https://github.com/HEPCloud/decisionengine/commit/a538cac4b8202d0c2e861e082e23e72f41d4f2a5>`_
:   Remove unused C++ files.

`4c9d125 <https://github.com/HEPCloud/decisionengine/commit/4c9d12549cff4e5f5545d505668a4c23bd218dfe>`_
:   Update repo where action is taken from

`87fb2d9 <https://github.com/HEPCloud/decisionengine/commit/87fb2d91b8afef4d9096e0dd3721e432c44b365a>`_
:   Update rpms installed in docker image. Update entrypoint.sh to use cmake3.

`199ee87 <https://github.com/HEPCloud/decisionengine/commit/199ee875b98ec21f565fbcbef21364d5849323f2>`_
:   Find python3 libraries using cmake3 from epel rpm Also need to install python3-devel

`4c79d2c <https://github.com/HEPCloud/decisionengine/commit/4c79d2c4ade0341457556166b591312c5211d46b>`_
:   Remove unused GNUmakefiles.

`94342ee <https://github.com/HEPCloud/decisionengine/commit/94342eea07ee2219bc17280b2a3fc2a60e08ea8a>`_
:   Add unit test as a Github Action

`1a0e102 <https://github.com/HEPCloud/decisionengine/commit/1a0e1029e19a51ccce38099702ee8fe8ba09c860>`_
:   more advanced travis.yml

`0be413f <https://github.com/HEPCloud/decisionengine/commit/0be413f14994d14c1631eedb5d644280e26976f9>`_
:   Add helper file for pip

`7794327 <https://github.com/HEPCloud/decisionengine/commit/77943276d9f971b9ba9c023d51088286b9ec0249>`_
:   Make recursive import happy

`7005c78 <https://github.com/HEPCloud/decisionengine/commit/7005c78a94aa9c14051b0a5bdcf2eb43e87b1736>`_
:   Add simple target

`de8b0fa <https://github.com/HEPCloud/decisionengine/commit/de8b0fa8a345d2c3bb73a906d651cb58814688aa>`_
:   python3 compliance: replace string.join() where appropriate, handle UserDict

`2662e6c <https://github.com/HEPCloud/decisionengine/commit/2662e6c7dec784f99cb49c2446cac87db1aece8f>`_
:   note required packages

`3b87119 <https://github.com/HEPCloud/decisionengine/commit/3b87119455b6e206b93ff4c4ffdc3a330c22a8ca>`_
:   Add missing header includes.

`3e79b84 <https://github.com/HEPCloud/decisionengine/commit/3e79b84afce941627159ae44e33c4e2f2848c474>`_
:   Remove defunct code and its tests

`b1dbe1a <https://github.com/HEPCloud/decisionengine/commit/b1dbe1a03aa795a2518a9454aeef7f13a9cc38fb>`_
:   Ensure attribs are defined at **init**

`c4ad78a <https://github.com/HEPCloud/decisionengine/commit/c4ad78af75d650ae7e58646ad33ae22e80257e1d>`_
:   Correct logger arguments do avoid duplicate string parse

`a8dcc67 <https://github.com/HEPCloud/decisionengine/commit/a8dcc679b375da05073f115004771ed3614c8f6a>`_
:   Remove unused imports (per pylint)

`d3502b5 <https://github.com/HEPCloud/decisionengine/commit/d3502b5e61fbb013d329845b2c3e5c1baee24594>`_
:   Remove obsolete CVS directories.

`d744111 <https://github.com/HEPCloud/decisionengine/commit/d744111e98a7c9d6afc665fdc7a463906fa1bb15>`_
:   add six module to the list of required modules

`0a9b1e8 <https://github.com/HEPCloud/decisionengine/commit/0a9b1e8d18f3c51ca7bb11542e3d1e61aa77b6bc>`_
:   Fix class declaration

`b83157e <https://github.com/HEPCloud/decisionengine/commit/b83157ea62b8780fa3febedc1570ad7e5484a269>`_
:   Handle metaclasses

`549f33b <https://github.com/HEPCloud/decisionengine/commit/549f33bf8c29ecfd43412a80b66889d8ae40e8bb>`_
:   Add config for Travis CI

`ee71044 <https://github.com/HEPCloud/decisionengine/commit/ee71044acc50848eb0b021f976336bd11a0f25a1>`_
:   Drop trailing white space

`3f82af6 <https://github.com/HEPCloud/decisionengine/commit/3f82af6ff7d9862b2b5e42cd6f0cd57df8d67604>`_
:   Python3 forward compatible syntax

`28bf291 <https://github.com/HEPCloud/decisionengine/commit/28bf291877537d5f819dfca6bd6be97b7536576f>`_
:   Add safe (for python 2.7) python3 compatible syntax

`1d1d76f <https://github.com/HEPCloud/decisionengine/commit/1d1d76fd0b7a1bf485e959439d9cb2723835049e>`_
:   prepare for python3
