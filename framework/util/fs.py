import os
from pathlib import Path

def files_with_extensions(dir_path, *extensions):
    '''
    Return all files in dir_path that match the provided extensions.

    If no extensions are given, then all files in dir_path are returned.
    '''
    p = Path(dir_path)
    files = []
    if len(extensions) == 0:
        extensions = ('')

    name_to_path = []
    for entry in p.iterdir():
        if not entry.is_file():
            continue
        if not entry.name.endswith(extensions):
            continue
        channel_name = os.path.splitext(entry.name)[0]
        name_to_path.append([channel_name, str(entry)])
    return name_to_path
