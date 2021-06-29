Release 1.7.0
-------------

In this release:

- New produces-consumes structure using decorators. This will improve the code quality, improving static checks and reducing the lines of code by removing repetitive boilerplates, especially in the modules.

Planned:
- Added structured logging. Improved python logging and adoption of structured logs format that will increase the semantinc content of the messages and ease the export of information for dashboards and Elastic Search.
- Addedf SQLAlchemy object-relational mapper to allow different database backends.
- Packaging via setuptools for both decisionengine and decisionengine_modules: RPM packages correctly install also all dependencies.

.. note::
    Added requirement on SQLAlchemy (for test framework)


Issues fixed in this release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


- `253 <https://github.com/HEPCloud/decisionengine/issues/253>`_ : Decision engine can sometimes start up at boot time before network name resolution is working (`ae04db5 <https://github.com/HEPCloud/decisionengine/commit/ae04db544599c6777d63cb315ddac169e586809d>`_)


Full list of commits since version 1.6.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`a25a4a3 <https://github.com/HEPCloud/decisionengine/commit/a25a4a3064c879b9e415ec8ece8cc813a3cf7c51>`_:   Fix ABC to match our actual usage

`1510b2d <https://github.com/HEPCloud/decisionengine/commit/1510b2d134165b9752101c9b981514ba5b4f8093>`_:   Address minor linting issues

`945e4b1 <https://github.com/HEPCloud/decisionengine/commit/945e4b16a8246d72a65a023501b84258e3d10e66>`_:   Fix missing attribute insert

`5eace9d <https://github.com/HEPCloud/decisionengine/commit/5eace9d51c4032585cc8821ccba1c59b36b8a730>`_:   Add note for how to get modules in place

`50a8e26 <https://github.com/HEPCloud/decisionengine/commit/50a8e2688987152523d83d4a8ac2e4d9435fb192>`_:   Add list of packages in the CI env to output

`b9cb197 <https://github.com/HEPCloud/decisionengine/commit/b9cb197d102f4755fb6ad074903ef1ceda983aa9>`_:   Sanity check the home directory

`cd17223 <https://github.com/HEPCloud/decisionengine/commit/cd17223c367ca692a94a3481c91b1c4d3b081abc>`_:   Have client provide a hint when you ask for no behavior

`95b0236 <https://github.com/HEPCloud/decisionengine/commit/95b02365d88e7d3a9f3a69f62491a4016ac77fc5>`_:   Fix de-query-tool to support produce/consume model

`e660ca7 <https://github.com/HEPCloud/decisionengine/commit/e660ca726b3457d4aecf4ae2f18b3e03419cc2f3>`_:   Update required versions for bugfixes

`6863cb8 <https://github.com/HEPCloud/decisionengine/commit/6863cb81174aff1598ac51b723070a1f1bd851f8>`_:   Fix path error

`bb52e8b <https://github.com/HEPCloud/decisionengine/commit/bb52e8b1659dea39aa3b853056893d7d85c343e0>`_:   Merge pull request #340 from jcpunk/service-stop

`6d7aba9 <https://github.com/HEPCloud/decisionengine/commit/6d7aba953ffce34d27685029b05f03977c4baf5f>`_:   Drop obsolete files

`168ae7a <https://github.com/HEPCloud/decisionengine/commit/168ae7aa0cc136a56b064e2a4d4f81aab746fa92>`_:   Name the tests better

`0f60c4e <https://github.com/HEPCloud/decisionengine/commit/0f60c4e3911686a47a12819c2276801e7868fa8e>`_:   Support new produces/consumes/configuration-description infrastructure.

`8191246 <https://github.com/HEPCloud/decisionengine/commit/819124695fbf8cb75ccbd7bf861d07b85fa1ab32>`_:   Add de-query-tool

`2a26c94 <https://github.com/HEPCloud/decisionengine/commit/2a26c9442938a376aa070c03fe6e12d4f744c9f0>`_:   ExecStopPre is not supported on all systemd instances

`67a54d5 <https://github.com/HEPCloud/decisionengine/commit/67a54d5cceeb9d4e5c6c7eaff8fa0e312d252f7a>`_:   Merge pull request #338 from jcpunk/fix-pytest-postgres

`70ab133 <https://github.com/HEPCloud/decisionengine/commit/70ab133ff92a82972bcefd36e989c1b373688b74>`_:   Fixup use of pytest_postgresql for version 3.0.0

`f8f4255 <https://github.com/HEPCloud/decisionengine/commit/f8f4255eb3dee4ab92e20df7f72e840c643f02a5>`_:   Merge pull request #337 from jcpunk/thread-names

`5f49a4f <https://github.com/HEPCloud/decisionengine/commit/5f49a4f63a1bd24e24ef91e2d870b8af5585f943>`_:   Set names for the various parallel code

`64da77c <https://github.com/HEPCloud/decisionengine/commit/64da77c6de71787386911e41b120627427c87fc8>`_:   Merge pull request #327 from jcpunk/datablock-expire

`de33a60 <https://github.com/HEPCloud/decisionengine/commit/de33a60a19510d1cbfea47c01c19eea7aef78e1c>`_:   Merge pull request #336 from knoepfel/use-toposort

`31a8a90 <https://github.com/HEPCloud/decisionengine/commit/31a8a9053a2067c6a14485bcaf96fb3724a42547>`_:   Merge pull request #328 from knoepfel/de-class-inference

`410e383 <https://github.com/HEPCloud/decisionengine/commit/410e383de712bdd5fcd5a6cc6e04deca8ce923bb>`_:   Merge pull request #331 from jcpunk/reaper-interval-tests

`719ff0c <https://github.com/HEPCloud/decisionengine/commit/719ff0c85a77376c19d7681bdf18c7abfc1f9c5d>`_:   Test datablock expire funtions

`e14c49d <https://github.com/HEPCloud/decisionengine/commit/e14c49d80537b549fea884546378fc5917c1591b>`_:   The 'name' parameter is optional.

`7846c9f <https://github.com/HEPCloud/decisionengine/commit/7846c9f3f9a0a83b0de168b30569138763691a21>`_:   Enable DE class inference based on configuration.

`32ab7e4 <https://github.com/HEPCloud/decisionengine/commit/32ab7e44c4c748938d7837ac96d12bf7a92525fc>`_:   Use third-party topological sort.

`01aa8ae <https://github.com/HEPCloud/decisionengine/commit/01aa8ae678f598f0b1b1941b63dcc6df66852304>`_:   Merge pull request #325 from jcpunk/channel-tests

`52b4847 <https://github.com/HEPCloud/decisionengine/commit/52b48479094c37acc5422301cc0ebce721db65bc>`_:   Merge pull request #326 from jcpunk/valid-config-tests

`8c4749e <https://github.com/HEPCloud/decisionengine/commit/8c4749e7d61727b820fee8b86ca572b4fe68585f>`_:   Merge pull request #330 from jcpunk/pylint-actions

`a37770c <https://github.com/HEPCloud/decisionengine/commit/a37770c9527932f81d754119524ffff6f8406c4d>`_:   Ensure validation testing is tested

`d8ab5eb <https://github.com/HEPCloud/decisionengine/commit/d8ab5eb6fd0998167635923a391d94785ab6a53f>`_:   Add missing test to ensure the run interval is actually used

`0cd9c42 <https://github.com/HEPCloud/decisionengine/commit/0cd9c42b708179a25cb4998466a39c86db66e069>`_:   Also run pylint for extra sanity checks

`c5cf1ff <https://github.com/HEPCloud/decisionengine/commit/c5cf1fff9e5b191c4fd913d185805b5d3dbabecd>`_:   Ensure our errors error out

`baf0170 <https://github.com/HEPCloud/decisionengine/commit/baf01700d8bb6cf4f8aca28e7fdd0726e3f617e0>`_:   Merge pull request #324 from jcpunk/cleanup-trivial-tests

`2a0133a <https://github.com/HEPCloud/decisionengine/commit/2a0133aadfba0fef2a70fcf43528bb60b7ed01bb>`_:   Try to cleanup trivial missing coverage

`44e0ad6 <https://github.com/HEPCloud/decisionengine/commit/44e0ad6f039dc2982f8e72cd56bcf0caf6737e5c>`_:   Merge pull request #323 from jcpunk/about-coverage

`d811f61 <https://github.com/HEPCloud/decisionengine/commit/d811f6174ecd77e40e84fac8b5eabe1d24aaa69d>`_:   Merge pull request #322 from knoepfel/fix-fail-on-error

`cb42626 <https://github.com/HEPCloud/decisionengine/commit/cb42626213ffed843eae5916c2b1fd535d9883f1>`_:   Merge pull request #312 from jcpunk/finish-setuptools

`8f6d407 <https://github.com/HEPCloud/decisionengine/commit/8f6d407de53f95602a3dce29603d23ab0ea4390c>`_:   Merge pull request #316 from jcpunk/abc-coverage

`4d0676b <https://github.com/HEPCloud/decisionengine/commit/4d0676bbe82d9b3adf89b0b660734755b5f14168>`_:   Merge pull request #317 from vitodb/pylint

`d7c43b9 <https://github.com/HEPCloud/decisionengine/commit/d7c43b961dbc4f092fdd39a73277be5d73dc9c2c>`_:   Use regular expression to support fail_on_error feature.

`ada6692 <https://github.com/HEPCloud/decisionengine/commit/ada6692533280d4171804ae2cc26f5337d721f0f>`_:   add support to run pylint tests

`efb1e57 <https://github.com/HEPCloud/decisionengine/commit/efb1e57bfdb7c03420440d34ad679eb5da618bc4>`_:   Finish migration to pure setuptools

`bc4720c <https://github.com/HEPCloud/decisionengine/commit/bc4720cf0e65f1df2b73958cbd64c5dabf84764c>`_:   We aren't testing 'unversioned" releases

`e4dc35e <https://github.com/HEPCloud/decisionengine/commit/e4dc35e36f75b14c71e0626afc7e1376adbac3df>`_:   Merge pull request #314 from jcpunk/jsonnet_syntax

`87e32c2 <https://github.com/HEPCloud/decisionengine/commit/87e32c228376bbe5a3cf513ac2890b2a8b7b793b>`_:   Merge pull request #294 from jcpunk/move-reaper

`dec85d5 <https://github.com/HEPCloud/decisionengine/commit/dec85d5ebb7cf9b8fb19c73ac5a68e9855503dba>`_:   Merge pull request #319 from jcpunk/task-loop

`4108472 <https://github.com/HEPCloud/decisionengine/commit/4108472afc04def8c35f7aaa569fd76568cf162f>`_:   Merge pull request #320 from jcpunk/container-swig

`920af1c <https://github.com/HEPCloud/decisionengine/commit/920af1c985f84896d92a1f5fe28ee8072d654247>`_:   Merge pull request #321 from knoepfel/include-init-files

`650dffa <https://github.com/HEPCloud/decisionengine/commit/650dffa70ea4bcca0022adb79823d53d81849d70>`_:   Don't forget __init__.py files.

`1b412e0 <https://github.com/HEPCloud/decisionengine/commit/1b412e03067216451d0552f434277d6069300ae3>`_:   The latest m2crypto seems to need swig now

`a6e3ab1 <https://github.com/HEPCloud/decisionengine/commit/a6e3ab1c283e5ec596cde771db9fd3fc6d97125d>`_:   Merge pull request #313 from jcpunk/conf-test

`1205636 <https://github.com/HEPCloud/decisionengine/commit/1205636a69763ef71d1baa273c92d0dbc51e46db>`_:   Simplify run loop

`30e59dc <https://github.com/HEPCloud/decisionengine/commit/30e59dc967285d13221dfee7b807f446f9fbfac2>`_:   fix test_client_with_no_server_verbose unit test for Jenkins CI (#315)

`10384a8 <https://github.com/HEPCloud/decisionengine/commit/10384a8cf3167bbadc0bfea08291c9eeb20cb01c>`_:   Move reaper into its own place and reuse state logic

`940584e <https://github.com/HEPCloud/decisionengine/commit/940584e446d9841e006b87dc5a0446cc52e664d8>`_:   No real way to test abstract base classes

`250c14b <https://github.com/HEPCloud/decisionengine/commit/250c14b151ba273417c09306556e591e9981d768>`_:   The `_validate` function doesn't permit missing 'PRODUCES'

`5ae1ce9 <https://github.com/HEPCloud/decisionengine/commit/5ae1ce9fc748a146777dd8f5bd63a96a7bc09fac>`_:   Make sure syntax error in config names the problem

`b899fa2 <https://github.com/HEPCloud/decisionengine/commit/b899fa237d20f949f1adf147fa7d6da55381b4b2>`_:   Add SourceProxy module test. (#307)

`7b3df14 <https://github.com/HEPCloud/decisionengine/commit/7b3df14c7a26c9d3ba2b0e56ac4598ed8d3c4d80>`_:   Increae coverage of utils (#304)

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
