"""Audit the frozen AC9 controls v3 result table without rerunning it."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent
RESULT = ROOT / "ac9_controls_results_v3" / "results.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_ledger(row):
    # All phases start with 128 material, 24 core particles, and 40 boundary
    # particles. Memory construction is represented in memory_bound and
    # memory_writes; the ledger equation tracks every material destination.
    l = row["ledger"]
    inv = row["final_inventory"]
    m0 = 128 + 24 + 40 + l["in_m"]
    m1 = inv[1] + 4 * inv[3] + 2 * inv[4] + sum(row["demand"])
    spent = l["writes"] - l["memory_writes"]
    losses = (l["memory_waste"] + l["memory_expiry"] +
              4 * (l["particle_expiry"] + l["particle_export"]) +
              2 * (l["B_expiry"] + l["B_discard"]) + l["overflow_m"])
    assert m0 == m1 + spent + losses, (row["seed"], row["history"], m0, m1, spent, losses)
    assert 64 + 8 * l["converted"] == inv[0] + l["spent_e"]
    assert 32 + l["in_f"] == inv[2] + l["overflow_f"] + l["converted"]


def main():
    data = json.loads(RESULT.read_text())
    rows = data["rows"]
    assert len(rows) == 64 and len({(r["seed"], r["history"], r["arm"]) for r in rows}) == 64
    for row in rows:
        check_ledger(row)
        assert 0 <= row["assay"]["active"] <= 1536
        assert row["assay"]["productive"] <= row["assay"]["contacts"]
    files = data.get("source_hashes", {})
    for name, digest in files.items():
        assert sha256(ROOT / name) == digest, name
    print(f"AC9 controls v3 audit passed: {len(rows)} rows, ledgers and source hashes valid")


if __name__ == "__main__":
    main()
