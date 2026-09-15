"""Same-author audit of the AC3 engineering data and exact model replays."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import ac3


def main():
    path = Path("ac3_results_v1/results.json")
    data = json.loads(path.read_text())
    snapshot = json.loads(Path("ac3_results_v1/pre_run_snapshot.json").read_text())
    assert data["source_hashes"] == snapshot["source_hashes"]
    for name, digest in data["source_hashes"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    total, replays, turnover = 0, [], []
    for ci, entry in enumerate(data["configs"]):
        c = ac3.Config(**entry["config"])
        rows = entry["rows"]
        expected = {(s, a) for s in data["seeds"] for a in ac3.ARMS}
        assert len(rows) == len(expected)
        assert {(r["seed"], r["arm"]) for r in rows} == expected
        for seed in data["seeds"]:
            assert len({r["env_digest"] for r in rows if r["seed"] == seed}) == 1
        for r in rows:
            e = r["ledger"]
            assert e["in_e"] == e["clamp_m"] == e["external_births"] == 0
            assert c.energy_start + e["clamp_e"] + c.fuel_yield * e["converted"] == r["final_energy"] + e["living_e"] + e["write_e"] + e["synthesis_e"] + e["C_synthesis_e"] + e["overflow_e"]
            assert c.fuel_start + e["in_f"] == r["final_fuel"] + e["converted"] + e["overflow_f"]
            assert c.material_start + 12 * c.catalyst_material + 3 * c.converter_material + e["in_m"] + c.converter_material * e["external_C"] == r["final_material"] + c.catalyst_material * r["final_W"] + c.converter_material * r["final_C"] + e["write_m"] + c.catalyst_material * e["expired"] + c.converter_material * e["C_expired"] + e["overflow_m"]
            assert r["final_W"] == 12 + e["births"] - e["expired"]
            assert r["final_C"] == 3 + e["C_births"] + e["external_C"] - e["C_expired"]
            assert e["births"] * c.catalyst_material == e["synthesis_m"]
            assert e["births"] * c.catalyst_energy == e["synthesis_e"]
            assert e["C_births"] * c.converter_material == e["C_synthesis_m"]
            assert e["C_births"] * c.converter_energy == e["C_synthesis_e"]
            assert e["write_e"] == e["write_m"] == e["writes"] == sum(r["bank_writes"])
            assert r["active_fraction"] == e["active"] / c.ticks
            assert r["completed"] == (e["active"] == c.ticks)
            for key, cap in (("final_energy", c.energy_cap), ("final_material", c.material_cap), ("final_fuel", c.fuel_cap)):
                assert 0 <= r[key] <= cap
            if r["arm"].startswith("no_C"):
                assert e["C_births"] == 0
            if r["arm"].startswith("no_W"):
                assert e["births"] == 0
            if r["arm"] == "no_policy_write":
                assert r["bank_writes"][:2] == [0, 0]
            if r["arm"] != "no_C_rescue":
                assert e["external_C"] == 0
            if r["arm"] not in ("no_C_energy", "self_energy", "no_W_energy"):
                assert e["clamp_e"] == 0
        for a, metrics in entry["means"].items():
            for key, mean in metrics.items():
                assert abs(np.mean([r[key] for r in rows if r["arm"] == a]) - mean) < 1e-12
        for a, b, k in ac3.PAIRS:
            assert entry["contrasts"][a + "-" + b] == ac3.contrast(
                [r[k] for r in rows if r["arm"] == a], [r[k] for r in rows if r["arm"] == b])
        seed = data["seeds"][0]
        inputs = ac3.world(seed, c)
        for arm in ac3.ARMS:
            actual = ac3.run_one(seed, c, arm, inputs)
            original = next(r for r in rows if r["seed"] == seed and r["arm"] == arm)
            assert actual == original
            replays.append(dict(config=ci, seed=seed, arm=arm, exact=True))
        turnover.append(dict(p=c.flip_p, self=[dict(seed=r["seed"], W_births=r["ledger"]["births"],
            C_births=r["ledger"]["C_births"], converted=r["ledger"]["converted"])
            for r in rows if r["arm"] == "self"]))
        total += len(rows)
    tests = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", "test_ac3"], text=True, capture_output=True)
    assert tests.returncode == 0, tests.stdout + tests.stderr
    report = dict(ok=True, rows=total, source_snapshots_match=True, coverage_and_pairing=True,
        all_material_fuel_energy_balances=True, means_and_intervals_recomputed=True,
        result_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), exact_replays=replays,
        turnover=turnover, tests=tests.stdout + tests.stderr,
        limits="Engineering only; same-author audit; no independent review, boundary, or autonomous acquisition of needs.")
    with Path("AC3_AUDIT_v1.json").open("x", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(dict(ok=True, rows=total, exact_replays=len(replays), mechanism_tests=8)))


if __name__ == "__main__":
    main()
