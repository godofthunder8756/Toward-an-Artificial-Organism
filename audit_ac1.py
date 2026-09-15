"""Read-only result/source audit; writes a separate report, never final data."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import ac1
import ac1_followup


def main():
    freeze = json.loads(Path("AC1_ENGINEERING_FREEZE_v1.json").read_text())
    for name, digest in freeze["files"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    follow = json.loads(Path("ac1_followup_results_v1/pre_run_snapshot.json").read_text())
    for name, digest in follow["source_hashes"].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    inventory = []
    replays = []
    for file in ("ac1_results_v1/results.json", "ac1_followup_results_v1/results.json"):
        data = json.loads(Path(file).read_text())
        total = 0
        for index, config in enumerate(data["configs"]):
            c = ac1.Config(**config["config"])
            rows = config["rows"]
            arms = sorted(config["means"])
            expected = {(s, a) for s in data["seeds"] for a in arms}
            assert {(r["seed"], r["arm"]) for r in rows} == expected
            assert len(rows) == len(expected)
            for seed in data["seeds"]:
                assert len({r["env_digest"] for r in rows if r["seed"] == seed}) == 1
            for row in rows:
                ledger = row["ledger"]
                assert row["final_energy"] == c.energy_start + ledger["in_e"] + ledger["rescue_e"] - ledger["spent_e"] - ledger["overflow_e"]
                assert row["final_material"] == c.material_start + ledger["in_m"] + ledger["rescue_m"] - ledger["spent_m"] - ledger["overflow_m"]
                assert sum(row["bank_writes"]) == ledger["writes"]
                if row["arm"] in ("no_policy_write", "free_policy_ablation"):
                    assert row["bank_writes"][:2] == [0, 0]
                assert row["active_fraction"] == ledger["active"] / c.ticks
                assert 0 <= row["final_energy"] <= c.energy_cap
                assert 0 <= row["final_material"] <= c.material_cap
            for arm, means in config["means"].items():
                for metric, value in means.items():
                    assert abs(np.mean([r[metric] for r in rows if r["arm"] == arm]) - value) < 1e-12
            for other, saved in config["paired_activity"].items():
                actual = ac1.contrast([r["active_fraction"] for r in rows if r["arm"] == "self"],
                                      [r["active_fraction"] for r in rows if r["arm"] == other])
                assert saved == actual
            # Declared audit sample: first seed, every environment, self and ablation.
            chosen = "free_policy_ablation" if "free_policy_ablation" in arms else "no_policy_write"
            seed = data["seeds"][0]
            inputs = ac1.world(seed, c)
            for arm in ("self", chosen):
                actual = ac1_followup.run_free(seed, c, inputs) if arm == "free_policy_ablation" else ac1.run_one(seed, c, arm, inputs)
                saved = next(r for r in rows if r["seed"] == seed and r["arm"] == arm)
                assert actual == saved
                replays.append(dict(file=file, config=index, seed=seed, arm=arm, exact=True))
            total += len(rows)
        inventory.append(dict(file=file, rows=total, sha256=hashlib.sha256(Path(file).read_bytes()).hexdigest()))
    tests = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", "test_ac1"], text=True, capture_output=True)
    assert tests.returncode == 0, tests.stdout + tests.stderr
    report = dict(ok=True, source_snapshots_match=True, inventories=inventory,
        seed_coverage=True, recorded_environment_pairing=True, resource_balances=True,
        means_and_bootstrap_intervals_recomputed=True, exact_replays=replays,
        mechanism_tests=tests.stdout + tests.stderr, followup_checks=ac1_followup.checks(),
        limits="Trusted in-process simulation; no full-runtime sandbox proof, external preregistration or independent scientific review.")
    with Path("AC1_AUDIT_v1.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(dict(ok=True, rows=sum(i["rows"] for i in inventory), exact_replays=len(replays), mechanism_tests=8)))


if __name__ == "__main__":
    main()
