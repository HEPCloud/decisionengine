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
        extensions = ['']

    for ext in list(extensions):
        files += p.glob('*' + ext)

    name_to_path = []
    for file in files:
        channel_name = os.path.splitext(file.name)[0]
        name_to_path.append([channel_name, str(file)])
    return name_to_path
