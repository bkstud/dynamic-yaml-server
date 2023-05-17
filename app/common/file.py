"Common file operations module"

import shutil
from pathlib import Path
from typing import Callable, Union


def prepare_symlink_noext(src: Union[str, Path], dst: Union[str, Path]):
    """Prepares symlink from source to destination without extension."""
    Path(src).with_suffix("").symlink_to(Path(dst))


def get_files_by_type(dir_: str, ext: str) -> list:
    """Returns list of files with specific type in given dir.

    Args:
        dir_: root directory to search in
        ext: extension of files to be included will
        result in files such as: '*.ext'
    """
    return [p.resolve() for p in Path(dir_).rglob(f"*.{ext}")]


def prepare_source_structure_and_call_by_ext(source_dir: str,
                                             out_dir: str,
                                             *,
                                             ext: str,
                                             callable_: Callable):
    """Prepares source structure copy based on files found with given extension
       and calls given method for them.
    """
    file_paths = get_files_by_type(source_dir, ext)
    if not file_paths:
        return False

    source_dir = Path(source_dir).resolve()
    out_dir = Path(out_dir).resolve()

    if out_dir.exists():
        shutil.rmtree(out_dir)

    for fpath in file_paths:
        relpath = fpath.parent.relative_to(source_dir)
        cp_file_path = out_dir.joinpath(relpath, fpath.name)
        cp_file_path.parent.mkdir(parents=True, exist_ok=True)
        callable_(fpath, cp_file_path)

    return True


def prepare_linking_directory(source_dir: str,
                              out_dir: str,
                              *,
                              ext: str):
    """Prepares structural copy of out dir with links based on extension.

    The resulting directory will contain links to source_dir files
    that match _type but without _type in name of the file."""
    return prepare_source_structure_and_call_by_ext(
        source_dir=source_dir,
        out_dir=out_dir,
        ext=ext,
        callable_=prepare_symlink_noext
    )
