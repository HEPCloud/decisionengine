.. SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
.. SPDX-License-Identifier: Apache-2.0

Decisionengine Redis broker
===========================

Before getting started with Redis, please read https://redis.io/topics/security.

To keep Redis deployment consistent, we are recommending use of the official Redis
container (https://hub.docker.com/_/redis).

If you are intending to run Redis on a shared network, review the container
instructions for setting passwords.

For the most simple instance, on the DE Server, run::

 podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning

It should now be available at redis://127.0.0.1:6379/

Persistent storage is not currently required for our usage.

.. note::  You may need to install ``podman`` from your system repositories; it should ship with a lot of `modern Linux distributions <https://podman.io/getting-started/installation>`_.  The ``podman`` package should be compatible with Docker, in most cases either one can be used without issue.  If ``podman`` is not available for your platform, you can review the Docker Desktop terms and conditions to see if you qualify for free usage.

.. note::  You may need to install ``nf-tables`` and remove ``ip-tables`` since Alma9 kernels support the former and not the letter. If you see an error like::
   Error: netavark: code: 3, msg: modprobe: FATAL: Module ip_tables not found in directory /lib/modules/5.14.0-503.21.1.el9_5.x86_64
   iptables v1.8.10 (legacy): can't initialize iptables table `nat': Table does not exist (do you need to insmod?)
   Perhaps iptables or your kernel needs to be upgraded.

 Then Run the commands::

   dnf rm iptables-legacy
   dnf install iptables-nft


Configuring the DE server
#########################

By default, the ``decisionengine`` server will use a local redis instance
and the default database there.  However, it is preferable to set this
specifically within the config so it is explicit.

``decision_engine.jsonnet``::

 {
   broker_url: "redis://localhost:6379/0"
 }

This is equivalent to the default, but provides a clear pointer within
the config file to the exact location of redis.

Reviewing the Redis content
###########################

The `redis-cli <https://redis.io/topics/rediscli>`_ command is the official
tool for looking at the content of a Redis data store.
