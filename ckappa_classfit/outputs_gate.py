"""Refuse writes that would mix or overwrite class-fit outputs.

Stdlib only. __main__ imports this before NumPy. A symlink is detected with
os.lstat and is not followed. A refusal writes nothing.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

OUTPUT_DIR_NAME = "classfit_outputs"
POST_RUN_INDEX_NAME = "classfit_post_run_index.json"

_claimed: set[str] = set()


def _lstat(path: Path):
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def outputs_refusal(root: Path) -> str | None:
    """None when classfit_outputs is absent or an empty real directory inside root.

    A symlink, a non-directory, a path whose real location is outside root,
    and a non-empty directory are refused.
    """
    root = Path(root)
    path = root / OUTPUT_DIR_NAME
    info = _lstat(path)
    if info is None:
        return None
    if stat.S_ISLNK(info.st_mode):
        return "symlink"
    if not stat.S_ISDIR(info.st_mode):
        return "not_a_directory"
    real = path.resolve()
    root_real = root.resolve()
    expected = root_real / OUTPUT_DIR_NAME
    if real != expected:
        return "resolves_outside_root"
    try:
        real.relative_to(root_real)
    except ValueError:
        return "resolves_outside_root"
    with os.scandir(path) as entries:
        for _entry in entries:
            return "nonempty"
    return None


def index_refusal(root: Path) -> str | None:
    """None when classfit_post_run_index.json is absent.

    An existing file or a symlink is refused. The same run may create the
    index only after this check has passed.
    """
    path = Path(root) / POST_RUN_INDEX_NAME
    info = _lstat(path)
    if info is None:
        return None
    if stat.S_ISLNK(info.st_mode):
        return "symlink"
    return "exists"


def claim_output_dir(root: Path) -> str | None:
    """Return a refusal reason, or None once this process may write under root.

    The first success is remembered. Later writes in the same process are
    allowed after the directory has received this run's own files. A refusal
    does not remember the root and does not create anything.
    """
    key = str(Path(root).resolve())
    if key in _claimed:
        return None
    reason = outputs_refusal(root)
    if reason is not None:
        return reason
    reason = index_refusal(root)
    if reason is not None:
        return "post_run_index:" + reason
    _claimed.add(key)
    return None


def output_dir_state(root: Path) -> str:
    """absent, empty, or the refusal reason. Does not follow symlinks."""
    reason = outputs_refusal(root)
    if reason is not None:
        return reason
    path = Path(root) / OUTPUT_DIR_NAME
    if _lstat(path) is None:
        return "absent"
    return "empty"
