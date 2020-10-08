from decisionengine.framework.util import fs

from pathlib import Path
import tempfile

def test_empty_directory():
    dir = tempfile.TemporaryDirectory()
    files = fs.files_with_extensions(dir.name)
    assert len(files) == 0

def test_nonempty_directory():
    dir = tempfile.TemporaryDirectory()
    a = Path(dir.name, 'a.txt')
    a.touch()
    files = fs.files_with_extensions(dir.name)
    assert files == (['a', str(a)])

def test_nonempty_directory_with_extensions():
    dir = tempfile.TemporaryDirectory()
    a = Path(dir.name, 'a.txt')
    b = Path(dir.name, 'b.jsonnet')
    c = Path(dir.name, 'c.conf')
    a.touch()
    b.touch()
    c.touch()

    files = fs.files_with_extensions(dir.name, '.jsonnet')
    assert files == (['b', str(b)])

    files = fs.files_with_extensions(dir.name, '.jsonnet', '.conf')
    assert files == (['b', str(b)], ['c', str(c)])
