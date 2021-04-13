import os
import logging
from pathlib import Path

def files_with_extensions(dir_path, *extensions):
    '''
    Return all files in dir_path that match the provided extensions.

    If no extensions are given, then all files in dir_path are returned.

    Results are sorted by channel name to ensure stable output.
    '''
    logging.getLogger("decision_engine").debug("files_with_extensions called")
    logging.getLogger("decision_engine").debug("dir_path is %s!", dir_path)

    if len(extensions) == 0:
        extensions = ('')
        logging.getLogger("decision_engine").info("file extensions have zero length")

    name_to_path = []

    try:
        for entry in Path(dir_path).iterdir():
            if not entry.is_file():
                continue
            if entry.name.endswith(extensions):
                channel_name = os.path.splitext(entry.name)[0]
                name_to_path.append([channel_name, str(entry)])
    except FileNotFoundError:
        logging.getLogger("decision_engine").exception("invalid path to config file given")
        raise
    except Exception:  # pragma: no cover
        logging.getLogger("decision_engine").exception("Unexpected error!")
        raise
    else:
        return tuple(sorted(name_to_path, key=lambda x: x[0]))
