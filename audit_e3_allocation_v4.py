"""Pre-freeze audit of e3_fep_engineering_seed_v4.py. Prints invariants only.

A. v4 reproduces v3 exactly (every row field) for all v3 policies.
B. v4 depth_first reproduces explore_e3_ceiling_search.deepest_then_stale
   exactly (repair decisions and recall), so the confirmatory candidate is the
   explored scheduler.
C. Truth relabelling leaves every truth-blind v4 policy's repair decisions
   unchanged and changes truth_oracle's.
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v3 as v3
import e3_fep_engineering_seed_v4 as v4
import explore_e3_ceiling_search as search

OUT = Path("e3_fep_seed_results/v4/audit_v4.json")


def _same(a, b) -> bool:
    if isinstance(a, float) and isinstance(b, float) and np.isnan(a) and np.isnan(b):
        return True
    return a == b


def check_v3_equivalence(seeds=(0, 1), ticks=1500) -> dict:
    mismatches, compared = [], 0
    for cfg in ((9, 0.02, 3), (7, 0.03, 4)):
        p3 = replace(v3.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2], ticks=ticks)
        p4 = replace(v4.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2], ticks=ticks)
        for seed in seeds:
            e3env, e4env = v3.generate_environment(seed, p3), v4.generate_environment(seed, p4)
            for pol in v3.POLICIES:
                a, b = v3.run_one(pol, seed, p3, env=e3env), v4.run_one(pol, seed, p4, env=e4env)
                compared += 1
                mismatches += [{"cfg": cfg, "seed": seed, "policy": pol, "field": k}
                               for k in a if not _same(a[k], b[k])]
    return {"runs_compared": compared, "exact_match": not mismatches, "mismatches": mismatches[:20]}


def check_explored_scheduler(seeds=(8, 9), ticks=6000) -> dict:
    checks = []
    for cfg in ((9, 0.02, 3), (9, 0.03, 4)):
        p3 = replace(v3.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2], ticks=ticks)
        p4 = replace(v4.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2], ticks=ticks)
        for seed in seeds:
            explored = search.simulate("deepest_then_stale", seed, p3, v3.generate_environment(seed, p3))
            mine = v4.run_one("depth_first", seed, p4)
            checks.append({"cfg": cfg, "seed": seed,
                           "digest_match": explored["repair_digest"] == mine["repair_digest"],
                           "accuracy_match": explored["overall_accuracy"] == mine["overall_accuracy"]})
    return {"all_match": all(c["digest_match"] and c["accuracy_match"] for c in checks), "checks": checks}


def check_truth_leak(seeds=(0, 1), ticks=1500) -> dict:
    p4 = replace(v4.Params(), trace_bits=9, corrupt_p=0.02, budget=3, ticks=ticks)
    mask = np.zeros(p4.n_cues, dtype=bool)
    mask[1::2] = True
    same = {}
    for seed in seeds:
        env = v4.generate_environment(seed, p4)
        for pol in v4.POLICIES:
            a = v4.run_one(pol, seed, p4, env=env)["repair_digest"]
            b = v4.run_one(pol, seed, p4, relabel=mask, env=env)["repair_digest"]
            same.setdefault(pol, []).append(a == b)
    return {"truth_blind_invariant": all(all(v) for k, v in same.items() if k != "truth_oracle"),
            "truth_oracle_detected": not all(same["truth_oracle"]), "by_policy": same}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    result = {"A_v3_equivalence": check_v3_equivalence(),
              "B_explored_scheduler_identity": check_explored_scheduler(),
              "C_truth_leak": check_truth_leak()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    a, b, c = result.values()
    print(f"A. v4 == v3 on all v3 policies: {a['exact_match']} ({a['runs_compared']} runs) {a['mismatches'][:3]}")
    print(f"B. depth_first == explored deepest_then_stale: {b['all_match']}")
    print(f"C. truth-blind invariant: {c['truth_blind_invariant']}; truth_oracle detected: {c['truth_oracle_detected']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
