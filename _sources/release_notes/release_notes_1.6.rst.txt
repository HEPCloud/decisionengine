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
