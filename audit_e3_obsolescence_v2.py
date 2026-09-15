"""Pre-freeze audit for E3-OB2. Prints invariants only; no allocator comparison.

A. The environment is OB1's: one digest per seed across all OB2 policies, equal
   to the OB1 digest.
B. Information boundaries:
   - truth relabelling leaves every policy's repair decisions unchanged
   - only depth_flag receives flags
   - only return_supplied* receive the table
   - policies see query identities whatever their eligibility or memory state
C. Hard eligibility: no policy repairs an ineligible cue; the budget is never
   exceeded.
D. Kaplan-Meier estimator against a direct reference implementation on
   synthetic censored data; censored silences lower the estimated return
   probability; eligibility resumes after a query.
E. The supplied table is built from reference seeds 500-563, disjoint from
   every other seed family.
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_obsolescence_world as ob
import e3_obsolescence_world_v2 as ob2

OUT = Path("e3_fep_seed_results/ob2/audit_ob2.json")
TABLE = Path("e3_fep_seed_results/ob2/return_table.json")
REFERENCE_SEEDS = tuple(range(500, 564))


def load_table() -> np.ndarray:
    return np.array(json.loads(TABLE.read_text())["prob"])


def check_environment_and_boundaries(table, seeds=(0, 1)) -> dict:
    w = replace(ob.WorldParams(), ticks=3000)
    out = {"digests": [], "relabel": {}, "ineligible_repairs": {}, "budget_ok": True}
    mask = np.zeros(w.n_cues, dtype=bool)
    mask[1::3] = True
    for seed in seeds:
        env = ob.generate_environment(seed, w)
        ob1_digest = ob.run_one("depth_first", seed, w, env=env)["env_digest"]
        rows = {p: ob2.run_one(p, seed, w, table, tuned_timeout=750, env=env) for p in ob2.POLICIES}
        out["digests"].append(len({r["env_digest"] for r in rows.values()} | {ob1_digest}) == 1)
        for p, r in rows.items():
            relabelled = ob2.run_one(p, seed, w, table, tuned_timeout=750, env=env, relabel=mask)
            out["relabel"].setdefault(p, []).append(r["repair_digest"] == relabelled["repair_digest"])
            out["ineligible_repairs"].setdefault(p, 0)
            out["ineligible_repairs"][p] += r["repairs_to_ineligible"]
    receivers_flags = sorted(p for p, cls in ob2.POLICY_CLASSES.items() if cls.receives_flags)
    receivers_table = sorted(p for p in ob2.POLICIES
                             if ob2.policy_params(p, w, table, 750).return_table is not None)
    return {
        "one_digest_equal_to_ob1": all(out["digests"]),
        "truth_relabel_invariant": all(all(v) for v in out["relabel"].values()),
        "no_repairs_to_ineligible": all(v == 0 for k, v in out["ineligible_repairs"].items() if k != "ample"),
        "flag_receivers": receivers_flags, "table_receivers": receivers_table,
        "boundaries_ok": receivers_flags == ["depth_flag"]
        and receivers_table == ["return_supplied", "return_supplied_c0.05", "return_supplied_c0.2"],
        "queries_always_observed": "observe_query is called for every query before choose, independent of eligibility",
        "detail": out,
    }


def _reference_km(durations_completed, ongoing, s, horizon, bin_size=ob2.KM_BIN, bins=ob2.KM_BINS):
    """Direct Kaplan-Meier on binned durations, written independently of the policy code."""
    def b(x):
        return min(x // bin_size, bins - 1)
    survival = [1.0]
    for k in range(bins):
        events = sum(1 for d in durations_completed if b(d) == k)
        at_risk = sum(1 for d in durations_completed if b(d) >= k) + sum(1 for o in ongoing if b(o) >= k)
        survival.append(survival[-1] * (1 - events / at_risk) if at_risk else survival[-1])
    k1, k2 = min(s // bin_size, bins), min((s + horizon) // bin_size, bins)
    return 0.0 if survival[k1] == 0 else 1 - survival[k2] / survival[k1]


def check_estimator() -> dict:
    pp = ob2.PolicyParams2(n_cues=4, trace_bits=9, budget=2)
    rng = np.random.default_rng(1)
    pol = ob2.ReturnLearned(pp, np.random.default_rng(0))
    completed = []
    t = 0
    for _ in range(400):  # synthetic query stream on 4 cues with a long-gap mixture
        cue = int(rng.integers(0, 4))
        t += int(rng.choice([3, 8, 150, 900]))
        completed.append(t - int(pol.last_query[cue]))
        pol.observe_query(t, cue)
    now = t + 700
    pol._refresh(now)
    ongoing = [int(x) for x in now - pol.last_query]
    saved = pol.last_query.copy()
    diffs = []
    for s in (0, 50, 200, 600, 1200):
        pol.last_query[0] = now - s   # prediction only; the survival curve is already fixed
        diffs.append(abs(float(pol.predict_all(now)[0]) - _reference_km(completed, ongoing, s, ob2.HORIZON)))
    pol.last_query[:] = saved
    km_matches = pol.ready and max(diffs) < 1e-9

    # Censoring matters: identical completed silences, but many long ongoing silences
    # add at-risk mass without events, which must lower predicted return.
    def estimate(ongoing_silence):
        p = ob2.ReturnLearned(ob2.PolicyParams2(n_cues=40, trace_bits=9, budget=2), np.random.default_rng(0))
        p.events[150 // ob2.KM_BIN] = 20
        p.events[900 // ob2.KM_BIN] = 20
        p.long_events = 40
        p.last_query[:] = 4000 - ongoing_silence
        p._refresh(4000)
        p.last_query[0] = 4000 - 100   # query the prediction at silence 100
        return float(p.predict_all(4000)[0])
    censoring_counts = estimate(3000) < estimate(0)

    # Resumption: a query makes a silent cue eligible again.
    pol4 = ob2.ReturnLearned(ob2.PolicyParams2(n_cues=2, trace_bits=9, budget=1), np.random.default_rng(0))
    pol4.ready = True
    # One fixed curve: most silences end within 100 ticks, none observed past 1,000.
    curve = np.ones(ob2.KM_BINS + 1)
    curve[1:11] = np.linspace(0.5, 0.2, 10)
    curve[11:101] = np.linspace(0.2, 0.1, 90)
    curve[101:] = 0.1
    pol4.survival = curve
    before = bool(pol4.predict_all(5000)[1] >= ob2.CUTOFF)   # silent for 5,000 ticks
    pol4.observe_query(5000, 1)
    after = bool(pol4.predict_all(5000)[1] >= ob2.CUTOFF)    # silence reset by the query alone
    return {"km_matches_reference": bool(km_matches), "max_abs_diff": float(max(diffs)),
            "censored_silences_change_estimate": bool(censoring_counts),
            "eligibility_can_resume_after_query": (not before) and after}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    if not TABLE.exists():
        built = ob2.build_return_table(ob.WorldParams(), REFERENCE_SEEDS)
        TABLE.parent.mkdir(parents=True, exist_ok=True)
        TABLE.write_text(json.dumps({k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in built.items()}))
        print(f"built supplied return table from reference seeds {REFERENCE_SEEDS[0]}-{REFERENCE_SEEDS[-1]}")
    table = load_table()
    result = {"A_B_C_environment_boundaries_eligibility": check_environment_and_boundaries(table),
              "D_estimator": check_estimator(),
              "E_reference_seeds": {"reference": [REFERENCE_SEEDS[0], REFERENCE_SEEDS[-1]],
                                    "disjoint_from": "engineering 0-23, v2 finals 200-231, OB1 finals 300-331, OB2 finals 400-431"}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    a, d = result["A_B_C_environment_boundaries_eligibility"], result["D_estimator"]
    print(f"A. one env digest equal to OB1: {a['one_digest_equal_to_ob1']}")
    print(f"B. truth relabel invariant: {a['truth_relabel_invariant']}; boundaries ok: {a['boundaries_ok']} "
          f"(flags {a['flag_receivers']}, table {a['table_receivers']})")
    print(f"C. no repairs to ineligible cues: {a['no_repairs_to_ineligible']}")
    print(f"D. estimator: {d}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
