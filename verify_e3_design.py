"""Read-only integrity audit of an engineering-only E3 design manifest.

verify(root, manifest) returns a JSON-compatible result, never writes files,
and never repairs a manifest. The default CLI audits this module's workspace;
--root and --manifest allow isolated fixtures. stdout is one JSON result and
exit status is 0 for pass, 1 for failure (including CLI/JSON/schema errors).
There are no run, target-draw, source-freeze or implementation-conformance
permissions in a successful integrity check. Run with Python -B to suppress
interpreter bytecode writes. Use a quiescent tree; this is not an OS sandbox
against concurrent adversarial filesystem replacement.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import NoReturn, Sequence


DEFAULT_MANIFEST = "E3_DESIGN_FREEZE_v0_11.json"
ENGINEERING_KIND = "engineering_only_design_freeze"
_FLAGS = {
    "external_preregistration": False,
    "implementation_present_at_snapshot": False,
    "engineering_execution_requires_implementation_validation": True,
    "final_target_draws_permitted": False,
    "confirmatory_h2_permitted": False,
}


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"nonstandard JSON constant: {value}")


def _reject_link(path: Path) -> os.stat_result:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or (
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    ):
        raise ValueError(f"symlink or reparse point is not permitted: {path.name}")
    return info


def _safe_file(root: Path, name: str) -> Path:
    if type(name) is not str or not name:
        raise ValueError("file path must be a nonempty relative string")
    # Require canonical portable relative names, not drive/UNC/ADS aliases.
    if any(character in name for character in ("\\", ":", "\x00")):
        raise ValueError(f"noncanonical file path: {name!r}")
    parts = name.split("/")
    if any(part in ("", ".", "..") or part.endswith((" ", ".")) for part in parts):
        raise ValueError(f"unsafe file path: {name!r}")
    path = root
    for index, part in enumerate(parts):
        path = path / part
        info = _reject_link(path)
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"non-directory path component: {name!r}")
    if not stat.S_ISREG(info.st_mode):
        raise ValueError(f"not a regular file: {name!r}")
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError(f"file escapes workspace: {name!r}")
    return resolved


def _result(failures: list[str], count: int = 0, checked: int = 0) -> dict[str, object]:
    return {
        "ok": not failures,
        "kind": ENGINEERING_KIND,
        "file_count": count,
        "files_checked": checked,
        "failures": failures,
    }


def verify(
    root: str | Path | None = None,
    manifest: str | Path = DEFAULT_MANIFEST,
) -> dict[str, object]:
    """Verify every entry of a nonempty manifest; entry count is not hard-coded.

    Manifest and file paths must stay inside root without symlinks/junctions.
    JSON duplicates at every depth, non-JSON constants, noncanonical paths,
    non-bool permissions, non-int sizes and non-lowercase SHA256 are failures.
    Errors are returned, not raised; no output sidecar or correction is made.
    """
    failures: list[str] = []
    count = checked = 0
    try:
        base = Path(__file__).absolute().parent if root is None else Path(root).absolute()
        # Do not silently resolve a symlink supplied as the workspace or parent.
        for parent in reversed((base, *base.parents)):
            _reject_link(parent)
        base = base.resolve(strict=True)
        if not base.is_dir():
            raise ValueError("workspace root must be a directory")
        manifest_name = os.fspath(manifest)
        if Path(manifest_name).is_absolute():
            manifest_name = Path(manifest_name).relative_to(base).as_posix()
        elif isinstance(manifest, Path):
            manifest_name = manifest.as_posix()
        manifest_path = _safe_file(base, manifest_name)
        data = json.loads(
            manifest_path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_invalid_constant,
        )
        if type(data) is not dict:
            raise ValueError("manifest must be a JSON object")
        if data.get("kind") != ENGINEERING_KIND:
            failures.append(f"kind must be {ENGINEERING_KIND!r}")
        for key, expected in _FLAGS.items():
            if data.get(key) is not expected:
                failures.append(f"{key} must be the JSON boolean {str(expected).lower()}")
        entries = data.get("files")
        if type(entries) is not dict or not entries:
            raise ValueError("files must be a nonempty JSON object")
        count = len(entries)
        seen: set[str] = set()
        for name, entry in entries.items():
            try:
                if type(entry) is not dict or set(entry) != {"bytes", "sha256"}:
                    raise ValueError("entry must contain exactly bytes and sha256")
                size, digest = entry["bytes"], entry["sha256"]
                if type(size) is not int or size < 0:
                    raise ValueError("bytes must be a nonnegative JSON integer")
                if type(digest) is not str or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
                    raise ValueError("sha256 must contain exactly 64 lowercase hexadecimal digits")
                path = _safe_file(base, name)
                identity = os.path.normcase(str(path))
                if identity in seen:
                    raise ValueError("duplicate resolved file path")
                seen.add(identity)
                actual_size = 0
                actual_hash = hashlib.sha256()
                with path.open("rb") as source:
                    for chunk in iter(lambda: source.read(1024 * 1024), b""):
                        actual_size += len(chunk)
                        actual_hash.update(chunk)
                checked += 1
                if actual_size != size:
                    failures.append(f"{name}: bytes mismatch (expected {size}, found {actual_size})")
                if actual_hash.hexdigest() != digest:
                    failures.append(f"{name}: sha256 mismatch")
            except (OSError, ValueError, TypeError, RuntimeError) as error:
                failures.append(f"{name!r}: {error}")
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        failures.append(f"manifest: {error}")
    return _result(failures, count, checked)


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError(message)


def main(argv: Sequence[str] | None = None) -> int:
    """Print one JSON result, including on invalid arguments; never rewrite files."""
    parser = _Parser(add_help=False)
    parser.add_argument("--root")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    try:
        args = parser.parse_args(argv)
        result = verify(args.root, args.manifest)
    except (ValueError, TypeError) as error:
        result = _result([f"arguments: {error}"])
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())