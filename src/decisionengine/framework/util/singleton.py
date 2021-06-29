import abc
import gc
import structlog

from threading import Lock
from weakref import WeakValueDictionary

LOCK = Lock()

__all__ = [
    "ScopedSingleton",
    "Singleton",
    "ScopedSingletonABC",
    "SingletonABC",
]

logger = structlog.getLogger("decision_engine")
logger = logger.bind(module=__name__.split(".")[-1])


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
            klass = super(Singleton, cls).__call__(*args, **kwargs)  # make a strong ref
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
        return super(ScopedSingleton, cls).__call__(*args, **kwargs)


class ScopedSingletonABC(abc.ABCMeta, ScopedSingleton):
    pass
