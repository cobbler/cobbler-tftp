"""
Various utility functions for cobbler-tftp
"""

from pathlib import Path
from typing import List, Optional, Tuple

try:
    from importlib.abc import Traversable
except ImportError:
    from importlib_resources.abc import Traversable


def copy_file(
    src_dir: Traversable,
    dst_dir: Path,
    name: str,
    patch: Optional[List[Tuple[str, str]]] = None,
):
    """
    Copy a file to a different directory, preserving the name and
    possibly replacing strings in it.

    :param src_dir: Directory that contains the file to copy.
    :param dst_dir: Directory to copy the file into.
    :param name: Name of the file (in both directories).
    :param patch: List of (old, new) strings to replace in the file.
    """
    src = src_dir / name
    dst = dst_dir / name
    contents: bytes = src.read_bytes()  # type: ignore
    if patch is not None:
        for old, new in patch:
            contents = contents.replace(old.encode("UTF-8"), new.encode("UTF-8"))
    dst.write_bytes(contents)
