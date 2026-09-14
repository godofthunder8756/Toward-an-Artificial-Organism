"""Pre-freeze audit of e3_fep_engineering_seed_v3.py (engineering seeds only).

Prints invariants only. It deliberately reports no recall comparison between
candidate allocators, so selection and freezing stay blind to their outcomes.

A. v3 reproduces v2 exactly for every shared policy (odd width).
B. v3's pregenerated environment has v2's digest, and each seed replays the
   same environment for every policy.
C. Truth leak test: relabelling evaluator truth (stored traces unchanged) must
   leave every truth-blind policy's repair decisions identical; truth_oracle
   must change, which shows the test can detect a leak.
D. Loss model: probabilities in [0, 1], monotone in minority count and rounds,
   and agreement with Monte Carlo simulation.
E. Rate learning: recov_learned's final estimate against the true flip rate.
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v2 as v2
import e3_fep_engineering_seed_v3 as v3

OUT = Path("e3_fep_seed_results/v3/audit_v3.json")
SHARED = {"none": "none", "random": "random", "uniform": "uniform", "recency": "recency",
          "precision": "precision", "oracle": "truth_oracle", "ample": "ample"}


def check_equivalence(ticks=1500, seeds=range(3), bits=7) -> dict:
    p2 = replace(v2.Params(), ticks=ticks, trace_bits=bits)
    p3 = replace(v3.Params(), ticks=ticks, trace_bits=bits)
    mismatches, compared = [], 0
    for seed in seeds:
        env = v3.generate_environment(seed, p3)
        for old, new in SHARED.items():
            a = v2.run_one(old, seed, p2)
            b = v3.run_one(new, seed, p3, env=env)
            compared += 1
            for key, value in a.items():
                if key == "policy":
                    continue
                other = b[key]
                same = (np.isnan(value) and np.isnan(other)) if isinstance(value, float) and np.isnan(value) else value == other
                if not same:
                    mismatches.append({"seed": seed, "policy": old, "field": key, "v2": value, "v3": other})
    return {"runs_compared": compared, "ticks": ticks, "width": bits, "exact_match": not mismatches,
            "mismatches": mismatches[:20]}


def check_environment(seeds=range(3), ticks=1500) -> dict:
    p3 = replace(v3.Params(), ticks=ticks)
    out = {}
    for seed in seeds:
        env = v3.generate_environment(seed, p3)
        digests = {v3.run_one(pol, seed, p3, env=None if pol == "blind_oracle" else env)["env_digest"]
                   for pol in v3.POLICIES}
        out[str(seed)] = {"single_digest_across_policies": len(digests) == 1}
    return {"all_ok": all(v["single_digest_across_policies"] for v in out.values()), "seeds": out}


def check_truth_leak(seeds=range(2), ticks=1500) -> dict:
    p3 = replace(v3.Params(), ticks=ticks, budget=3, corrupt_p=0.03)
    results = {}
    for seed in seeds:
        env = v3.generate_environment(seed, p3)
        mask = np.zeros(p3.n_cues, dtype=bool)
        mask[::2] = True
        for pol in v3.POLICIES:
            a = v3.run_one(pol, seed, p3, env=env)["repair_digest"]
            b = v3.run_one(pol, seed, p3, relabel=mask, env=env)["repair_digest"]
            results.setdefault(pol, []).append(a == b)
    blind_ok = all(all(results[pol]) for pol in v3.POLICIES if pol != "truth_oracle")
    detector_ok = not all(results["truth_oracle"])
    return {"truth_blind_policies_invariant": blind_ok, "truth_oracle_detected": detector_ok,
            "identical_decisions_by_policy": results}


def check_loss_model(bits=7, p_flip=0.02, rounds=(1, 5, 20, 60), samples=200000) -> dict:
    table = v3.loss_probability_table(bits, p_flip)
    bounded = bool(((table >= -1e-12) & (table <= 1 + 1e-12)).all())
    monotone_d = bool((np.diff(table, axis=0) >= -1e-12).all())
    monotone_r = bool((np.diff(table[:, :200], axis=1) >= -1e-12).all())
    rng = np.random.default_rng(12345)
    f = (bits + 1) // 2
    comparisons = []
    for d in range(f):
        for r in rounds:
            state = np.zeros((samples, bits), dtype=bool)  # True = in current minority value
            state[:, :d] = True
            for _ in range(r):
                state ^= rng.random((samples, bits)) < p_flip
            mc = float((state.sum(axis=1) >= f).mean())
            se = (mc * (1 - mc) / samples) ** 0.5
            comparisons.append({"d": d, "rounds": r, "model": float(table[d, r]), "monte_carlo": mc,
                                "within_4se": bool(abs(mc - table[d, r]) <= 4 * se + 1e-4)})
    return {"bounded": bounded, "monotone_in_minority": monotone_d, "monotone_in_rounds_first200": monotone_r,
            "monte_carlo_agreement": all(c["within_4se"] for c in comparisons), "comparisons": comparisons}


def check_rate_learning(configs=((7, 0.01, 3), (7, 0.03, 3), (9, 0.02, 4)), seed=0, ticks=3000) -> dict:
    rows = []
    for bits, p_flip, budget in configs:
        p3 = replace(v3.Params(), ticks=ticks, trace_bits=bits, corrupt_p=p_flip, budget=budget)
        r = v3.run_one("recov_learned", seed, p3)
        rows.append({"width": bits, "true_p": p_flip, "budget": budget, "p_hat_final": r["p_hat_final"],
                     "relative_error": abs(r["p_hat_final"] - p_flip) / p_flip})
    return {"rows": rows}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    result = {
        "engineering_seed_only": True,
        "A_equivalence_with_v2": check_equivalence(),
        "B_environment_replay": check_environment(),
        "C_truth_leak": check_truth_leak(),
        "D_loss_model": check_loss_model(),
        "E_rate_learning": check_rate_learning(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    A, B, C, D, E = (result[k] for k in list(result)[1:])
    print(f"A. v3 == v2 on shared policies: {A['exact_match']} ({A['runs_compared']} runs); mismatches: {A['mismatches'][:3]}")
    print(f"B. one environment digest per seed across all policies: {B['all_ok']}")
    print(f"C. truth-blind decisions invariant to relabel: {C['truth_blind_policies_invariant']}; "
          f"truth_oracle leak detected: {C['truth_oracle_detected']}")
    print(f"D. loss model bounded={D['bounded']} monotone(d)={D['monotone_in_minority']} "
          f"monotone(r)={D['monotone_in_rounds_first200']} MC agreement={D['monte_carlo_agreement']}")
    for row in E["rows"]:
        print(f"E. width {row['width']} p={row['true_p']} budget {row['budget']}: p_hat={row['p_hat_final']:.4f} "
              f"(relative error {row['relative_error']:.1%})")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
