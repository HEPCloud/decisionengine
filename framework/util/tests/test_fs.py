import tempfile
from pathlib import Path

from decisionengine.framework.util import fs

def test_empty_directory():
    mydir = tempfile.TemporaryDirectory()
    files = fs.files_with_extensions(mydir.name)
    assert len(files) == 0

def test_nonempty_directory():
    mydir = tempfile.TemporaryDirectory()
    __a = Path(mydir.name, 'a.txt')
    __a.touch()
    files = fs.files_with_extensions(mydir.name)
    assert files == (['a', str(__a)], )

def test_nonempty_directory_with_extensions():
    mydir = tempfile.TemporaryDirectory()
    __a = Path(mydir.name, 'a.txt')
    __b = Path(mydir.name, 'b.jsonnet')
    __c = Path(mydir.name, 'c.conf')
    __a.touch()
    __b.touch()
    __c.touch()

    files = fs.files_with_extensions(mydir.name, '.jsonnet')
    assert files == (['b', str(__b)], )

    files = fs.files_with_extensions(mydir.name, '.jsonnet', '.conf')
    assert files == (['b', str(__b)], ['c', str(__c)])
