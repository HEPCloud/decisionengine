# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import tempfile

from pathlib import Path

import pytest

from decisionengine.framework.util import fs


def test_non_real_directory():
    with pytest.raises(FileNotFoundError):
        fs.files_with_extensions("/this/dir/is/not/real")


def test_empty_directory():
    with tempfile.TemporaryDirectory() as mydir:
        files = fs.files_with_extensions(mydir)
        assert len(files) == 0


def test_nonempty_directory():
    with tempfile.TemporaryDirectory() as mydir:
        __a = Path(mydir, "a.txt")
        __a.touch()
        files = fs.files_with_extensions(mydir)
        assert files == (["a", str(__a)],)


def test_nonempty_directory_with_extensions():
    with tempfile.TemporaryDirectory() as mydir:
        __a = Path(mydir, "a.txt")
        __b = Path(mydir, "b.jsonnet")
        __c = Path(mydir, "c.conf")
        __d = Path(mydir, "somedir")
        __a.touch()
        __b.touch()
        __c.touch()
        __d.mkdir()

        files = fs.files_with_extensions(mydir, ".jsonnet")
        assert files == (["b", str(__b)],)

        files = fs.files_with_extensions(mydir, ".jsonnet", ".conf")
        assert files == (["b", str(__b)], ["c", str(__c)])
