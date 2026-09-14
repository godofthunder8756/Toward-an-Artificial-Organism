"""Pre-selection audit of e3_obsolescence_world.py. Prints invariants only.

A. Environment: one digest per seed across policies. Queries only target HOT or
   SHORT cues. Exactly n_obsolete cues become OBSOLETE, at their scheduled ticks,
   permanently. Returns only come from dormancy.
B. Interface: Observation has exactly {t, traces, obsolete_flags}; traces are
   read-only; only depth_flag receives flags, and inverting its flags changes
   its decisions.
C. Truth relabelling leaves every policy's repair decisions unchanged.
D. Policy unit tests on hand-built observations: ordering, deprioritization and
   the learned quantile.
"""

from __future__ import annotations

import dataclasses
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_obsolescence_world as ob

OUT = Path("e3_fep_seed_results/ob1/audit_ob1.json")


def check_environment(seeds=(0, 1, 2)) -> dict:
    w = replace(ob.WorldParams(), ticks=4000)
    out = []
    for seed in seeds:
        env = ob.generate_environment(seed, w)
        digests = {ob.run_one(p, seed, w, env=None if p == "depth_first" else env)["env_digest"] for p in ob.POLICIES}
        q = env.queries
        valid_q = q >= 0
        targets = env.state[np.flatnonzero(valid_q), q[valid_q]]
        obsolete_cues = np.flatnonzero(env.obsolete_at >= 0)
        schedule_ok = all(
            (env.state[: env.obsolete_at[c], c] != ob.OBSOLETE).all() and (env.state[env.obsolete_at[c]:, c] == ob.OBSOLETE).all()
            for c in obsolete_cues)
        prev = np.vstack([np.where(env.state[0] >= 0, env.state[0], 0)[None, :], env.state[:-1]])
        returns_from_dormancy = bool(np.isin(prev[env.returns], (ob.SHORT, ob.LONG)).all()) if env.returns.any() else True
        out.append({"seed": seed, "one_digest": len(digests) == 1,
                    "queries_only_hot_or_short": bool(np.isin(targets, (ob.HOT, ob.SHORT)).all()),
                    "obsolete_count_exact": len(obsolete_cues) == w.n_obsolete,
                    "obsolescence_permanent_and_on_schedule": bool(schedule_ok),
                    "returns_only_from_dormancy": returns_from_dormancy,
                    "long_returns_subset": bool((env.long_returns <= env.returns).all())})
    return {"all_ok": all(all(v for k, v in r.items() if k != "seed") for r in out), "seeds": out}


def check_interface(seed=3) -> dict:
    fields = {f.name for f in dataclasses.fields(ob.Observation)}
    view = np.zeros((2, 3), dtype=np.int8)
    view.flags.writeable = False
    try:
        view[0, 0] = 1
        readonly = False
    except ValueError:
        readonly = True
    flag_receivers = sorted(name for name, cls in ob.POLICY_CLASSES.items() if cls.receives_flags)
    w = replace(ob.WorldParams(), ticks=3000)
    env = ob.generate_environment(seed, w)
    original = ob.run_one("depth_flag", seed, w, env=env)["repair_digest"]

    class InvertedFlags(ob.DepthFlagPolicy):
        def choose(self, obs):
            return super().choose(ob.Observation(obs.t, obs.traces, ~obs.obsolete_flags))

    ob.POLICY_CLASSES["_inverted"] = InvertedFlags
    try:
        inverted = ob.run_one("_inverted", seed, w, env=env)["repair_digest"]
    finally:
        del ob.POLICY_CLASSES["_inverted"]
    return {"observation_fields": sorted(fields), "fields_ok": fields == {"t", "traces", "obsolete_flags"},
            "traces_read_only": readonly, "flag_receivers": flag_receivers,
            "only_depth_flag_receives_flags": flag_receivers == ["depth_flag"],
            "flags_change_depth_flag_decisions": original != inverted}


def check_truth_relabel(seeds=(4, 5)) -> dict:
    w = replace(ob.WorldParams(), ticks=3000)
    mask = np.zeros(w.n_cues, dtype=bool)
    mask[::3] = True
    same = {}
    for seed in seeds:
        env = ob.generate_environment(seed, w)
        for p in ob.POLICIES:
            same.setdefault(p, []).append(ob.run_one(p, seed, w, env=env)["repair_digest"]
                                          == ob.run_one(p, seed, w, env=env, relabel=mask)["repair_digest"])
    return {"all_invariant": all(all(v) for v in same.values()), "by_policy": same}


def check_policies() -> dict:
    pp = ob.PolicyParams(n_cues=5, trace_bits=5, budget=2)
    traces = np.array([[0, 0, 0, 0, 1],    # depth 1
                       [1, 1, 1, 0, 0],    # depth 2
                       [0, 0, 0, 0, 0],    # undamaged
                       [1, 1, 0, 0, 1],    # depth 2
                       [1, 1, 1, 1, 0]],   # depth 1
                      dtype=np.int8)
    traces.flags.writeable = False
    results = {}
    df = ob.DepthFirstPolicy(pp, np.random.default_rng(0))
    df.last_repair[:] = [0, 5, 0, 1, 0]
    results["depth_first_picks_deepest_then_stalest"] = df.choose(ob.Observation(10, traces, None)) == [3, 1]
    flags = np.array([False, False, False, True, False])
    fl = ob.DepthFlagPolicy(pp, np.random.default_rng(0))
    picked = fl.choose(ob.Observation(10, traces, flags))
    results["depth_flag_skips_flagged_when_alternatives_exist"] = 3 not in picked and 1 in picked
    to = ob.DepthTimeoutPolicy(pp, np.random.default_rng(0))
    to.last_query[:] = [900, 900, 900, 0, 900]
    picked = to.choose(ob.Observation(1000, traces, None))
    results["timeout_deprioritizes_silent_cue"] = 3 not in picked and bool(to.deprioritized()[3])
    lp = ob.DepthLearnedPolicy(pp, np.random.default_rng(0))
    for k in range(60):
        lp.observe_query(k * 10, 0)  # 59 gaps of 10 ticks
    lp.observe_query(1000, 1)
    lp.observe_query(1500, 1)       # one gap of 500
    lp.choose(ob.Observation(1550, traces, None))
    results["learned_threshold_is_q99_of_own_gaps"] = abs(lp.threshold - np.quantile([10] * 59 + [500], 0.99)) < 1e-9
    results["learned_no_threshold_before_min_gaps"] = np.isinf(ob.DepthLearnedPolicy(pp, np.random.default_rng(0)).threshold)
    return {"all_ok": all(results.values()), "tests": results}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    result = {"A_environment": check_environment(), "B_interface": check_interface(),
              "C_truth_relabel": check_truth_relabel(), "D_policy_units": check_policies()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    a, b, c, d = result.values()
    print(f"A. environment invariants: {a['all_ok']}")
    print(f"B. interface: fields_ok={b['fields_ok']} read_only={b['traces_read_only']} "
          f"only_depth_flag_gets_flags={b['only_depth_flag_receives_flags']} flags_used={b['flags_change_depth_flag_decisions']}")
    print(f"C. truth relabel invariant for all policies: {c['all_invariant']}")
    print(f"D. policy unit tests: {d['all_ok']} {d['tests']}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
