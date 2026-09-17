"""Read-only audit of the AC1-4 confirmatory study; writes a report, never data.

Re-derives coverage, means, contrasts and every gate from the saved table
without simulating, verifies source-hash drift, and checks rows.jsonl agreement.
Verification tools are hashed into the report only, never the frozen snapshot.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

import ac1_4_confirm as conf

ROOT = Path("ac1_4_confirm_results_v1")
ANALYZERS = {
    "ac1": conf.analyze_ac1,
    "ac2": conf.analyze_ac2,
    "ac3": conf.analyze_ac3,
    "ac4_short": conf.analyze_ac4_short,
    "ac4_long": conf.analyze_ac4_long,
}
ARMS = {
    "ac1": ("self", "no_policy_write", "free_policy_ablation", "protected"),
    "ac2": ("self", "no_synthesis", "no_synthesis_rescue", "protected",
            "self_clamp", "no_synthesis_clamp"),
    "ac3": ("self", "no_C", "no_C_rescue", "no_C_energy", "protected",
            "self_energy", "no_W_energy"),
    "ac4_short": ("self", "no_B", "no_B_rescue", "no_B_retention", "protected"),
    "ac4_long": ("self", "no_policy_write", "protected", "no_B_retention"),
}


def main():
    snapshot = json.loads((ROOT / "pre_run_snapshot.json").read_text())
    results = json.loads((ROOT / "results.json").read_text())
    assert results["kind"] == "confirmatory_v1"
    assert results["seeds"] == conf.SEEDS

    # Source-hash drift check on the frozen set (protocol + runner + frozen deps).
    for name, digest in snapshot["source_hashes"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name

    # rows.jsonl must agree exactly with the aggregated rows.
    logged = [json.loads(line) for line in (ROOT / "rows.jsonl").read_text().splitlines()]
    stored = [r for study in results["studies"].values() for cfg in study for r in cfg["rows"]]
    assert logged == stored, "rows.jsonl disagrees with results.json rows"

    total_rows = 0
    for name, configs in results["studies"].items():
        analyzer = ANALYZERS[name]
        arms = ARMS[name]
        for cfg in configs:
            rows = cfg["rows"]
            # rectangular coverage: every (seed, arm) exactly once
            assert {(r["seed"], r["arm"]) for r in rows} == {(s, a) for s in conf.SEEDS[name] for a in arms}
            assert len(rows) == len(conf.SEEDS[name]) * len(arms)
            # re-derive means, contrasts, gates without simulating
            means, contrasts, gates = analyzer(rows)
            assert means == cfg["means"], (name, "means")
            assert contrasts == cfg["contrasts"], (name, "contrasts")
            assert gates == cfg["gates"], (name, "gates")
            # ledger sanity for every row
            for r in rows:
                assert 0.0 <= r.get("active_fraction", r.get("activity", -1)) <= 1.0
            total_rows += len(rows)

    tool_hashes = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                   for p in ("audit_ac1_4_confirm.py", "replay_ac1_4_confirm.py",
                             "test_ac1_4_confirm.py") if Path(p).exists()}

    report = dict(ok=True, kind="confirmatory_v1", rows=total_rows,
                  source_snapshots_match=True, rows_jsonl_agreement=True,
                  coverage=True, means_recomputed=True, contrasts_recomputed=True,
                  gates_recomputed=True,
                  verification_tool_hashes=tool_hashes,
                  limits="Same-author confirmatory audit; frozen physics reused unmodified; "
                         "no external preregistration or independent scientific review.")
    with (ROOT / "audit.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(dict(ok=True, rows=total_rows, gates_recomputed=True)))


if __name__ == "__main__":
    main()
