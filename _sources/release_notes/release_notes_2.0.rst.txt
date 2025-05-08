.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 2.0.6
-------------

This improves separation and compatibility with the GlideinWMS Frontend package.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enhancements:

- `DE 721 <https://github.com/HEPCloud/decisionengine/pull/721>`_: Update Dockerfile and entrypoint to be able to build RPMs and wheels on Jenkins (@vitodb)
- `DE 720 <https://github.com/HEPCloud/decisionengine/pull/720>`_: Added option to prepare for OSG release to make_release (@mambelli)
- `DE 719 <https://github.com/HEPCloud/decisionengine/pull/719>`_: Update CI related Dockerfile and Jenkins pipeline (@vitodb)
- `DE 718 <https://github.com/HEPCloud/decisionengine/pull/718>`_: Release 2.0.4  (@mambelli)



Full list of commits since version 2.0.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


`3b183afb2 <https://github.com/HEPCloud/decisionengine/commit/3b183afb2e2c7e14ffd7992c4deb95413bcf94f8>`_:   Added glidein group to coordinate with GWMS Frontend installation

`765f66059 <https://github.com/HEPCloud/decisionengine/commit/765f660599625b5d491c9379f26cabdc5d71b551>`_:   Update EL9/python3-entrypoint.sh to use python venv from framework container. Add the option to call make-release script to build RPMs and wheels. Update Jenkinsfile_EL9 to fit these updates.

`13d03d7df <https://github.com/HEPCloud/decisionengine/commit/13d03d7dfac59a988b8ae40a1507df17d6bdaad6>`_:   Update EL9/framework/Dockerfile container to use a python venv to handle python modules

`dc4c2cbbd <https://github.com/HEPCloud/decisionengine/commit/dc4c2cbbdb05aad787f209577ada18bf7b352104>`_:   Added option to prepare for OSG release (make specfile, checksummed source tar ball and upload to OSG library)

`c24b74ed5 <https://github.com/HEPCloud/decisionengine/commit/c24b74ed540e67411fb64e56f46cf8631cef1542>`_:   Merge pull request #719 from vitodb/feature/vito_update_ci_build

`b4951eeea <https://github.com/HEPCloud/decisionengine/commit/b4951eeea07a8e0ec735e4f0274f5df31d26acf7>`_:   In Jenkinsfile_EL9 pipeline replace rpmbuild stage with DEbuild and use make-release.sh script to build DE/DEM RPMs/wheels

`ac9e23823 <https://github.com/HEPCloud/decisionengine/commit/ac9e2382324e476ec548c588e4c227804b6c45d1>`_:   In Dockerfile add dependencies and requirements to use mock

`3f4fa209b <https://github.com/HEPCloud/decisionengine/commit/3f4fa209bdd4ae14f12cf987f2e7f8ba27a300f6>`_:   Fixed release notes and typo in make-release.sh

`4add02381 <https://github.com/HEPCloud/decisionengine/commit/4add023813b6a1d354a55bfc24450be5a7097a6f>`_:   Remove use of build, not installed

`f48a31839 <https://github.com/HEPCloud/decisionengine/commit/f48a31839d1388dfe5cf742d9572971578c77aa2>`_:   Install sphinx as user, not as root

`ce1f28584 <https://github.com/HEPCloud/decisionengine/commit/ce1f28584320bd10c6d264703885bfbec6f921c2>`_:   Updated actions in gh-pages workflow


Release 2.0.4
-------------

This release brings a new packaging with RPM packages for dependencies and system files, and a Python wheel for the Python code.
There are also new Prometheus metrics and a few bug fixes like the source logging set incorrectly.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugs fixed:

- `DE 670 <https://github.com/HEPCloud/decisionengine/pull/670>`_: changes to fix source logging  (@goodenou)
- `DE 674 <https://github.com/HEPCloud/decisionengine/pull/674>`_: Upgrading isort version to fix pre-config install error w/ poetry  (@mambelli)
- `DE 683 <https://github.com/HEPCloud/decisionengine/pull/683>`_: Fix unit tests  (@vitodb)
- `DE 696 <https://github.com/HEPCloud/decisionengine/pull/696>`_: Re-enable flake8 linter  (@vitodb)
- `DE 701 <https://github.com/HEPCloud/decisionengine/pull/701>`_: Fixed bugs in metrics with labels  (@IlyaBaburashvili)
- `DE 700 <https://github.com/HEPCloud/decisionengine/pull/700>`_: For flake8 skip build folder  (@vitodb)
- `DE 713 <https://github.com/HEPCloud/decisionengine/pull/713>`_: Set /metrics Content-type header to text/plain  (@shreyb)
- `DE 710 <https://github.com/HEPCloud/decisionengine/pull/710>`_: add invocation in the child processes for sources/channels logging  (@namrathaurs)

Enhancements:

- `DE 668 <https://github.com/HEPCloud/decisionengine/pull/668>`_: Introduce publisher status data product  (@knoepfel)
- `DE 671 <https://github.com/HEPCloud/decisionengine/pull/671>`_: explicitly select a container with all our required python versions  (@jcpunk)
- `DE 676 <https://github.com/HEPCloud/decisionengine/pull/676>`_: Added EL9 instructions  (@mambelli)
- `DE 678 <https://github.com/HEPCloud/decisionengine/pull/678>`_: Updated and tested instructions, PIP installation working  (@mambelli)
- `DE 679 <https://github.com/HEPCloud/decisionengine/pull/679>`_: Disabling unit tests for python 3.6  (@vitodb)
- `DE 680 <https://github.com/HEPCloud/decisionengine/pull/680>`_: Make default database init use stronger data protections  (@jcpunk)
- `DE 681 <https://github.com/HEPCloud/decisionengine/pull/681>`_: Update to pytest 7 with pytest-postgresql 5  (@jcpunk)
- `DE 682 <https://github.com/HEPCloud/decisionengine/pull/682>`_: Updated EL9 instruction: PIP installation and GWMS config tested  (@mambelli)
- `DE 685 <https://github.com/HEPCloud/decisionengine/pull/685>`_: Enable some tests only on DE 1.7 branch  (@vitodb)
- `DE 687 <https://github.com/HEPCloud/decisionengine/pull/687>`_: Update GH actions  (@vitodb)
- `DE 688 <https://github.com/HEPCloud/decisionengine/pull/688>`_: Added two metrics on the Source - de_source_status and de_source_acquire_seconds  (@skylerfoster67)
- `DE 690 <https://github.com/HEPCloud/decisionengine/pull/690>`_: Adding DE EL9 containers based on AlmaLinux9  (@vitodb)
- `DE 691 <https://github.com/HEPCloud/decisionengine/pull/691>`_: Adding Jenkinsfile for EL9  (@vitodb)
- `DE 689 <https://github.com/HEPCloud/decisionengine/pull/689>`_: Added new de-client metrics for duration  (@IlyaBaburashvili)
- `DE 694 <https://github.com/HEPCloud/decisionengine/pull/694>`_: Decision Engine Components Data  (@skylerfoster67)
- `DE 697 <https://github.com/HEPCloud/decisionengine/pull/697>`_: Redis Exporter Data  (@skylerfoster67)
- `DE 703 <https://github.com/HEPCloud/decisionengine/pull/703>`_: Create Redis mock for unit tests  (@shreyb)
- `DE 706 <https://github.com/HEPCloud/decisionengine/pull/706>`_: In Jenkins pipeline config use podman instead of docker  (@vitodb)
- `DE 712 <https://github.com/HEPCloud/decisionengine/pull/712>`_: Rpm pip packaging with uv and pyproject.toml  (@mambelli)
- `DE 714 <https://github.com/HEPCloud/decisionengine/pull/714>`_: Fixed spec file and added release script  (@mambelli)
- `DE 715 <https://github.com/HEPCloud/decisionengine/pull/715>`_: Added wrapper to run the decisionengine commands also as root. Fixed installation glitches.  (@mambelli)
- `DE 716 <https://github.com/HEPCloud/decisionengine/pull/716>`_: Added a check for the Python code being installed and improved Python code install  (@mambelli)
- `DE 717 <https://github.com/HEPCloud/decisionengine/pull/717>`_: Added codespell in pre-commit and fixed files to compliance  (@mambelli)

Full list of commits since version 2.0.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`34ae84f15 <https://github.com/HEPCloud/decisionengine/commit/34ae84f153cd54f6e3d68062a8b645b3877cfdb1>`_:   Added ability to build Python (wheel and sdist) packages to make-release.sh

`8192524ba <https://github.com/HEPCloud/decisionengine/commit/8192524ba4bb61b772746fc768765d3f2e0d7411>`_:   Added codespell in pre-commit and fixed files to compliance

`e045cb960 <https://github.com/HEPCloud/decisionengine/commit/e045cb960700095f29731b75a878d29110869cde>`_:   Added a check for the Python code being installed. Improved the Python install script, adding the ability to clone the repo

`7093d5b12 <https://github.com/HEPCloud/decisionengine/commit/7093d5b1271c09ffcf7045ce3a72f5f0b69f60af>`_:   Added wrapper to run the decisionengine commands also as root. Fixed installation glitches.

`59cd65825 <https://github.com/HEPCloud/decisionengine/commit/59cd65825654c7cc797916f8b930570b9f58c626>`_:   Fixed spec file and added release script

`8174106dd <https://github.com/HEPCloud/decisionengine/commit/8174106ddb08d5090b0391c82dfbdc280d855d87>`_:   Adding dependencies RPM package and packaging with uv and pyproject.toml

`22951dc58 <https://github.com/HEPCloud/decisionengine/commit/22951dc58cc1262ddd7da4ec46c105e8ab8f67a6>`_:   Set /metrics Content-type header to text/plain

`aea4fd7ad <https://github.com/HEPCloud/decisionengine/commit/aea4fd7ad436d347671f80ec8faa0522239a600f>`_:   logging fix for sources and channels

`30fb83dc5 <https://github.com/HEPCloud/decisionengine/commit/30fb83dc50b509f49b1c8b37659966e8a3c11698>`_:   In Jenkins pipeline config use podman instead of docker

`0aca4d926 <https://github.com/HEPCloud/decisionengine/commit/0aca4d926ec8c792bc2ff959269d7736d5e61f8e>`_:   Added .vscode/ to .gitignore

`489d45abf <https://github.com/HEPCloud/decisionengine/commit/489d45abf4e309c16309b01130cb0a27bf27fedc>`_:   Dynamically check for redis server availability when a test is marked as redis

`ff674229e <https://github.com/HEPCloud/decisionengine/commit/ff674229ebebaa42a2562427937ba56203797fbe>`_:   Remove unit test marker

`6b1799f1b <https://github.com/HEPCloud/decisionengine/commit/6b1799f1bbc482be01d0e6ae09deb5440c1e0e82>`_:   Check if redis server is running.  If not, skip integration test.  Also marked applicable unit tests in this file

`6879f72c5 <https://github.com/HEPCloud/decisionengine/commit/6879f72c5f4dd3456734a5f1a4b630408b30bff1>`_:   Added unit marker for pytest

`22488d720 <https://github.com/HEPCloud/decisionengine/commit/22488d7204bcf5ad238a787e6bc3fe67481fc51c>`_:   For flake8 skip build folder

`19a163a14 <https://github.com/HEPCloud/decisionengine/commit/19a163a1404d85457d3addeb2097d0829f5d09f4>`_:   Fixed bugs in metrics with labels (#701)

`0a38b170b <https://github.com/HEPCloud/decisionengine/commit/0a38b170be381b3a69e533bd6cb7cc360ae166a9>`_:   Update test to be compliant with flake8 linter

`22162226c <https://github.com/HEPCloud/decisionengine/commit/22162226c29b3a11225f2cb81c5b4c150343c041>`_:   Add licence info to flake8 config file

`1da6bd8df <https://github.com/HEPCloud/decisionengine/commit/1da6bd8dfa6d09b879e7af613ba67ba899aee29d>`_:   Re-enable flak8 linter

`65d5ccd9a <https://github.com/HEPCloud/decisionengine/commit/65d5ccd9aa20a5692e5e8a0410cfd730c82b703c>`_:   Dashboard on Redis Exporter information

`daaac113c <https://github.com/HEPCloud/decisionengine/commit/daaac113ca7a4051a72cc0c1356a8c866d38e56c>`_:   Added json files containing the dashboards for Source and Channel Data in decisionengine/dashboards

`d21728923 <https://github.com/HEPCloud/decisionengine/commit/d217289234b36f104376bf0ea6edcbfa5763ee36>`_:   Added license compliance for json files

`ba29da2af <https://github.com/HEPCloud/decisionengine/commit/ba29da2af5127842fc4d1d846d22c5b87ef48e03>`_:   [pre-commit.ci] auto fixes from pre-commit.com hooks

`d79908778 <https://github.com/HEPCloud/decisionengine/commit/d7990877896fa624b76331c57bd520f01e9527d4>`_:   Configure buckets for de-client metrics

`14826e839 <https://github.com/HEPCloud/decisionengine/commit/14826e8394aeccd9ebfa57b8917db52c3d539fb8>`_:   [pre-commit.ci] auto fixes from pre-commit.com hooks

`87457a1e0 <https://github.com/HEPCloud/decisionengine/commit/87457a1e0a3481440b64722b50f7e1805908e4e3>`_:   Fix de-client --metrics description

`2cc376a60 <https://github.com/HEPCloud/decisionengine/commit/2cc376a60a0809ab8ddac8989deb79f272047765>`_:   Added decorators for all rpc_ methods

`7fe99a642 <https://github.com/HEPCloud/decisionengine/commit/7fe99a64270c410ca7b0b1ad0bf12b41f4832db0>`_:   Added directory for Grafana dashboards

`a9d1590c3 <https://github.com/HEPCloud/decisionengine/commit/a9d1590c3b0ad71481fdd26e928f80d9419fc4bb>`_:   Adding Jenkinsfile for EL9

`018c8ab47 <https://github.com/HEPCloud/decisionengine/commit/018c8ab47bf8bb25e84bdc767b42ddaefdd0742f>`_:   Updated documentation for 1.7.5 release

`ebfd6d4a0 <https://github.com/HEPCloud/decisionengine/commit/ebfd6d4a0a9eafbe7324e41523656e75ba23287e>`_:   Numpy security update requires >= 1.22 (not available for Python 3.6)

`aa474a9d8 <https://github.com/HEPCloud/decisionengine/commit/aa474a9d8b16bd038ea95d9801727c5afe98052e>`_:   Fixed misspelling

`9e9088418 <https://github.com/HEPCloud/decisionengine/commit/9e908841827a1051439644e6c4fbb9a74eee56e5>`_:   Adding DE EL9 containers based on AlmaLinux9

`438621a0a <https://github.com/HEPCloud/decisionengine/commit/438621a0ae3a9d2da9f234e6a800e148ddda6a64>`_:   Added two metrics on the Source - de_source_status and de_source_acquire_seconds

`f54b92a59 <https://github.com/HEPCloud/decisionengine/commit/f54b92a5966b81aeb9aea25b61f26007b7ae32d7>`_:   Update GH actions

`f842996df <https://github.com/HEPCloud/decisionengine/commit/f842996df2fe5a49f4e51bf59630bcd11631f28c>`_:   enable rpmbuild_el7, run_flake8 and pytest_el7 tests only on DE branch 1.7

`97915e0be <https://github.com/HEPCloud/decisionengine/commit/97915e0be225cccd5affeec5a21ca769b12b0f3c>`_:   Note of possible future change

`1c23be195 <https://github.com/HEPCloud/decisionengine/commit/1c23be1951538f73fb8c1045892f5d9d1840e881>`_:   update regexp in _expected_circularity

`aa12938f9 <https://github.com/HEPCloud/decisionengine/commit/aa12938f984200545d7322730f650dd917672c20>`_:   Updated instruction after testing PIP installation and pressure-based condifuraition on EL9

`d302e74bf <https://github.com/HEPCloud/decisionengine/commit/d302e74bf98480578cad41f2877baf0a481f30e8>`_:   Update to pytest 7 with pytest-postgresql 5

`e9372585e <https://github.com/HEPCloud/decisionengine/commit/e9372585eae4feabc309f8085f56e93bbc9f1dba>`_:   Make default database init use stronger data protections

`aed2d7666 <https://github.com/HEPCloud/decisionengine/commit/aed2d7666c11ed070cc55169401e2020a937a3c6>`_:   Disabling unit tests for python 3.6

`87b3f6e92 <https://github.com/HEPCloud/decisionengine/commit/87b3f6e9280e06a4cb7afc7453929d647f95d6d4>`_:   Updated and tested instructions, PIP installation working

`84ebaa528 <https://github.com/HEPCloud/decisionengine/commit/84ebaa528bae3aae9aa31b07d2777f14dd0e3068>`_:   Fixed setup for EL9

`0053e5963 <https://github.com/HEPCloud/decisionengine/commit/0053e5963c7bbe1d4030aae4ad5c3f6efba4e788>`_:   Added EL9 instructions

`d23db48f2 <https://github.com/HEPCloud/decisionengine/commit/d23db48f2d49d4f56600aedf290acbc3099ae624>`_:   Upgrading isort version to fix install error w/ poetry

`fd3c5bda7 <https://github.com/HEPCloud/decisionengine/commit/fd3c5bda703fe168d5b72c52e428ae3ba72e85cc>`_:   explicitly select a container with all our required python versions

`85617b14d <https://github.com/HEPCloud/decisionengine/commit/85617b14dc0639a4d98503633bda3a3b9dc5296f>`_:   fix source logging by defining logger in Sources correctly

`669555cc7 <https://github.com/HEPCloud/decisionengine/commit/669555cc7144b18a0ffb4076412e5c9f9f67c98f>`_:   Add docstrings.

`1681f211d <https://github.com/HEPCloud/decisionengine/commit/1681f211d999e9a3d8e9fa4fd39a7aefd6aa62e4>`_:   Add timing information for when publisher was disabled.

`33e4f699e <https://github.com/HEPCloud/decisionengine/commit/33e4f699e810863ab7304531d4018a6d631712ea>`_:   Test publisher status w/in publisher.

`4d3d9100b <https://github.com/HEPCloud/decisionengine/commit/4d3d9100b6bbf491dccf932cbeeace90b656be66>`_:   Some renaming.


Release 2.0.3
-------------

Skipping this tag

Release 2.0.2
-------------

This is mainly a bug fix and documentation release. Instructions to run on EL8 have been added.
Also a UP/DOWN status metric was added via Prometheus.

Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `428 <https://github.com/HEPCloud/decisionengine_modules/issues/428>`_ : Decision engine 1.7.3 bug too many open file descriptors in glide_frontend_element.py
- `427 <https://github.com/HEPCloud/decisionengine_modules/pull/427>`_ : Set CONTINUE_IF_NO_PROXY to False to allow hybrid configuration

Full list of commits since version 2.0.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`7ec132e9 <https://github.com/HEPCloud/decisionengine/commit/7ec132e9f66d22f44ad7ebc87bf901ba7009aee1>`_:   [pre-commit.ci] auto fixes from pre-commit.com hooks

`b942241a <https://github.com/HEPCloud/decisionengine/commit/b942241a8fdbc69a12a3562b1010afdbad6d82c9>`_:   Add installation instructions for CentOS 8

`4f6fc134 <https://github.com/HEPCloud/decisionengine/commit/4f6fc134c7e830bfdcc9c34c54e263950970d85a>`_:   [pre-commit.ci] auto fixes from pre-commit.com hooks

`e8d1922e <https://github.com/HEPCloud/decisionengine/commit/e8d1922ecbe4a301d72ad0370d4b759d4f4adf23>`_:   Fix docstrings errors and warnings

`fc6aefd5 <https://github.com/HEPCloud/decisionengine/commit/fc6aefd5ae51e1a2336e34a9d44e82d949cd9eaf>`_:   Docker container and test setup for EL8

`51d5293f <https://github.com/HEPCloud/decisionengine/commit/51d5293f30c00cc1844166ce6dce80096a9e1bb4>`_:   [pre-commit.ci] auto fixes from pre-commit.com hooks

`0c15d3bd <https://github.com/HEPCloud/decisionengine/commit/0c15d3bd6ff308a90ad4068dc29e2fad4441afa1>`_:   Added UP/DOWN status metric of the decision engine

`fc76a1f0 <https://github.com/HEPCloud/decisionengine/commit/fc76a1f0e86bfd948b632c80694f9352f382a36b>`_:   Fixup coverage for new version

`04b18750 <https://github.com/HEPCloud/decisionengine/commit/04b187501ee41114a972cc12b15aa2fad5e20859>`_:   Set upper limit version for flake8. This is needed to have pytest-flake8 and flake8 versions working together.

`98797411 <https://github.com/HEPCloud/decisionengine/commit/98797411868f9c2791976d078141d97eab0ad946>`_:   Add 'Setup pressure-based pilot submission' section to install document

`0165183c <https://github.com/HEPCloud/decisionengine/commit/0165183cb7fa72bfb0927b023b324143ae92668f>`_:   make RPM requires more flexible

`28e2a0d4 <https://github.com/HEPCloud/decisionengine/commit/28e2a0d4211d02f80eee12b87be1764c456195bf>`_:   Updated release notes for 2.0.1 and porting of 1.7.3


Release 2.0.1
-------------

Patch level (bug fix) release.


Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bugs fixed:

- `DE 639 <https://github.com/HEPCloud/decisionengine/issues/639>`_: de-client --status stalls whenever channels are not yet in STEADY state
- `DE 638 <https://github.com/HEPCloud/decisionengine/issues/638>`_: Sources should go offline if the client channel offline
- `DE 634 <https://github.com/HEPCloud/decisionengine/issues/634>`_: de-client --stop-channel / --start-channel doesn't work in 2.0rc2
- `DE 626 <https://github.com/HEPCloud/decisionengine/issues/626>`_: New DE 2.0rc2 regularly takes 2-3 minutes to shut down
- `DE 599 <https://github.com/HEPCloud/decisionengine/issues/599>`_: Clarify timeout variable in block_while()
- `DE 522 <https://github.com/HEPCloud/decisionengine/issues/522>`_: Decision engine log files get split between several different processes with several different versions open
- `DE 236 <https://github.com/HEPCloud/decisionengine/issues/236>`_: New race condition in de-client

Enhancements:

- `DE 650 <https://github.com/HEPCloud/decisionengine/issues/650>`_: Added separate log files for Sources


Full list of commits since version 2.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`b5e56ab8 <https://github.com/HEPCloud/decisionengine/commit/b5e56ab8701266e890fed6e9ca4baff49c131c86>`_:   Remove signal handler.

`0fb6814b <https://github.com/HEPCloud/decisionengine/commit/0fb6814b8e26c1249fe80f1b3df19f76f1b2ddf1>`_:   Prevent blocking (if possible) during service actions.

`bb68fc31 <https://github.com/HEPCloud/decisionengine/commit/bb68fc311d8a35e3ebccecfff5148ba5396b5557>`_:   Add logging handler to client-message receiver.

`53fefbc5 <https://github.com/HEPCloud/decisionengine/commit/53fefbc5adce62c0d70b3c8e0154d1ff27fa3650>`_:   Update kombu version.

`009cdd95 <https://github.com/HEPCloud/decisionengine/commit/009cdd95108719f9b19f6bc6f4d8941f59478a1b>`_:   Use kombu queues for server/client communication.

`29a1ee25 <https://github.com/HEPCloud/decisionengine/commit/29a1ee25c8b71d73a029f7b2e13e19b8fca061dd>`_:   add distinct logging for sources

`e44e9210 <https://github.com/HEPCloud/decisionengine/commit/e44e9210059ffa28215e57c120c61418c9b2b4e9>`_:   Update GitHub actions; pylint workaround.

`d192f8fb <https://github.com/HEPCloud/decisionengine/commit/d192f8fb19810bd9ff7f2fdb60effcb42e8a5927>`_:   Lock typing_extensions for Python 3.6 compat

`2b946043 <https://github.com/HEPCloud/decisionengine/commit/2b9460433338c9245ae9dbc065584f8cc36c3679>`_:   Fix pre-commit node version to 17.9.0, the last to support SL7.

`76f3ddfb <https://github.com/HEPCloud/decisionengine/commit/76f3ddfb8060f0f21dba80fc595ea668c130d7e3>`_:   lock pyupgrade to python3.6 support

`c9c7cb3e <https://github.com/HEPCloud/decisionengine/commit/c9c7cb3ec3533873a431303a85282424203bbb48>`_:   Include psutil as part of runtime requirements.

`df8a3941 <https://github.com/HEPCloud/decisionengine/commit/df8a394181c98c35189aca885b5471ae86b99bf0>`_:   Make sure to kill worker process.

`69924d0c <https://github.com/HEPCloud/decisionengine/commit/69924d0c1dbc6c863c691bfee576396c9fadef63>`_:   Do not block de-client calls during startup.

`ddb18d7c <https://github.com/HEPCloud/decisionengine/commit/ddb18d7cc1004742a4b41ef347f04c171dc50afe>`_:   Minor cleanups.

`f4dc7da7 <https://github.com/HEPCloud/decisionengine/commit/f4dc7da7ed9c1162a352bd7f50260252528b5deb>`_:   Do not take source offline more than once during detach.

`cbffa992 <https://github.com/HEPCloud/decisionengine/commit/cbffa992f59c666540c6b19b2443acbfcdf02f07>`_:   Update Docker entrypoint script for DE 2.0 branch

`e10fe5af <https://github.com/HEPCloud/decisionengine/commit/e10fe5afbb72d3c96fc83da9a6d889ebdbac4dd9>`_:   Fixed cross-package link in the documentation

`9da1eac8 <https://github.com/HEPCloud/decisionengine/commit/9da1eac86efa2f8f6519ad3faca19e2f518d737a>`_:   Added cross-package link in the documentation

`d278726b <https://github.com/HEPCloud/decisionengine/commit/d278726b1747385d42ad4e8264223376fa488ce8>`_:   Updated 2.0 release notes and indexes, ready for 2.0.0


Release 2.0.0
-------------

This release series follows 1.7. A lot started to happen in 1.7.0 and has happened since, so we felt it was proper
to change the major version number.
We are proud to introduce Decision Engine 2.0.0 to outside users: it provides a
friendlier installation procedure and configuration samples to test it
on all resources supported by the GlideinWMS Factory, like OSG, some HPC resources and
commercial cloud providers.

- New architecture with redesigned source system using Kombu message passing with a Redis backend.
- Token support via DE modules: support for SciToken, WlcgToken (for CE authentication) and HTCondor Idtokens (for Glideins and Factory communication)
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

`685a3a8e <https://github.com/HEPCloud/decisionengine/commit/685a3a8eaf0f86e7c6df305f256d58b068963320>`_:   Added changelog file for developers curated list of changes

`044f4463 <https://github.com/HEPCloud/decisionengine/commit/044f44631b7155b006f411061d6ff9fe6c9ff38b>`_:   Updated 1.7 and 2.0 release notes, ready for 2.0.0 RC4

`19994fb5 <https://github.com/HEPCloud/decisionengine/commit/19994fb5544d04d572093b346d7fd9ab1cb0bbdf>`_:   Convert timeout program options to floats.

`e2055f92 <https://github.com/HEPCloud/decisionengine/commit/e2055f92b66c7d9dd5a21bf777d6bf3b2691cf83>`_:   Address Marco's review comments.

`abdf35ad <https://github.com/HEPCloud/decisionengine/commit/abdf35ad566682e42672d565451f35fb9fb636c3>`_:   Restore multiple queues but purge source queue after each publish.

`52936cb5 <https://github.com/HEPCloud/decisionengine/commit/52936cb5cfb18db33ad166bb651b318636e73912>`_:   Improve error-handling.

`aad20744 <https://github.com/HEPCloud/decisionengine/commit/aad20744655a26d7045b20be9ce41fcfd5ff9720>`_:   Change to multiprocessing.Lock for protecting channel/source workers.

`24bbee41 <https://github.com/HEPCloud/decisionengine/commit/24bbee4175631600533975bc1c8f2e95e54d350a>`_:   Adjust launching of source workers in attempt to avoid deadlock.

`6d13a392 <https://github.com/HEPCloud/decisionengine/commit/6d13a3929f995ac5a6512716ef5dc9b431a1ec2a>`_:   Remove unnecessary (and perhaps harmful) external updating of channel states.

`5456f32f <https://github.com/HEPCloud/decisionengine/commit/5456f32f2e63a75574710b230975cc8a98687350>`_:   Improve test coverage.

`1afabb70 <https://github.com/HEPCloud/decisionengine/commit/1afabb7097d50d1556d8a12abda6d2abb1a55955>`_:   Use service_actions to disable sources whenever client channels fail.

`7f67a172 <https://github.com/HEPCloud/decisionengine/commit/7f67a1729bbabdfe60da20a110893f071a3bc113>`_:   Various naming and logging adjustments

`e6e49184 <https://github.com/HEPCloud/decisionengine/commit/e6e491847909dc3af6f9709756f607a584d2cfd2>`_:   Adjust de-client --status and add --product-dependencies program option.

`a7c1f351 <https://github.com/HEPCloud/decisionengine/commit/a7c1f351312f05a85842c94f8f7cf2914ae6c470>`_:   Apply block-while timeout to all channels, not each channel.

`3d739ec7 <https://github.com/HEPCloud/decisionengine/commit/3d739ec7372764f9d7af813cafe46ef4c0a8c3ee>`_:   Update ci workflow to include workflow_dispatch mechanism and to customize artifact file name

`c5a05650 <https://github.com/HEPCloud/decisionengine/commit/c5a05650590c79a373c608e3fbe9c701ba1e3364>`_:   Archive unit test logs in case of unit test failure and make them available as artifacts

`e94c2abb <https://github.com/HEPCloud/decisionengine/commit/e94c2abb215edcebf76f7f978dd879ad263e5609>`_:   Update Python 3.6-compatible pre-commit hooks.

`aeb6b974 <https://github.com/HEPCloud/decisionengine/commit/aeb6b9742d1d0ac3d68329255216e9a9677135ee>`_:   Update Countdown docstrings.

`525eb3a8 <https://github.com/HEPCloud/decisionengine/commit/525eb3a8ac6e01b304b3b47438444bac0b5c4e19>`_:   Add Countdown class to address global timeout problem.

`4c458e0c <https://github.com/HEPCloud/decisionengine/commit/4c458e0c225ec2ce1e82d56e752724983331b7d1>`_:   Updated release notes for 2.0.0 RC3 (1.7.99.post3)

`137b574a <https://github.com/HEPCloud/decisionengine/commit/137b574ad5209bb649ce84fba06dde7196c358dc>`_:   Add a minimal container image more suited to production usage

`9d7f6875 <https://github.com/HEPCloud/decisionengine/commit/9d7f68758d4477bb3ab85bfbcd008fda37485426>`_:   Provide de-client --queue-status program option.

`a7dcc30d <https://github.com/HEPCloud/decisionengine/commit/a7dcc30d7d0d247f7d4dc32dbb518767bfd8b0fd>`_:   Ensure that channels and sources shared the same queues.

`49a316e0 <https://github.com/HEPCloud/decisionengine/commit/49a316e05c90b6cc5fd3532ae23df0f98417c335>`_:   Restore pyupgrade to v2.30, which works on Python 3.6

`2ce5ccb6 <https://github.com/HEPCloud/decisionengine/commit/2ce5ccb6ffe34ac6837b5da9a2bdefd8335ad2e6>`_:   [pre-commit.ci] pre-commit autoupdate

`7bd41851 <https://github.com/HEPCloud/decisionengine/commit/7bd41851d521fe7742ee7b23395caff88e4359fa>`_:   Print number of pickled bytes of source-produced data.

`97aed846 <https://github.com/HEPCloud/decisionengine/commit/97aed84622d8ea19dd35ad60f20bfcdc7efd10bd>`_:   Protect tests from Redis DB/routing-key collisions.

`4d3abab7 <https://github.com/HEPCloud/decisionengine/commit/4d3abab7e9ddc2295474b501b36c36b9fe92b835>`_:   Flush the Redis DB once the DE server stops.

`e36c2150 <https://github.com/HEPCloud/decisionengine/commit/e36c2150e2d05fbde9a8276df32653391901d5da>`_:   Remove unnecessary @pytest.mark.usefixtures(...) decorations.

`30d68610 <https://github.com/HEPCloud/decisionengine/commit/30d686107dcd1ceef4cd7f9aeebd931cfc26a1cb>`_:   More unit testing

`7850995d <https://github.com/HEPCloud/decisionengine/commit/7850995dbb6249413ed5042d813f0a3450afdd0e>`_:   We should have one path where we test without -v.

`a81a52cc <https://github.com/HEPCloud/decisionengine/commit/a81a52cc05a039b6c056d6f2d0d822d1f3229025>`_:   A simple test to ensure the metrics can run

`7547720c <https://github.com/HEPCloud/decisionengine/commit/7547720c58577b836d85cc11041628b0378f0f9e>`_:   Logger tests are a bit unstable at high parallelization.

`56516df7 <https://github.com/HEPCloud/decisionengine/commit/56516df7d8f8c0886e64d4d1f504e4eeda2f0fea>`_:   Add missing test to ensure we can change the channel level twice

`abde7d0f <https://github.com/HEPCloud/decisionengine/commit/abde7d0fe64eabe8c04958d923ebb6e12b0fc5c8>`_:   Add missing tests for inherited functions

`6522ed37 <https://github.com/HEPCloud/decisionengine/commit/6522ed37b08aa5edd54fbb10c1bcc02d851e229e>`_:   Note lines we are not testing

`de7829a4 <https://github.com/HEPCloud/decisionengine/commit/de7829a4e482513772b741976b89087d9933782f>`_:   Remove the unit test log directory if it got created

`28fbd599 <https://github.com/HEPCloud/decisionengine/commit/28fbd599fe4b8087d7df69b5f0019f97fd323aa9>`_:   pin jsonnet 0.17.0

`9c5c827e <https://github.com/HEPCloud/decisionengine/commit/9c5c827e422324e28a00f67f99da12b34859e246>`_:   Metrics seems to want the channels setup to complete

`b8829997 <https://github.com/HEPCloud/decisionengine/commit/b8829997844f77f906bdab19181a1af263b709a9>`_:   Pin pytest version

`b348d6f7 <https://github.com/HEPCloud/decisionengine/commit/b348d6f7e1ecb0b35c77267fead871cca86bbb5e>`_:   Fix deadlock starting cherrypy metrics server

`7697e6c1 <https://github.com/HEPCloud/decisionengine/commit/7697e6c119de4ce1507032a8aa4a5f340d80b340>`_:   Log invocation of random port

`9e7e4813 <https://github.com/HEPCloud/decisionengine/commit/9e7e4813cc450b9d21883b6e13ba11706912cdf3>`_:   Clarify note on xdist, run more workers

`0b495fbf <https://github.com/HEPCloud/decisionengine/commit/0b495fbf588eb7360ccb3fc3509b4b8232c5ac5f>`_:   Leave note to remember to cleanup temp files

`ca5ddf6f <https://github.com/HEPCloud/decisionengine/commit/ca5ddf6f6da5b234edae0f5a8a4f6e205c0520e8>`_:   Ensure we are calling the cherrypy shutdown methods

`e60efe78 <https://github.com/HEPCloud/decisionengine/commit/e60efe78527d41e212a2df3771d60f97ec9176cc>`_:   Move metrics fixtures to the fixtures file

`9c717cc5 <https://github.com/HEPCloud/decisionengine/commit/9c717cc50055ceb9ef5cabc595b61117ecd49006>`_:   Log finished with DB init

`55965f9e <https://github.com/HEPCloud/decisionengine/commit/55965f9e9d154b2ce327f8cc574b35ce55705343>`_:   Prep the server fixture to permit the metrics webserver

`732ff99b <https://github.com/HEPCloud/decisionengine/commit/732ff99b3d24d83af6a0e290d72ed8dbccd44b85>`_:   Add a 'ping' method

`6117cc95 <https://github.com/HEPCloud/decisionengine/commit/6117cc9515d47c20fb3b67e7ac7b17c4fbe7e209>`_:   [pre-commit.ci] pre-commit autoupdate

`b5af73ca <https://github.com/HEPCloud/decisionengine/commit/b5af73ca69dedac73e696e0142bda081ab92446e>`_:   More logging about cherrypy state

`dfe4278f <https://github.com/HEPCloud/decisionengine/commit/dfe4278f6c9fca7e934f34b251e719fd5d232a9b>`_:   Added unlinked release notes for DE 2.0.0

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

`cd345701 <https://github.com/HEPCloud/decisionengine/commit/cd345701539b9444eb09d6fece5b7445696b05f5>`_:   Increase coverage in LogicEngine

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
