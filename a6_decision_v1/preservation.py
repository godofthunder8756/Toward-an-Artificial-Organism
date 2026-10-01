"""Additive inventory of every tracked input to the bounded A6 effort."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parent.parent
MUTABLE = ("README.md", ".vscode/kanban-agent.json")


def head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_once(path: Path, document: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(document, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def inventory() -> dict:
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True,
    )
    paths = sorted(p.decode("utf-8") for p in result.stdout.split(b"\0") if p)
    return {
        "schema": 1, "head": head(),
        "protected": {p: digest(ROOT.joinpath(*PurePosixPath(p).parts))
                      for p in paths if p not in MUTABLE},
        "navigation_before": {p: digest(ROOT.joinpath(*PurePosixPath(p).parts))
                              for p in paths if p in MUTABLE},
        "allowed_existing_edits": list(MUTABLE),
    }


def verify(document: dict) -> dict:
    if document["schema"] != 1 or document["allowed_existing_edits"] != list(MUTABLE):
        raise ValueError("unknown preservation contract")
    changed = [p for p, sha in document["protected"].items()
               if not ROOT.joinpath(*PurePosixPath(p).parts).is_file()
               or digest(ROOT.joinpath(*PurePosixPath(p).parts)) != sha]
    if changed:
        raise ValueError(f"protected inputs changed: {changed}")
    return {"preserved": len(document["protected"]), "starting_head": document["head"],
            "live_head": head(), "allowed_existing_edits": list(MUTABLE)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(verify(json.loads(args.path.read_text(encoding="utf-8")))))
    else:
        write_once(args.path, inventory())
        print("Recorded all tracked inputs:", args.path)
