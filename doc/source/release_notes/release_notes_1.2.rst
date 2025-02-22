.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Release 1.2.0
-------------

In this release:


* Switched to python3
* Improved coverage
* Database data retention : added reaper to remove data older than configurable number of days
* Improved logging


decisionengine
~~~~~~~~~~~~~~

`3dfe167 <https://github.com/HEPCloud/decisionengine/commit/3dfe167968c431fe4448ee1d371a6216e073c8f4>`_
:   Jenkins pipeline improvements (#106)

`22a7073 <https://github.com/HEPCloud/decisionengine/commit/22a7073aeff6e65883a5a757db7deca04fcd51db>`_
:   pull request for review request 137 (#105)

`cafffb2 <https://github.com/HEPCloud/decisionengine/commit/cafffb24db7624c2fad7cccf27374072bd4d353b>`_
:   Make it possible to run code directly (for tests), and (#100)

`802e98b <https://github.com/HEPCloud/decisionengine/commit/802e98baefc81976ecad141987f442f98aabec10>`_
:   replace psycog2 witt psycopg2-binary (#101)

`573ce8f <https://github.com/HEPCloud/decisionengine/commit/573ce8f3095723cd1cd7b3447f921a1b81df1d9a>`_
:   Jenkins pipeline improvements (#99)

`9d08835 <https://github.com/HEPCloud/decisionengine/commit/9d08835e5da1859a533ffd6cc73e75f2fcb9fc41>`_
:   Run coveralls even under failed state (#97)

`bc1df4b <https://github.com/HEPCloud/decisionengine/commit/bc1df4b5da8b1f7f3093497e48121ecd95ee8495>`_
:   Add tests for PostgreSQL datasource (#71)

`c1ac391 <https://github.com/HEPCloud/decisionengine/commit/c1ac3911a69fab23400103ef26efe827a006a520>`_
:   Fix missing py-modules.html (#96)

`8dbfdee <https://github.com/HEPCloud/decisionengine/commit/8dbfdee2cd762e547b2b32d4ce7c41272b07196f>`_
:   Setup gh-pages doc workflow (#94)

`cd4a01a <https://github.com/HEPCloud/decisionengine/commit/cd4a01a9eab32ae180cef566ffa1ccdb2f0603a4>`_
:   Doc (#93)

`673080d <https://github.com/HEPCloud/decisionengine/commit/673080de6311ec497d63119a699c488e86ea33f7>`_
:   set version to 1.2.0 (for now). Supply conf file that corresponds to (#91)

`f912225 <https://github.com/HEPCloud/decisionengine/commit/f912225541d43d07334a8d9120ff713908a83454>`_
:   Db (#92)

`dc8b68a <https://github.com/HEPCloud/decisionengine/commit/dc8b68acb6dec69a766ac058e7eadb17e0f36b73>`_
:   Add reaper to the RPC (#83) (#90)

`29ade91 <https://github.com/HEPCloud/decisionengine/commit/29ade9127313b7bfea9ffdb4b5ce3d9a3abe84c2>`_
:   adding .Jenkinsfile with Jenkins pipeline configuration (#86)

`c1dfe5c <https://github.com/HEPCloud/decisionengine/commit/c1dfe5c2cd32c4cccdf0295bafc06ea45f3362f9>`_
:   Don't exclude E1004 from pylint, do exclude line breaks (#89)

`440f949 <https://github.com/HEPCloud/decisionengine/commit/440f949e0a16bd0bf3826cac39c4b4375f24308a>`_
:   Fix varname (#88)

`313d135 <https://github.com/HEPCloud/decisionengine/commit/313d135d7c90c3377c0daed7c250f3bf9a82da4e>`_
:   Compress (#87)

`6b8dc4b <https://github.com/HEPCloud/decisionengine/commit/6b8dc4b295ebd1e5f9751de49608fd90757ac81a>`_
:   Revert "Add reaper to the RPC (#83)"

`dbea8e5 <https://github.com/HEPCloud/decisionengine/commit/dbea8e5cb69d3ed4cc14bdaf2bf250b5d9275e1a>`_
:   Update utils.sh so pytest will complete.

`e848316 <https://github.com/HEPCloud/decisionengine/commit/e8483169ae99527888971f35751374662f098d64>`_
:   Update to postgresql11

`7f4b805 <https://github.com/HEPCloud/decisionengine/commit/7f4b8057843417ff52204283823c735d290c11f1>`_
:   Add reaper to the RPC (#83)

`0ba2c51 <https://github.com/HEPCloud/decisionengine/commit/0ba2c51c1d911baaee20fd2e36a5f99448d39939>`_
:   remove astpp module and dependencies it pulls in (#81)

`6b8eab9 <https://github.com/HEPCloud/decisionengine/commit/6b8eab9aaa1b4e2cd0ee4538bc6844cdd6b56517>`_
:   don't track test coverage of tests (#80)

`0da18ec <https://github.com/HEPCloud/decisionengine/commit/0da18ec903e56a72c955c08f492af8be8bf73a34>`_
:   made reaper.py executable

`aca24a3 <https://github.com/HEPCloud/decisionengine/commit/aca24a3840da92af2268e100cc6b15a7d1f1d2b0>`_
:   make reaper.py executable, make symbolic link to it from /usr/bin (#72)

`0202acf <https://github.com/HEPCloud/decisionengine/commit/0202acf5df330ee2cc5fe49fe95980901e157871>`_
:   Implementation of data reaper  (#70)

`16b6be1 <https://github.com/HEPCloud/decisionengine/commit/16b6be1f674ed356188520a3094cba3ec506cecf>`_
:   Simple changes for Python 3 deployment (#69)

`fd2418c <https://github.com/HEPCloud/decisionengine/commit/fd2418ce9713002e080c92ae339f2cb250f7af90>`_
:   Fix warnings caught by PEP-8 Speaks.

`d16359b <https://github.com/HEPCloud/decisionengine/commit/d16359bf5f00046edce4814f8326199903bd3e64>`_
:   Python 3 (and other) simplifications.

`3c7b6b7 <https://github.com/HEPCloud/decisionengine/commit/3c7b6b7bd22a3c1e7af5971ee6892542006a9ac5>`_
:   Only run Github Actions for python3.6 (#68)

`453cbba <https://github.com/HEPCloud/decisionengine/commit/453cbba897c328ac8bc9a8dd8ffaa0f6ae1d7a6c>`_
:   Update README.md

`b27ed53 <https://github.com/HEPCloud/decisionengine/commit/b27ed5320c962dd3c7f90e673181eae5e5cb8e5d>`_
:   remove unnecessary (and actually harmful) python shebang (#66)

decisionengine_modules
~~~~~~~~~~~~~~~~~~~~~~


`30d928b <https://github.com/HEPCloud/decisionengine_modules/commit/30d928b67a442206ad7fe7114b44ff6a2b9ff404>`_
:   clone version 1.2.0 of decisionengine

`ae7c5a6 <https://github.com/HEPCloud/decisionengine_modules/commit/ae7c5a6b9985e2270459635f315fd30a706352f8>`_
:   Jenkins pipeline improvements (#236)

`310befd <https://github.com/HEPCloud/decisionengine_modules/commit/310befdbf805fd6168132b852b881a4c6f5ed9dc>`_
:   T198 (#235)

`a65886d <https://github.com/HEPCloud/decisionengine_modules/commit/a65886d0a52ffd8b898a7daebe3ab155466c0820>`_
:   Fix import as reported in : https://github.com/HEPCloud/decisionengin… (#232)

`93711cc <https://github.com/HEPCloud/decisionengine_modules/commit/93711ccd802c8ee99ecfa9b9f824ae312c5b8d89>`_
:   Run coveralls even if tests fail (#229)

`03d763a <https://github.com/HEPCloud/decisionengine_modules/commit/03d763ae2646f5bbdbdbffffed0735daf68fc830>`_
:   Jenkins pipeline improvements (#230)

`f48d30f <https://github.com/HEPCloud/decisionengine_modules/commit/f48d30fa1e436b602f5a5f7c35645b97f3db6d83>`_
:   Fix/223 (#228)

`c8aa262 <https://github.com/HEPCloud/decisionengine_modules/commit/c8aa262964f7cd3891a8421fbaad9667d8e4f525>`_
:   github ticket 199 (#222)

`0323bda <https://github.com/HEPCloud/decisionengine_modules/commit/0323bda0241903ab8cc57fd37e66bbfcd40c412c>`_
:   Address : https://github.com/HEPCloud/decisionengine_modules/issues/224 (#226)

`62e4df6 <https://github.com/HEPCloud/decisionengine_modules/commit/62e4df697fe290f0780b8e10fc81727fdc31dfc1>`_
:   Add support to run CI on Jenkins (#221)

`5ab1541 <https://github.com/HEPCloud/decisionengine_modules/commit/5ab15411b79505d752cf21c3b2ec15213bd83be3>`_
:   bump master version to 1.2.0 (for now) (#219)

`bc19c65 <https://github.com/HEPCloud/decisionengine_modules/commit/bc19c6528ab89922a95465c3c67c60273255e039>`_
:   decisionengine_modules/NERSC: Added retry loop for NERSC API Calls (#220)

`41a50de <https://github.com/HEPCloud/decisionengine_modules/commit/41a50de88209542fd5ed15a8b529794a3ff66098>`_
:   Sync up pep8speaks and run_pylint.sh with decisionengine settings (#218)

`db4634f <https://github.com/HEPCloud/decisionengine_modules/commit/db4634f89f35b8f5dde6bac11ad5b66a756d68ed>`_
:   silence pylint error (#217)

`1b95141 <https://github.com/HEPCloud/decisionengine_modules/commit/1b95141a7ae7ef9f9b9d8a6da1cf7c69acc35379>`_
:   Fix whitespace around operator error

`746ea38 <https://github.com/HEPCloud/decisionengine_modules/commit/746ea38446c5908e5b24184299ce5e3b6eb6c0e9>`_
:   ignore W503

`8a8b5f4 <https://github.com/HEPCloud/decisionengine_modules/commit/8a8b5f4277a2d005249c4f75c03edb1e4408d800>`_
:   remove unused variable

`a6668bf <https://github.com/HEPCloud/decisionengine_modules/commit/a6668bf2b18cfd770be377419126e17004053e7c>`_
:   fix PEP8 warnings

`13773ee <https://github.com/HEPCloud/decisionengine_modules/commit/13773ee0ae5a25c5fd5bfc62feb1b899d2010bb4>`_
:   address pep8 warnings

`6bea4ca <https://github.com/HEPCloud/decisionengine_modules/commit/6bea4cadd184bbefd2339dcece2a2db2fe27c39d>`_
:   silence pylint error

`f589895 <https://github.com/HEPCloud/decisionengine_modules/commit/f5898958cd10f99137333ec314fc4cfecc97bcff>`_
:   Pass sort=True parameter to fix future warning (#215)

`a1d0507 <https://github.com/HEPCloud/decisionengine_modules/commit/a1d0507b62fc0fbe5386cdaf518e23702bf53159>`_
:   fixing pep8 warning

`a10bd17 <https://github.com/HEPCloud/decisionengine_modules/commit/a10bd17ed8160d1397c3d2c4462e39c60dd1b8b4>`_
:   debugging one import error

`ec501ad <https://github.com/HEPCloud/decisionengine_modules/commit/ec501ad738ef885e70e08dad59f15b2db555fc1c>`_
:   make coveralls.io links work

`deab1a7 <https://github.com/HEPCloud/decisionengine_modules/commit/deab1a77eac6a8a4315bdedf4fc1241df032b25e>`_
:   T201 (#204)

`69f2645 <https://github.com/HEPCloud/decisionengine_modules/commit/69f26451705f3d2b7336bb98db2387b70f0ba329>`_
:   Add coveragerc

`6d8a5f5 <https://github.com/HEPCloud/decisionengine_modules/commit/6d8a5f5f45159c18b2b79efab7e1dcabedbe039a>`_
:   decisionengine_modules/NERSC: Make Nersc API call backward-compatible with old config (#196)

`a7e0af9 <https://github.com/HEPCloud/decisionengine_modules/commit/a7e0af9572cc62987008dd8d7164cc1efc37921f>`_
:   Only run Github Actions for python3.6 (#24)
