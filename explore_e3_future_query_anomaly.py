"""EXPLORATORY bounded diagnostic of two v2-study anomalies (not prespecified).

1. Future-query anomaly. With identical actions and objective, more information
   cannot lower the best achievable recall. recov_supplied (inferred relevance)
   scored 0.957 but blind_oracle (realized future queries) scored 0.663 with the
   same loss model. This asks which information-use rule causes the loss by
   swapping only the relevance input to the loss model:
     inferred           belief-mixed expected query probability (= recov_supplied)
     oracle_ignores     the oracle with use_future=False; must equal inferred,
                        which shows the extra information can simply be ignored
     true_state         expected query probability from the true current hot state
     true_trajectory    exact per-tick query probability from the true future
                        hot trajectory (knows relevance, not the realized draws)
     realized           indicator of the realized future queries (= blind_oracle)
     realized_long      realized with a 3,000-round horizon
     inferred_long      inferred with a 3,000-round horizon
   plus decision diagnostics: mean depth repaired, depth inversions, and the
   share of repairs and inversions involving zero-valued cues.
2. Rate sensitivity. Is "recov_learned ~ recov_supplied" informative? Supplied
   rate misspecified x0.25, x0.5, x2, x4, and recov_learned's stored estimate
   overwritten at tick 1,000 with x0.25 or x4 the true rate and learning stopped.

The harness is validated to reproduce v4 recov_supplied, recov_learned and
blind_oracle exactly before anything else runs. Engineering seeds 16-23, never
used before. Configurations are the two v2 confirmatory configurations.
"""

from __future__ import annotations

import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v4 as v4

OUT = Path("e3_fep_seed_results/v4/exploratory_future_query_anomaly.json")
CONFIGS = ((9, 0.02, 3), (9, 0.03, 4))
SEEDS = tuple(range(16, 24))
LONG = 3000
ANOMALY_VARIANTS = ("inferred", "oracle_ignores", "true_state", "true_trajectory", "realized",
                    "realized_long", "inferred_long")
RATE_VARIANTS = ("supplied_x0.25", "supplied_x0.5", "supplied_x1", "supplied_x2", "supplied_x4",
                 "learned", "learned_override_x0.25", "learned_override_x4")


def simulate(variant: str, seed: int, p: v4.Params, env: v4.Environment) -> dict:
    rng = np.random.default_rng([seed, 1])
    n, bits, T = p.n_cues, p.trace_bits, p.ticks
    f = (bits + 1) // 2
    a, b, cw = p.p_hot_to_cold, p.p_cold_to_hot, p.cold_query_weight

    horizon = LONG if variant.endswith("_long") else v4.HORIZON
    rate = p.corrupt_p
    if variant.startswith("supplied_x"):
        rate = min(p.corrupt_p * float(variant.split("_x")[1]), 0.45)
    learned = variant.startswith("learned")
    override = float(variant.split("_x")[1]) if "override" in variant else None
    source = ("realized" if variant.startswith("realized") else
              "true_state" if variant == "true_state" else
              "true_trajectory" if variant == "true_trajectory" else "inferred")

    qh, qc = v4.query_probability_ahead(p, horizon)
    benefit = v4.repair_benefit_table(bits, 0.45 if learned else rate, horizon)
    vh, vc = benefit @ qh, benefit @ qc
    p_hat, flips_seen, opportunities = 0.45, 0, 0
    prev_minority = np.zeros(n, dtype=np.int64)

    if source == "true_trajectory":
        weights = np.where(env.hot, 1.0, cw)
        query_prob = weights / weights.sum(axis=1, keepdims=True)  # (T, n) exact probability at each tick
    query_ticks = [np.flatnonzero(env.queries == i) for i in range(n)]

    trace = np.repeat(env.truth[:, None], bits, axis=1).astype(np.int8)
    belief = np.full(n, p.initial_hot_p)
    digest = hashlib.sha256()
    c = dict.fromkeys("queries correct repairs depth_sum inversion_ticks inversion_zero_value "
                      "zero_value_repairs majority_flips".split(), 0)

    for t in range(T):
        qi = int(env.queries[t])
        prior = belief * (1 - a) + (1 - belief) * b
        ew = float(np.sum(prior + (1 - prior) * cw))
        lh, lc = np.full(n, 1 - 1 / ew), np.full(n, 1 - cw / ew)
        lh[qi], lc[qi] = 1 / ew, cw / ew
        belief = prior * lh / (prior * lh + (1 - prior) * lc)

        c["queries"] += 1
        c["correct"] += int(v4.majority(trace[qi]) == env.truth[qi])
        maj_before = (trace.sum(axis=1) * 2 >= bits)
        trace = np.where(env.flips[t], 1 - trace, trace).astype(np.int8)
        ones = trace.sum(axis=1)
        minority = np.minimum(ones, bits - ones)
        c["majority_flips"] += int(((ones * 2 >= bits) != maj_before).sum())
        if learned:
            clean = prev_minority == 0
            flips_seen += int(minority[clean].sum())
            opportunities += bits * int(clean.sum())

        needing = np.flatnonzero(minority > 0)
        chosen = []
        if len(needing):
            d = minority[needing]
            if source == "realized":
                scores = np.zeros(len(needing))
                for j, cue in enumerate(needing):
                    qt = query_ticks[cue]
                    lo = np.searchsorted(qt, t, side="right")
                    hi = np.searchsorted(qt, t + horizon, side="right")
                    scores[j] = benefit[d[j], qt[lo:hi] - t - 1].sum()
            elif source == "true_trajectory":
                scores = np.zeros(len(needing))
                stop = min(T, t + 1 + horizon)
                for j, cue in enumerate(needing):
                    probs = query_prob[t + 1:stop, cue]
                    scores[j] = benefit[d[j], : len(probs)] @ probs
            elif source == "true_state":
                scores = np.where(env.hot[t][needing], vh[d], vc[d])
            else:
                bh = belief[needing]
                scores = bh * vh[d] + (1 - bh) * vc[d]
            scores = scores + 1e-12 * rng.random(len(needing))
            order = list(np.argsort(scores)[::-1])
            chosen = [int(needing[k]) for k in order[: p.budget]]
            chosen_set = set(chosen)
            raw = scores - 1e-12  # jitter is below any real value difference
            zero_valued = {int(needing[j]) for j in range(len(needing)) if raw[j] <= 1e-11}
            deepest_skipped = [int(cue) for cue in needing if minority[cue] == f - 1 and int(cue) not in chosen_set]
            if deepest_skipped and any(minority[cue] < f - 1 for cue in chosen):
                c["inversion_ticks"] += 1
                c["inversion_zero_value"] += int(any(cue in zero_valued for cue in deepest_skipped))
            for cue in chosen:
                c["depth_sum"] += int(minority[cue])
                c["zero_value_repairs"] += int(cue in zero_valued)

        digest.update(np.int64(t).tobytes())
        for cue in chosen:
            bit = v4.repair_one_bit(trace[cue], rng)
            c["repairs"] += 1
            digest.update(np.int64(cue).tobytes() + np.int64(bit).tobytes())

        if learned:
            ones_after = trace.sum(axis=1)
            prev_minority = np.minimum(ones_after, bits - ones_after)
            if t % v4.LEARN_REFRESH == v4.LEARN_REFRESH - 1:
                if override is not None and t >= 1000:
                    p_hat = min(p.corrupt_p * override, 0.45)
                else:
                    p_hat = float(np.clip((flips_seen + 1) / (opportunities + 2), 1e-4, 0.45))
                bt = v4.repair_benefit_table(bits, p_hat, horizon)
                vh, vc = bt @ qh, bt @ qc

    repairs = max(c["repairs"], 1)
    return {"variant": variant, "seed": seed, "repair_digest": digest.hexdigest(),
            "overall_accuracy": c["correct"] / c["queries"], "mean_depth_repaired": c["depth_sum"] / repairs,
            "inversion_tick_fraction": c["inversion_ticks"] / T,
            "inversions_with_zero_valued_deep_cue": (c["inversion_zero_value"] / c["inversion_ticks"]
                                                     if c["inversion_ticks"] else float("nan")),
            "zero_value_repair_fraction": c["zero_value_repairs"] / repairs,
            "majority_flips_per_cue_tick": c["majority_flips"] / (n * T), "p_hat_final": p_hat if learned else None}


def validate() -> dict:
    checks = []
    for cfg in CONFIGS:
        p = replace(v4.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2], ticks=2000)
        env = v4.generate_environment(16, p)
        for variant, policy in (("inferred", "recov_supplied"), ("oracle_ignores", "recov_supplied"),
                                ("realized", "blind_oracle"), ("learned", "recov_learned"),
                                ("supplied_x1", "recov_supplied")):
            ref, mine = v4.run_one(policy, 16, p, env=env), simulate(variant, 16, p, env)
            checks.append({"cfg": cfg, "variant": variant, "policy": policy,
                           "match": ref["repair_digest"] == mine["repair_digest"]
                           and ref["overall_accuracy"] == mine["overall_accuracy"]})
    return {"all_match": all(c["match"] for c in checks), "checks": checks}


def _job(args):
    cfg, seed = args
    p = replace(v4.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2])
    env = v4.generate_environment(seed, p)
    rows = [simulate(v, seed, p, env) for v in ANOMALY_VARIANTS + RATE_VARIANTS]
    rows.append({"variant": "depth_first", "seed": seed,
                 "overall_accuracy": v4.run_one("depth_first", seed, p, env=env)["overall_accuracy"]})
    return cfg, rows


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    validation = validate()
    print(f"harness reproduces v4 recov_supplied, recov_learned and blind_oracle: {validation['all_match']}", flush=True)
    if not validation["all_match"]:
        OUT.write_text(json.dumps({"exploratory": True, "validation": validation}, indent=1))
        sys.exit("validation failed; nothing else run")
    with ProcessPoolExecutor(max_workers=7) as pool:
        results = list(pool.map(_job, [(cfg, s) for cfg in CONFIGS for s in SEEDS]))
    report = []
    boot = np.random.default_rng(20260914)
    for cfg in CONFIGS:
        rows = [r for c, batch in results if c == cfg for r in batch]
        by = {(r["variant"], r["seed"]): r for r in rows}
        print(f"\nwidth {cfg[0]} p {cfg[1]} budget {cfg[2]}  (paired vs inferred, overall recall; descriptive 95%)")
        entry = {"config": cfg, "variants": {}}
        for v in ANOMALY_VARIANTS + RATE_VARIANTS + ("depth_first",):
            d = np.array([by[(v, s)]["overall_accuracy"] - by[("inferred", s)]["overall_accuracy"] for s in SEEDS])
            lo, hi = np.quantile(d[boot.integers(0, len(d), size=(10000, len(d)))].mean(axis=1), [0.025, 0.975])
            keys = [k for k in rows[0] if k not in ("variant", "seed", "repair_digest")]
            means = {k: float(np.nanmean([by[(v, s)][k] for s in SEEDS if by[(v, s)].get(k) is not None]))
                     for k in keys if any(by[(v, s)].get(k) is not None for s in SEEDS)}
            same = (len({by[(v, s)].get("repair_digest") for s in SEEDS} & {by[("inferred", s)]["repair_digest"] for s in SEEDS}) > 0
                    if v != "depth_first" else False)
            entry["variants"][v] = {**means, "diff_vs_inferred": float(d.mean()), "ci95": [float(lo), float(hi)],
                                    "identical_decisions_to_inferred": all(
                                        by[(v, s)].get("repair_digest") == by[("inferred", s)]["repair_digest"] for s in SEEDS)}
            m = entry["variants"][v]
            extra = "" if v == "depth_first" else (
                f" depth {m['mean_depth_repaired']:.2f} inversions {m['inversion_tick_fraction']:.3f} "
                f"(zero-valued deep {m['inversions_with_zero_valued_deep_cue']:.2f}) zero-value repairs "
                f"{m['zero_value_repair_fraction']:.3f} flips/cue-tick {m['majority_flips_per_cue_tick']:.4f}"
                + (f" p_hat {m['p_hat_final']:.4f}" if "p_hat_final" in m else ""))
            print(f"  {v:<24} recall {m['overall_accuracy']:.3f} diff {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] "
                  f"same_decisions={m['identical_decisions_to_inferred']}{extra}")
        report.append(entry)
    OUT.write_text(json.dumps({"exploratory": True, "seeds": SEEDS, "validation": validation, "report": report},
                              indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
