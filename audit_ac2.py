"""Audit AC2 evidence without modifying source snapshots or result rows."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import ac2


def main():
    result_file = Path("ac2_results_v1/results.json")
    data = json.loads(result_file.read_text())
    snapshot = json.loads(Path("ac2_results_v1/pre_run_snapshot.json").read_text())
    assert data["source_hashes"] == snapshot["source_hashes"]
    for name, digest in data["source_hashes"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    total = 0
    replays = []
    counts = []
    for ci, entry in enumerate(data["configs"]):
        c = ac2.Config(**entry["config"])
        rows = entry["rows"]
        pairs = {(seed, arm) for seed in data["seeds"] for arm in ac2.ARMS}
        assert len(rows) == len(pairs)
        assert {(r["seed"], r["arm"]) for r in rows} == pairs
        for seed in data["seeds"]:
            assert len({r["env_digest"] for r in rows if r["seed"] == seed}) == 1
        for row in rows:
            e = row["ledger"]
            assert c.energy_start + e["in_e"] + e["clamp_e"] == row["final_energy"] + e["living_e"] + e["write_e"] + e["synthesis_e"] + e["overflow_e"]
            assert c.material_start + 12 * c.catalyst_material + e["in_m"] + e["clamp_m"] + c.catalyst_material * e["external_births"] == row["final_material"] + c.catalyst_material * row["final_catalysts"] + e["write_m"] + c.catalyst_material * e["expired"] + e["overflow_m"]
            assert row["final_catalysts"] == 12 + e["births"] + e["external_births"] - e["expired"]
            assert e["births"] * c.catalyst_material == e["synthesis_m"]
            assert e["births"] * c.catalyst_energy == e["synthesis_e"]
            assert e["write_e"] == e["write_m"] == e["writes"] == sum(row["bank_writes"])
            assert row["active_fraction"] == e["active"] / c.ticks
            assert 0 <= row["final_energy"] <= c.energy_cap
            assert 0 <= row["final_material"] <= c.material_cap
            if row["arm"].startswith("no_synthesis"):
                assert e["births"] == 0
            if row["arm"] == "no_policy_write":
                assert row["bank_writes"][:2] == [0, 0]
            if row["arm"] != "no_synthesis_rescue":
                assert e["external_births"] == 0
        for arm, metrics in entry["means"].items():
            for key, mean in metrics.items():
                assert abs(np.mean([r[key] for r in rows if r["arm"] == arm]) - mean) < 1e-12
        for a, b, metric in (("self", "no_synthesis", "active_fraction"),
                             ("self", "no_policy_write", "active_fraction"),
                             ("no_synthesis_rescue", "no_synthesis", "active_fraction"),
                             ("self_clamp", "no_synthesis_clamp", "policy_accuracy")):
            expected = ac2.contrast([r[metric] for r in rows if r["arm"] == a],
                                    [r[metric] for r in rows if r["arm"] == b])
            assert entry["contrasts"][a + "-" + b] == expected
        # First seed, every arm and environment. Technical validation, not new n.
        seed = data["seeds"][0]
        inputs = ac2.world(seed, c)
        for arm in ac2.ARMS:
            actual = ac2.run_one(seed, c, arm, inputs)
            expected = next(r for r in rows if r["seed"] == seed and r["arm"] == arm)
            assert actual == expected
            replays.append(dict(config=ci, seed=seed, arm=arm, exact=True))
        total += len(rows)
        counts.append(dict(p=c.flip_p, self_births=[r["ledger"]["births"] for r in rows if r["arm"] == "self"],
                           self_expiries=[r["ledger"]["expired"] for r in rows if r["arm"] == "self"]))
    tests = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", "test_ac2"], capture_output=True, text=True)
    assert tests.returncode == 0, tests.stdout + tests.stderr
    report = dict(ok=True, rows=total, result_sha256=hashlib.sha256(result_file.read_bytes()).hexdigest(),
        source_snapshots_match=True, coverage_and_pairing=True,
        full_energy_and_material_balances=True, means_and_intervals_recomputed=True,
        exact_replays=replays, turnover_counts=counts, tests=tests.stdout + tests.stderr,
        limits="Same-author audit of a trusted model. No independent review, molecular validation, converter, boundary, or autonomous acquisition.")
    with Path("AC2_AUDIT_v1.json").open("x", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(dict(ok=True, rows=total, exact_replays=len(replays), mechanism_tests=7)))


if __name__ == "__main__":
    main()
