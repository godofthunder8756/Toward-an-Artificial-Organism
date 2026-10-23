"""Hash check for the E30 close-out.

Reads bytes and compares SHA256 digests. Does not import wrel.
Does not run a solver, planner, item, or replay.
Does not write a study output. Prints the result on stdout.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent

MANIFESTS = (
    "IMPLEMENTATION_MANIFEST.md",
    "ADDENDUM_A2_MANIFEST.md",
    "ADDENDUM_A3_MANIFEST.md",
    "ADDENDUM_A3_D1_MANIFEST.md",
    "ADDENDUM_A3_D2_MANIFEST.md",
    "RESULTS_A2_errata_E29_MANIFEST.md",
    "VERIFICATION_A1_MANIFEST.md",
)

# Output ledgers written by earlier runs. Each line is "SHA256 <rel> <digest>"
# with rel already including the outputs/ directory, or a bare name inside the
# ledger's directory. HASHES.txt files use paths relative to the study root
# except where the line itself contains outputs/.
HASH_LEDGERS = (
    "outputs/attainability_A2/HASHES.txt",
    "outputs/attainability_A3/HASHES.txt",
    "outputs/attainability_A3_D1/HASHES.txt",
    "outputs/attainability_A3_D2/HASHES.txt",
)

# Primary and repair commits whose stored bytes must still match the worktree.
GIT_PINS = (
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "RESULTS_A3.md"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/smoke.json"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/PM.json"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/TSEP-3.json"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/TSEP-4.json"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/SUMMARY.json"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/HASHES.txt"),
    ("7e153d1648dfa5babe080b028a0c1609682c5a69", "outputs/attainability_A3/RESULTS_A3.sha256"),
    ("0c5b308d001ca55402b012cce6655ce9e2317288", "outputs/attainability_A3_D1/SUMMARY.json"),
    ("0c5b308d001ca55402b012cce6655ce9e2317288", "RESULTS_A3_D1.md"),
    ("1f2a6c9", "outputs/attainability_A3_D2/SUMMARY.json"),
    ("1f2a6c9", "RESULTS_A3_D2.md"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_manifest(name: str) -> tuple[int, list[str]]:
    errors = []
    count = 0
    text = (ROOT / name).read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip().strip("`")
        if not stripped.startswith("SHA256 "):
            continue
        parts = stripped.split()
        if len(parts) != 3:
            errors.append(f"{name}: unparsed {line!r}")
            continue
        _tag, rel, expected = parts
        rel = rel.strip("`")
        expected = expected.strip("`")
        count += 1
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing {rel} listed by {name}")
            continue
        got = sha256(path)
        if got != expected:
            errors.append(f"{name} {rel} {got} != {expected}")
    if name != "VERIFICATION_A1_MANIFEST.md" and name != "IMPLEMENTATION_MANIFEST.md":
        declared = None
        for line in text.splitlines():
            if line.startswith("FILE_COUNT "):
                declared = int(line.split()[1])
        if declared is not None and declared != count:
            errors.append(f"{name} FILE_COUNT {declared} != {count}")
    return count, errors


def resolve_ledger_path(ledger: str, rel: str) -> Path:
    if rel.startswith("outputs/"):
        return ROOT / rel
    parent = (ROOT / ledger).parent
    return parent / rel


def check_ledgers() -> tuple[int, list[str]]:
    errors = []
    count = 0
    for ledger in HASH_LEDGERS:
        for line in (ROOT / ledger).read_text(encoding="utf-8").splitlines():
            if not line.startswith("SHA256 "):
                continue
            _tag, rel, expected = line.split()
            count += 1
            path = resolve_ledger_path(ledger, rel)
            if not path.is_file():
                errors.append(f"ledger {ledger} missing {rel}")
                continue
            got = sha256(path)
            if got != expected:
                errors.append(f"ledger {ledger} {rel} {got} != {expected}")
    return count, errors


def check_git_pins() -> tuple[int, list[str]]:
    errors = []
    for commit, rel in GIT_PINS:
        blob = subprocess.check_output(
            ["git", "show", f"{commit}:c4_reliability_exact_check_v1/{rel}"],
            cwd=str(REPO),
        )
        got = hashlib.sha256(blob).hexdigest()
        working = sha256(ROOT / rel)
        if got != working:
            errors.append(f"git {commit} {rel} worktree {working} != commit {got}")
    return len(GIT_PINS), errors


def main() -> int:
    errors = []
    n_manifest = 0
    for name in MANIFESTS:
        count, found = check_manifest(name)
        n_manifest += count
        errors.extend(found)
        print(f"manifest {name} lines={count} errors={len(found)}")
    n_ledger, found = check_ledgers()
    errors.extend(found)
    print(f"hash ledgers lines={n_ledger} errors={len(found)}")
    n_git, found = check_git_pins()
    errors.extend(found)
    print(f"git pins={n_git} errors={len(found)}")
    if errors:
        print("HASH CHECK FAILED")
        for item in errors:
            print(item)
        return 1
    print(
        f"HASH CHECK OK manifest_lines={n_manifest} ledger_lines={n_ledger} git_pins={n_git}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
