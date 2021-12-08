.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Decisionengine Docker image
===========================

| The Docker image used to run tests for decisionengine framework and modules repositories is created using the Dockerfile in decisionengine repository.
| The docker image is named *decision-engine-ci* and it is hosted on `hepcloud docker hub <https://hub.docker.com/repository/docker/hepcloud/decision-engine-ci>`_.

In order to accommodate software requirements for different branches, each branch to be tested has its own tag of the docker image.
Currently are present *master* and *1.4* tags.

Automated docker image builds
-----------------------------
Hepcloud docker hub can be configured to build new docker images when there are changes to selected branches in a github repository.
Configuration details are available in `docker hub documentation <https://docs.docker.com/docker-hub/builds/>`_.

Any time a git push is made against one of the branch of interest in decisionengine framework repository, docker hub triggers a build for the associated docker image.

The docker image tags are chosen to be the same as the repository branch name, plus we have the tag *latest* that is built out of the master branch.
Currently we have this configuration in place.

==========  =======
Docker Tag  git branch
1.4         1.4
master      master
latest      master
==========  =======

Manual build of docker image
-----------------------------
Although there is in place an automatic procedure to build docker images, it can be handy to build a docker image manually for testing purpose or alike.

From inside the decisionengine directory, where the Dockerfile is, the commands to build and push the new docker image on docker hub are::

 docker build --pull -t hepcloud/decision-engine-ci:master -f Dockerfile ./
 docker push hepcloud/decision-engine-ci:master

Details about those docker commands can be found in `docker documentation <https://docs.docker.com/engine/reference/commandline/docker/>`_.
