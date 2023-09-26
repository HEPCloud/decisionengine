<!--
SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
SPDX-License-Identifier: Apache-2.0
-->

We are providing a few EL9 `Dockerfile`s here to simplify a number of deployments.

These containers are a bit "proof-of-concept" and may not repersent best practices.

## framework

This `Dockerfile` will generate a container you can use to run an 'all in one' Decision Engine Framework server.

There are a few things you'll need to do yourself:

1. bind mount your config files into `/etc/decisionengine` (read only is ok)
2. bind mount a log storage location into `/var/log/decisionengine`
3. bind mount the decision engine code into the container
4. establish an entrypoint that starts : postgresql, redis, and the decision-engine server
5. expose the port you've configured for the Decision Engine Framework server

NOTE: currently the Decision Engine Framework server does not do authentication, localhost only please!

## framework-minimal

This `Dockerfile` will generate a container you can use to run just the Decision Engine Framework server.

There are a few things you'll need to do yourself:

1. bind mount your config files into `/etc/decisionengine` (read only is ok)
2. bind mount a log storage location into `/var/log/decisionengine`
3. bind mount the decision engine code into the container as `/home/decisionengine`
4. expose the port you've configured for the Decision Engine Framework server

NOTE: currently the Decision Engine Framework server does not do authentication, localhost only please!

### TODO

- Leave "our" wheel installed as a backup and let folks use a custom source repo as an option, rather than mandatory.
- The 'git clone' layer can be cached and thus not reflect the current tree's deps....
- For the container, maybe don't use `/etc` and `/var/log`?
- Find a clean way to get the de-modules deps loaded too
  - those may require more compilers etc
