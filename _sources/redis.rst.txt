Decisionengine Redis broker
===========================

Before getting started with Redis, please read https://redis.io/topics/security.

To keep Redis deployment consistent, we are recommending use of the official Redis
container (https://hub.docker.com/_/redis).

If you are intending to run Redis on a shared network, review the container
instructions for setting passwords.

For the most simple instance, on the DE Server, run::

 podman run --name decisionengine-redis -p 127.0.0.1:6379:6379 -d redis:6 --loglevel warning

It should now be avaliable at redis://127.0.0.1:6379/

Persistant storage is not currently required for our usage.
