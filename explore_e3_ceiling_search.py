"""EXPLORATORY: can any truth-blind scheduler beat round-robin in the unchanged v3 world?

E3_ALLOCATION_PROTOCOL_v1.md stopped at phase 1 because blind_oracle, the
myopic loss-model ceiling, did not beat uniform. Before changing any world rule,
this asks whether headroom above uniform exists at all for schedulers that
never read truth. Schedulers may read true relevance and true future query
times; they are ceilings or probes, never candidate mechanisms.

- Engineering seeds 8-15 (not used by phase 1).
- Configurations: the phase-1 grid points where budgeted repair is not
  hopeless.
- The harness is validated first: it must reproduce v3's uniform and
  blind_oracle exactly (recall and every repair decision).
- Nothing here is prespecified or confirmatory.
"""

from __future__ import annotations

import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np

import e3_fep_engineering_seed_v3 as v3

OUT = Path("e3_fep_seed_results/v3/exploratory_ceiling_search.json")
CONFIGS = ((9, 0.02, 3), (9, 0.03, 3), (9, 0.03, 4))
SEEDS = tuple(range(8, 16))
DEADLINE = 20
SCHEDULERS = ("uniform", "blind_oracle", "hot_then_stale", "deadline_then_stale",
              "deepest_then_stale", "shallowest_then_stale", "deadline_then_shallowest")


def _scores(name, t, needing, minority, stale, hot, time_to_query, benefit, query_ticks):
    d = minority[needing]
    s = stale[needing].astype(float)
    ttq = time_to_query[needing]
    if name == "uniform":
        return s, False
    if name == "blind_oracle":
        out = np.zeros(len(needing))
        for j, cue in enumerate(needing):
            qt = query_ticks[cue]
            lo = np.searchsorted(qt, t, side="right")
            hi = np.searchsorted(qt, t + v3.HORIZON, side="right")
            out[j] = benefit[d[j], qt[lo:hi] - t - 1].sum()
        return out, True
    if name == "hot_then_stale":
        return s + 1e6 * hot[needing], True
    if name == "deadline_then_stale":
        return np.where(ttq <= DEADLINE, 1e9 - ttq, s), True
    if name == "deepest_then_stale":
        return d * 1e6 + s, True
    if name == "shallowest_then_stale":
        return -d * 1e6 + s, True
    if name == "deadline_then_shallowest":
        return np.where(ttq <= DEADLINE, 1e9 - ttq, (100 - d) * 1e6 + s), True
    raise ValueError(name)


def simulate(name: str, seed: int, p: v3.Params, env: v3.Environment) -> dict:
    rng = np.random.default_rng([seed, 1])
    n, bits, T = p.n_cues, p.trace_bits, p.ticks
    trace = np.repeat(env.truth[:, None], bits, axis=1).astype(np.int8)
    stale = np.zeros(n, dtype=np.int64)
    since_return = np.full(n, -1, dtype=np.int64)
    query_ticks = [np.flatnonzero(env.queries == i) for i in range(n)]
    benefit = v3.repair_benefit_table(bits, p.corrupt_p)
    pointer = np.zeros(n, dtype=np.int64)
    digest = hashlib.sha256()
    c = dict.fromkeys("queries correct post_n post_correct returns returns_lost scrubs harmful".split(), 0)
    for t in range(T):
        to_hot = env.to_hot[t]
        if to_hot.any():
            c["returns"] += int(to_hot.sum())
            dec = (trace[to_hot].sum(axis=1) * 2 >= bits).astype(np.int8)
            c["returns_lost"] += int((dec != env.truth[to_hot]).sum())
        hot = env.hot[t]
        since_return[to_hot] = 0
        qi = int(env.queries[t])
        since_return[since_return >= 0] += 1
        ok = int(v3.majority(trace[qi]) == env.truth[qi])
        c["queries"] += 1
        c["correct"] += ok
        if 0 <= since_return[qi] < p.post_return_window:
            c["post_n"] += 1
            c["post_correct"] += ok
        if since_return[qi] >= p.post_return_window:
            since_return[qi] = -1
        trace = np.where(env.flips[t], 1 - trace, trace).astype(np.int8)
        ones = trace.sum(axis=1)
        minority = np.minimum(ones, bits - ones)
        maj = (ones * 2 >= bits).astype(np.int8)
        needing = np.flatnonzero(minority > 0)
        chosen = []
        if len(needing):
            for i in range(n):  # advance each cue's next-query pointer past t
                qt = query_ticks[i]
                while pointer[i] < len(qt) and qt[pointer[i]] <= t:
                    pointer[i] += 1
            time_to_query = np.array([query_ticks[i][pointer[i]] - t if pointer[i] < len(query_ticks[i]) else 10**9
                                      for i in range(n)], dtype=float)
            scores, jitter = _scores(name, t, needing, minority, stale, hot, time_to_query, benefit, query_ticks)
            if jitter:
                scores = scores + 1e-12 * rng.random(len(needing))
                order = list(np.argsort(scores)[::-1])
            else:
                order = list(np.argsort(list(scores))[::-1])
            chosen = [int(needing[k]) for k in order[: p.budget]]
        digest.update(np.int64(t).tobytes())
        for cue in chosen:
            c["harmful"] += int(maj[cue] != env.truth[cue])
            bit = v3.repair_one_bit(trace[cue], rng)
            c["scrubs"] += 1
            digest.update(np.int64(cue).tobytes() + np.int64(bit).tobytes())
            stale[cue] = 0
        stale += 1
    return {"scheduler": name, "seed": seed, "repair_digest": digest.hexdigest(),
            "overall_accuracy": c["correct"] / c["queries"],
            "post_return_accuracy": c["post_correct"] / c["post_n"] if c["post_n"] else float("nan"),
            "lost_at_return_fraction": c["returns_lost"] / c["returns"] if c["returns"] else float("nan"),
            "harmful_repair_fraction": c["harmful"] / c["scrubs"] if c["scrubs"] else float("nan"),
            "scrubs": c["scrubs"]}


def _job(args):
    cfg, seed = args
    p = replace(v3.Params(), trace_bits=cfg[0], corrupt_p=cfg[1], budget=cfg[2])
    env = v3.generate_environment(seed, p)
    return cfg, [simulate(name, seed, p, env) for name in SCHEDULERS]


def validate() -> dict:
    p = replace(v3.Params(), trace_bits=9, corrupt_p=0.02, budget=3)
    checks = []
    for seed in (8, 9):
        env = v3.generate_environment(seed, p)
        for name in ("uniform", "blind_oracle"):
            ref = v3.run_one(name, seed, p, env=env)
            mine = simulate(name, seed, p, env)
            checks.append({"seed": seed, "scheduler": name,
                           "digest_match": ref["repair_digest"] == mine["repair_digest"],
                           "accuracy_match": ref["overall_accuracy"] == mine["overall_accuracy"]})
    return {"all_match": all(c["digest_match"] and c["accuracy_match"] for c in checks), "checks": checks}


def main() -> None:
    if OUT.exists():
        sys.exit(f"refusing to overwrite {OUT}")
    validation = validate()
    print(f"harness reproduces v3 uniform and blind_oracle exactly: {validation['all_match']}", flush=True)
    if not validation["all_match"]:
        OUT.write_text(json.dumps({"exploratory": True, "validation": validation}, indent=1))
        sys.exit("harness validation failed; no search run")
    with ProcessPoolExecutor(max_workers=7) as pool:
        results = list(pool.map(_job, [(cfg, s) for cfg in CONFIGS for s in SEEDS]))
    report = []
    boot = np.random.default_rng(20260914)
    for cfg in CONFIGS:
        rows = [r for c, batch in results if c == cfg for r in batch]
        by = {(r["scheduler"], r["seed"]): r for r in rows}
        print(f"\nwidth {cfg[0]} p {cfg[1]} budget {cfg[2]}  (paired vs uniform, overall recall, descriptive 95%)")
        entry = {"config": cfg, "schedulers": {}}
        for name in SCHEDULERS:
            vals = {k: float(np.nanmean([by[(name, s)][k] for s in SEEDS]))
                    for k in ("overall_accuracy", "post_return_accuracy", "lost_at_return_fraction", "harmful_repair_fraction")}
            d = np.array([by[(name, s)]["overall_accuracy"] - by[("uniform", s)]["overall_accuracy"] for s in SEEDS])
            means = d[boot.integers(0, len(d), size=(10000, len(d)))].mean(axis=1)
            lo, hi = np.quantile(means, [0.025, 0.975])
            entry["schedulers"][name] = {**vals, "diff_vs_uniform": float(d.mean()), "ci95": [float(lo), float(hi)],
                                         "seeds_positive": int((d > 0).sum())}
            print(f"  {name:<26} overall {vals['overall_accuracy']:.3f}  diff {d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] "
                  f"+{int((d > 0).sum())}/8  lost@ret {vals['lost_at_return_fraction']:.3f} "
                  f"harmful {vals['harmful_repair_fraction']:.3f}")
        report.append(entry)
    OUT.write_text(json.dumps({"exploratory": True, "seeds": SEEDS, "deadline": DEADLINE,
                               "validation": validation, "report": report}, indent=1))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
