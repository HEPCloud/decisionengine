# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import abc
import concurrent.futures
import threading

import pytest

from decisionengine.framework.util.singleton import ScopedSingleton, ScopedSingletonABC, Singleton, SingletonABC


class BasicClass(metaclass=Singleton):
    def __init__(self):
        self.value = 0


class BasicScopedClass(metaclass=ScopedSingleton):
    def __init__(self):
        self.value = 0


class AbstractClass(metaclass=SingletonABC):
    def __init__(self):
        self.value = 0

    @abc.abstractmethod
    def method(self):
        raise NotImplementedError("replace me")


class AbstractScopedClass(metaclass=ScopedSingletonABC):
    def __init__(self):
        self.value = 0

    @abc.abstractmethod
    def method(self):
        raise NotImplementedError("replace me")


class RealClass(AbstractClass):
    def method(self):
        pass


class RealScopedClass(AbstractScopedClass):
    def method(self):
        pass


def test_single_instance_normal():
    """Does this really make just one copy"""

    def scope_1():
        v1 = BasicClass()
        v2 = BasicClass()

        assert v1.value == 0
        assert v2.value == 0

        v2.value = 1

        assert v1.value == 1

        del v1
        del v2

        v3 = BasicClass()

        assert v3.value == 1

        v3.value = 2
        del v3

    scope_1()

    v4 = BasicClass()
    assert v4.value == 2

    del v4


def test_single_instance_threading_lock():
    """Test threading lock really does what it should"""

    def make_class(barrier):
        thread_id = barrier.wait()
        v1 = BasicClass()

        if thread_id == 0:
            v1.value = 1

        barrier.wait()

        assert v1.value == 1

        del v1

    barrier = threading.Barrier(15, timeout=3)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        threads = []
        for _i in range(15):
            threads.append(executor.submit(make_class, barrier))

        for future in concurrent.futures.as_completed(threads):
            if isinstance(future.exception(), Exception):
                raise future.exception()


def test_single_instance_abstract():
    """Does this really make just one copy"""

    with pytest.raises(TypeError):
        AbstractClass()

    def scope_1():
        v1 = RealClass()
        v2 = RealClass()

        v1.method()

        assert v1.value == 0
        assert v2.value == 0

        v2.value = 1

        assert v1.value == 1

        del v1
        del v2

        v3 = RealClass()

        assert v3.value == 1

        v3.value = 2
        del v3

    scope_1()

    v4 = RealClass()
    assert v4.value == 2

    del v4


def test_single_scoped_instance_normal():
    """Does this really make just one copy in scope"""

    def scope_1():
        v1 = BasicScopedClass()
        v2 = BasicScopedClass()

        assert v1.value == 0
        assert v2.value == 0

        v2.value = 1

        assert v1.value == 1

        del v1
        del v2

        v3 = BasicScopedClass()

        assert v3.value == 0

        v3.value = 1
        del v3

    scope_1()

    v4 = BasicScopedClass()
    assert v4.value == 0


def test_single_scoped_instance_abstract():
    """Does this really make just one copy in scope"""

    with pytest.raises(TypeError):
        AbstractScopedClass()

    def scope_1():
        v1 = RealScopedClass()
        v2 = RealScopedClass()

        assert v1.value == 0
        assert v2.value == 0

        v2.value = 1

        assert v1.value == 1

        del v1
        del v2

        v3 = RealScopedClass()

        assert v3.value == 0

        v3.value = 1
        del v3

    scope_1()

    v4 = RealScopedClass()
    assert v4.value == 0
