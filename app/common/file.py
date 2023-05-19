"Common file operations module"

from pathlib import Path


def get_files_by_type(dir_: str, ext: str) -> list:
    """Returns list of files with specific type in given dir.

    Args:
        dir_: root directory to search in
        ext: extension of files to be included will
        result in files such as: '*.ext'
    """
    return [p.resolve() for p in Path(dir_).rglob(f"*.{ext}")]
