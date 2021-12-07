# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import abc
import gc

from threading import Lock
from weakref import WeakValueDictionary

import structlog

from decisionengine.framework.modules.logging_configDict import DELOGGER_CHANNEL_NAME, LOGGERNAME

LOCK = Lock()

__all__ = [
    "ScopedSingleton",
    "Singleton",
    "ScopedSingletonABC",
    "SingletonABC",
]

logger = structlog.getLogger(LOGGERNAME)
logger = logger.bind(module=__name__.split(".")[-1], channel=DELOGGER_CHANNEL_NAME)


class Singleton(type):
    """
    Singleton pattern using Metaclass with strong refs
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        klass = cls._instances.get(cls, None)  # get a strong ref if it exists

        if klass is not None:
            logger.debug(f"found instance of {cls}")
            return klass

        with LOCK:  # so that threads can't make parallel versions
            klass = cls._instances.get(cls, None)  # get a strong ref if it exists
            if klass is not None:  # pragma: no cover
                # this case can be very hard to hit if cls inits super fast
                # with trivial unit tests, it isn't going to happen
                logger.debug(f"found instance of {cls} after lock")
                return klass

            logger.debug(f"Making instance of {cls}")
            klass = super().__call__(*args, **kwargs)  # make a strong ref
            cls._instances[cls] = klass

        return klass


class SingletonABC(abc.ABCMeta, Singleton):
    pass


class ScopedSingleton(Singleton):
    """
    Singleton pattern using Metaclass with weak refs
    """

    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        # pypy uses delayed garbage collection
        # so we need to do an explicit garbage collection here
        gc.collect()
        return super().__call__(*args, **kwargs)


class ScopedSingletonABC(abc.ABCMeta, ScopedSingleton):
    pass
