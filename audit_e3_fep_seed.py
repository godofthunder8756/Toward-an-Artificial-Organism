"""Audit of the E3 binary-trace maintenance toy (engineering seed only).

A. Refactor equivalence: v2 in --legacy-shared-rng mode must reproduce v1
   (e3_fep_engineering_seed.py) exactly, so v2 inherits v1's audited rules.
B. Random-stream pairing: do environment events (relevance, queries, corruption
   masks) stay identical across policies for one seed? Checked for v1's shared
   stream (via legacy mode) and v2's split streams.
C. Repair in isolation: every bit pattern of every width 3..8 and both truth
   values, repaired to a fixed point by v2's own repair_one_bit with no further
   damage. The evaluator knows truth; the repair function never receives it.

Writes one JSON file and refuses to overwrite it.
"""

from __future__ import annotations

import itertools
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed as v1
import e3_fep_engineering_seed_v2 as v2

OUT = Path("e3_fep_seed_results/v2/audit.json")


def check_equivalence(ticks: int = 800, seeds: range = range(3)) -> dict:
    v1.TICKS = ticks
    p = replace(v2.Params(), ticks=ticks, legacy_shared_rng=True)
    fields = [("overall_accuracy", "overall_accuracy"), ("post_return_accuracy", "post_return_accuracy"),
              ("post_return_n", "post_return_n"), ("steady_accuracy", "steady_accuracy"),
              ("steady_n", "steady_n"), ("scrubs_spent", "scrubs")]
    mismatches = []
    compared = 0
    for seed in seeds:
        for policy in ("random", "uniform", "recency", "precision"):
            a = v1.run_one(policy, seed)
            b = v2.run_one(policy, seed, p)
            compared += 1
            for f1, f2 in fields:
                if a[f1] != b[f2]:
                    mismatches.append({"seed": seed, "policy": policy, "field": f1, "v1": a[f1], "v2": b[f2]})
    return {"runs_compared": compared, "ticks": ticks, "exact_match": not mismatches, "mismatches": mismatches}


def _events(args):
    policy, seed, p = args
    r = v2.run_one(policy, seed, p, record_events=True)
    return policy, seed, r["env_digest"], r["events_query"], r["flips"]


def check_pairing(seeds: range = range(4), workers: int = 6) -> dict:
    out = {}
    for label, legacy in (("v1_shared_stream", True), ("v2_split_streams", False)):
        p = replace(v2.Params(), legacy_shared_rng=legacy)
        jobs = [(policy, s, p) for s in seeds for policy in v2.POLICIES]
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(_events, jobs))
        per_seed = {}
        for s in seeds:
            rs = {pol: (d, q, f) for pol, seed, d, q, f in results if seed == s}
            ref_q = np.array(rs["none"][1])
            detail = {}
            for pol, (d, q, f) in rs.items():
                q = np.array(q)
                diff = np.flatnonzero(q != ref_q)
                detail[pol] = {
                    "digest_matches_none": d == rs["none"][0],
                    "first_query_divergence_tick": int(diff[0]) if len(diff) else None,
                    "fraction_query_ticks_differing": float(len(diff) / len(q)),
                    "total_flips": int(f),
                }
            per_seed[str(s)] = {
                "all_digests_identical": len({v[0] for v in rs.values()}) == 1,
                "policies": detail,
            }
        out[label] = {"all_seeds_paired": all(v["all_digests_identical"] for v in per_seed.values()),
                      "seeds": per_seed}
    return out


def check_repair_isolation(widths=range(3, 9)) -> dict:
    table = {}
    violations = []
    for bits in widths:
        rows = {}
        for truth in (0, 1):
            for pattern in itertools.product((0, 1), repeat=bits):
                start = np.array(pattern, dtype=np.int8)
                wrong = int((start != truth).sum())
                finals = []
                for rng_seed in (0, 1):  # which disagreeing bit is chosen must not matter
                    trace = start.copy()
                    rng = np.random.default_rng(rng_seed)
                    steps = 0
                    while v2.repair_one_bit(trace, rng):
                        steps += 1
                        if steps > bits:
                            violations.append({"bits": bits, "pattern": pattern, "issue": "no fixed point"})
                            break
                    finals.append((trace.copy(), steps))
                if not np.array_equal(finals[0][0], finals[1][0]) or finals[0][1] != finals[1][1]:
                    violations.append({"bits": bits, "pattern": pattern, "issue": "order-dependent result"})
                final, steps = finals[0]
                before = v2.majority(start) == truth
                after = v2.majority(final) == truth
                key = (truth, wrong)
                agg = rows.setdefault(key, {"patterns": 0, "decode_correct_before": 0, "decode_correct_after": 0,
                                            "fully_restored": 0, "worsened": 0, "recovered": 0, "repairs": 0})
                agg["patterns"] += 1
                agg["decode_correct_before"] += before
                agg["decode_correct_after"] += after
                agg["fully_restored"] += bool((final == truth).all())
                agg["worsened"] += before and not after
                agg["recovered"] += (not before) and after
                agg["repairs"] += steps
        table[str(bits)] = {
            f"truth{t}_wrong{w}": {**v, "mean_repairs": v["repairs"] / v["patterns"]}
            for (t, w), v in sorted(rows.items())
        }
    return {"violations": violations, "by_width": table}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    result = {
        "engineering_seed_only": True,
        "A_refactor_equivalence": check_equivalence(),
        "B_random_stream_pairing": check_pairing(),
        "C_repair_isolation": check_repair_isolation(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1))

    a = result["A_refactor_equivalence"]
    print(f"A. v2 legacy mode reproduces v1: {a['exact_match']} ({a['runs_compared']} runs, {a['ticks']} ticks)")
    for label, b in result["B_random_stream_pairing"].items():
        firsts = [d["first_query_divergence_tick"] for s in b["seeds"].values()
                  for pol, d in s["policies"].items() if pol != "none"]
        fracs = [d["fraction_query_ticks_differing"] for s in b["seeds"].values()
                 for pol, d in s["policies"].items() if pol != "none"]
        known = [f for f in firsts if f is not None]
        print(f"B. {label}: environments identical across policies = {b['all_seeds_paired']}; "
              f"earliest query divergence tick = {min(known) if known else None}; "
              f"mean fraction of query ticks differing = {np.mean(fracs):.3f}")
    c = result["C_repair_isolation"]
    print(f"C. repair isolation violations: {len(c['violations'])}")
    for bits, rows in c["by_width"].items():
        cells = []
        for key, v in rows.items():
            cells.append(f"{key}: after={v['decode_correct_after']}/{v['patterns']} "
                         f"worse={v['worsened']} rec={v['recovered']} cost={v['mean_repairs']:.1f}")
        print(f"   width {bits}:\n     " + "\n     ".join(cells))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
