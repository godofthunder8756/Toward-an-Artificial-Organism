"""Preserve all earlier scientific and governance artifacts during shared4 work."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def inventory():
    paths = list(ROOT.glob("R10A_*_v1.md"))
    paths += [ROOT / name for name in (
        "R9_FUNCTION_CLASS_v1.md", "PHASE3B_VERDICT_v1.md",
        "PHASE3B_R10_CERTIFICATION_v1.md", "ACI_RESEARCH_CONSTITUTION_v1.md",
        "ACI_ARCHITECTURAL_PRINCIPLES_v1.md")]
    for name in ("phase3b", "phase3b_results_v1", "phase3b_r10_v1", "r10a_v1"):
        paths += [p for p in (ROOT / name).rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main(path, check):
    now = inventory()
    if check:
        before = json.loads(path.read_text())
        if before["sha256"] != now:
            raise AssertionError("earlier scientific/governance artifacts changed")
        print("Preserved", len(now), "earlier files")
    else:
        head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
        with path.open("x", encoding="utf-8") as stream:
            json.dump({"head": head, "sha256": now}, stream, sort_keys=True, indent=2)
            stream.write("\n")
        print("Recorded", len(now), "earlier files at", head)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    main(args.path, args.check)
