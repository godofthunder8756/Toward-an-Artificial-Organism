"""Snapshot and verify old scientific artifacts without modifying them."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def inventory() -> dict[str, str]:
    paths = [ROOT / "PHASE3B_VERDICT_v1.md", ROOT / "PHASE3B_R10_CERTIFICATION_v1.md"]
    for folder in ("phase3b", "phase3b_results_v1", "phase3b_r10_v1"):
        paths.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts)
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main(output: Path, check: bool) -> None:
    current = inventory()
    if check:
        recorded = json.loads(output.read_text(encoding="utf-8"))
        if current != recorded["sha256"]:
            raise AssertionError("old artifact inventory or bytes changed")
        print(f"Preserved {len(current)} scientific files")
    else:
        head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
        with output.open("x", encoding="utf-8") as stream:
            json.dump({"head": head, "sha256": current}, stream, sort_keys=True, indent=2)
            stream.write("\n")
        print(f"Recorded {len(current)} scientific files at {head}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    main(args.output, args.check)
