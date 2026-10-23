"""Hash check: frozen files and original outputs are unchanged.

Reads bytes and compares SHA256 digests. Does not import wrel.
Does not run a solver, planner, item, or replay.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MANIFEST_SHA256 = "d1975600213fe4fd7fe11dc1de3f2c64a5b57207c7e1439444c6a9630dd45daf"

# Freeze-run outputs and the existing D1 outputs. These files are not rewritten
# by the errata.
OUTPUT_SHA256 = {
    "outputs/ITEM-1.json": "39e739b1abd8614113d7e266f9e38aff32da50f2e52e1e9b8469566ae3777d3a",
    "outputs/ITEM-2.json": "4ac58ac8ab74b837ce97def6d1869be0f07b525a868680d30d32a9823b78e999",
    "outputs/ITEM-3.json": "9f65f641917d835162d1e9b592c7a98f1b1bea8f23a5633664e66eac1a19395d",
    "outputs/ITEM-4.json": "8509c16c6da0547aba8b4e9008107926ef37528cc4974b9662833aaaa2400faa",
    "outputs/ITEM-5.json": "e62924e29d36709d8870f9674bbe6b1959e36f1eeafb6bfe77d21058d3850b05",
    "outputs/ITEM-6.json": "91ce46223299557be8d9f97b21d121b8387dff2c3017f24ec1d0963baa995c6a",
    "outputs/ITEM-7.json": "77e77207fcf516dcc759c104c5d2a3edd778bfbea5d11ffe28d8cdc354a0e0a9",
    "outputs/ITEM-8.json": "9d5148e692f48f533acb42dba8e730a54277580af375eb1287694b662d81c51b",
    "outputs/ITEM-9.json": "dfe1899729dd4b4a73683064cfa2723a482f441540c0f1c1ea58a2caaed31950",
    "outputs/SUMMARY.json": "3b4a69b3c0ee35d5cd70b6d368562d1fccd79603c91158e4177475861feddac1",
    "outputs/deviation_1/ITEM-8.json": "5c1e8200cc8063a8bcf01b2e11f362cb2bc43dd55df543f7f323d0229680c103",
    "outputs/deviation_1/ITEM-9.json": "ff8ec5a1db225f908025b594cd7940db1d33c6a30ed4d21e8c98b6ace82bfbd3",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_manifest() -> list[str]:
    errors = []
    manifest = ROOT / "IMPLEMENTATION_MANIFEST.md"
    got = sha256(manifest)
    if got != MANIFEST_SHA256:
        errors.append(f"IMPLEMENTATION_MANIFEST.md {got} != {MANIFEST_SHA256}")
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.startswith("SHA256 "):
            continue
        _tag, rel, expected = line.split()
        got = sha256(ROOT / rel)
        if got != expected:
            errors.append(f"frozen {rel} {got} != {expected}")
    return errors


def check_outputs() -> list[str]:
    errors = []
    for rel, expected in OUTPUT_SHA256.items():
        got = sha256(ROOT / rel)
        if got != expected:
            errors.append(f"output {rel} {got} != {expected}")
    return errors


def test_frozen_files_unchanged() -> None:
    errors = check_manifest()
    assert errors == [], errors


def test_original_outputs_unchanged() -> None:
    errors = check_outputs()
    assert errors == [], errors


def main() -> int:
    errors = check_manifest() + check_outputs()
    if errors:
        print("HASH CHECK FAILED")
        for item in errors:
            print(item)
        return 1
    n_frozen = sum(
        1
        for line in (ROOT / "IMPLEMENTATION_MANIFEST.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("SHA256 ")
    )
    print(
        f"HASH CHECK OK frozen_lines={n_frozen} manifest=1 outputs={len(OUTPUT_SHA256)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
