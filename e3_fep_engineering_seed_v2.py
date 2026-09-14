"""E3 engineering seed v2: audit build of the binary-trace maintenance toy.

ENGINEERING SEED ONLY. Exploratory side branch; not part of e3/, not covered by
E3_DESIGN_FREEZE_v0_11.json, excluded from any confirmatory sample. See
E3_BRANCH_RECORD_2026-09-14.md for lineage and E3_REVISED_HYPOTHESIS_v1.md for
the original question and its corrections.

v1 (e3_fep_engineering_seed.py) is preserved unchanged. v2 keeps v1's world
rules and the four v1 policies exactly, and changes only:

1. Random streams. v1 drew relevance transitions, queries, corruption and the
   policies' own scrub choices from ONE generator. Scrub draws depend on the
   policy and on policy-dependent trace state, so after the first tick where
   policies differ, every later environment event differed too: seeds were
   paired only at initialization. v2 draws all environment events (initial
   truths and relevance, relevance transitions, queries, corruption masks) from
   env_rng and all policy choices from policy_rng. --legacy-shared-rng restores
   v1's single stream and draw order; audit_e3_fep_seed.py checks that this
   mode reproduces v1 exactly, which is what licenses reusing v1's semantics.
2. Controls: none (no repair), ample (every disagreeing bit of every damaged
   cue repaired every tick, no budget), oracle (budgeted, privileged).
3. Instrumentation: repair frequency, harmful/tie repairs, damage exposure,
   loss at return, wrong-majority exposure by relevance state, accuracy by
   truth value, and an environment-event digest for the pairing check.
4. Paired within-seed differences with descriptive bootstrap intervals.

World rules (unchanged from v1):
- Each cue stores a binary truth as TRACE_BITS copies; decode is majority vote,
  with an exact tie decoding as 1 (v1's `sum*2 >= len`).
- Each tick, in order: relevance transitions (two-state chain per cue), one
  query drawn by relevance weight, decode and score, independent bit flips with
  probability corrupt_p, then repair.
- One repair sets one currently disagreeing bit to the trace's current
  majority. It never reads truth. Budgeted policies repair at most one bit per
  cue per tick, on at most `budget` cues.

Oracle (ceiling only, never a candidate mechanism): reads the true truth bit,
true damage and true relevance state plus the true chain parameters. It
repairs only cues whose decode is currently correct but damaged (repairing an
already-wrong majority only reinforces the error), ranked by expected query
weight over the next ORACLE_HORIZON ticks divided by the number of further
flips until decode fails. It is a greedy privileged heuristic, not a proven
optimum.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np

POLICIES = ("none", "random", "uniform", "recency", "precision", "oracle", "ample")
ORACLE_HORIZON = 50
PAIRED_COMPARISONS = (
    ("precision", "recency"),
    ("oracle", "recency"),
    ("oracle", "precision"),
    ("recency", "none"),
    ("uniform", "none"),
    ("ample", "none"),
    ("ample", "oracle"),
)
METRICS = ("post_return_accuracy", "steady_accuracy", "overall_accuracy", "cold_accuracy")


@dataclass(frozen=True)
class Params:
    n_cues: int = 16
    trace_bits: int = 8
    corrupt_p: float = 0.03
    budget: int = 5
    ticks: int = 6000
    p_hot_to_cold: float = 0.02
    p_cold_to_hot: float = 0.01
    cold_query_weight: float = 0.05
    recency_decay: float = 0.05
    ucb_c: float = 0.05
    post_return_window: int = 20
    legacy_shared_rng: bool = False


def majority(trace: np.ndarray) -> int:
    """Decode one trace row; an exact tie decodes as 1, as in v1."""
    return int(trace.sum() * 2 >= len(trace))


def disagreeing_bits(trace: np.ndarray) -> np.ndarray:
    return np.flatnonzero(trace != majority(trace))


def repair_one_bit(trace: np.ndarray, rng: np.random.Generator) -> bool:
    """Set one randomly chosen disagreeing bit to the current majority, in place.

    Reads only the trace itself, never the truth. Returns False when there is
    nothing to repair.
    """
    bad = disagreeing_bits(trace)
    if len(bad) == 0:
        return False
    bit = int(rng.choice(bad))
    trace[bit] = majority(trace)
    return True


def flips_until_failure(wrong: int, truth: int, bits: int) -> int:
    """Further wrong bits after which majority decode no longer equals truth."""
    # Decode is 1 when ones*2 >= bits. For truth 1, ones = bits - wrong; for truth 0, ones = wrong.
    fail_at = bits // 2 + 1 if truth == 1 else (bits + 1) // 2
    return fail_at - wrong


def expected_query_weight(hot: bool, p: Params, horizon: int) -> float:
    a, b = p.p_hot_to_cold, p.p_cold_to_hot
    stationary = b / (a + b)
    k = np.arange(1, horizon + 1)
    p_hot = stationary + ((1.0 if hot else 0.0) - stationary) * (1 - a - b) ** k
    return float(np.mean(p_hot + (1 - p_hot) * p.cold_query_weight))


def run_one(policy: str, seed: int, p: Params, record_events: bool = False) -> dict:
    if p.legacy_shared_rng:
        env_rng = policy_rng = np.random.default_rng(seed)
    else:
        env_rng = np.random.default_rng([seed, 0])
        policy_rng = np.random.default_rng([seed, 1])

    n, bits = p.n_cues, p.trace_bits
    truth = np.zeros(n, dtype=np.int8)
    hot = np.zeros(n, dtype=bool)
    for i in range(n):  # v1's interleaved per-cue init order
        truth[i] = int(env_rng.integers(0, 2))
        hot[i] = bool(env_rng.random() < 0.5)
    trace = np.repeat(truth[:, None], bits, axis=1).astype(np.int8)
    ticks_since_scrub = np.zeros(n, dtype=np.int64)
    ticks_since_query = np.zeros(n, dtype=np.int64)
    recency_ema = np.zeros(n)
    ticks_since_return = np.full(n, -1, dtype=np.int64)
    hot_weight_future = expected_query_weight(True, p, ORACLE_HORIZON)
    cold_weight_future = expected_query_weight(False, p, ORACLE_HORIZON)

    digest = hashlib.sha256()
    events_query = [] if record_events else None
    c = dict.fromkeys(
        (
            "queries correct post_return_n post_return_correct steady_n steady_correct "
            "cold_n cold_correct truth0_n truth0_correct truth1_n truth1_correct "
            "flips scrubs scrubs_hot scrubs_cold scrubs_harmful scrubs_at_tie "
            "hot_cue_ticks hot_wrong_ticks cold_cue_ticks cold_wrong_ticks "
            "returns returns_lost"
        ).split(),
        0,
    )

    for t in range(p.ticks):
        # 1. relevance transitions
        r = env_rng.random(n)
        to_cold = hot & (r < p.p_hot_to_cold)
        to_hot = ~hot & (r < p.p_cold_to_hot)
        if to_hot.any():
            c["returns"] += int(to_hot.sum())
            ones = trace[to_hot].sum(axis=1)
            decoded = (ones * 2 >= bits).astype(np.int8)
            c["returns_lost"] += int((decoded != truth[to_hot]).sum())
        hot = (hot & ~to_cold) | to_hot
        ticks_since_return[to_hot] = 0

        # 2. query, decode, score
        weights = np.where(hot, 1.0, p.cold_query_weight)
        weights = weights / weights.sum()
        qi = int(env_rng.choice(n, p=weights))
        ticks_since_query += 1
        ticks_since_return[ticks_since_return >= 0] += 1
        recency_ema *= 1 - p.recency_decay
        ticks_since_query[qi] = 0
        recency_ema[qi] += p.recency_decay

        ok = int(majority(trace[qi]) == truth[qi])
        c["queries"] += 1
        c["correct"] += ok
        c[f"truth{int(truth[qi])}_n"] += 1
        c[f"truth{int(truth[qi])}_correct"] += ok
        if 0 <= ticks_since_return[qi] < p.post_return_window:
            c["post_return_n"] += 1
            c["post_return_correct"] += ok
        elif hot[qi]:
            c["steady_n"] += 1
            c["steady_correct"] += ok
        if not hot[qi]:
            c["cold_n"] += 1
            c["cold_correct"] += ok
        if ticks_since_return[qi] >= p.post_return_window:
            ticks_since_return[qi] = -1

        # 3. corruption (mask drawn independent of trace state)
        flips = env_rng.random((n, bits)) < p.corrupt_p
        c["flips"] += int(flips.sum())
        trace = np.where(flips, 1 - trace, trace).astype(np.int8)

        digest.update(hot.tobytes())
        digest.update(np.int64(qi).tobytes())
        digest.update(np.packbits(flips).tobytes())
        if record_events:
            events_query.append(qi)

        # 4. repair
        ones = trace.sum(axis=1)
        maj = (ones * 2 >= bits).astype(np.int8)
        damaged = (trace != maj[:, None]).any(axis=1)
        chosen: list[int] = []
        if policy == "ample":
            chosen = list(np.flatnonzero(damaged))
        elif policy != "none":
            needing = np.flatnonzero(damaged)
            if len(needing):
                if policy == "random":
                    order = list(policy_rng.permutation(len(needing)))
                elif policy == "oracle":
                    wrong = (trace[needing] != truth[needing, None]).sum(axis=1)
                    scores, eligible = [], []
                    for j, cue in enumerate(needing):
                        margin = flips_until_failure(int(wrong[j]), int(truth[cue]), bits)
                        if maj[cue] == truth[cue] and margin > 0:
                            eligible.append(j)
                            w = hot_weight_future if hot[cue] else cold_weight_future
                            scores.append(w / margin + 1e-9 * policy_rng.random())
                    order = [eligible[k] for k in np.argsort(scores)[::-1]]
                else:
                    if policy == "uniform":
                        scores = ticks_since_scrub[needing].astype(float)
                    elif policy == "recency":
                        scores = recency_ema[needing]
                    elif policy == "precision":
                        scores = recency_ema[needing] + p.ucb_c * np.sqrt(ticks_since_query[needing])
                    else:
                        raise ValueError(policy)
                    order = list(np.argsort(list(scores))[::-1])
                chosen = [int(needing[k]) for k in order[: p.budget]]

        for cue in chosen:
            if maj[cue] != truth[cue]:
                c["scrubs_harmful"] += 1
            if ones[cue] * 2 == bits:
                c["scrubs_at_tie"] += 1
            if hot[cue]:
                c["scrubs_hot"] += 1
            else:
                c["scrubs_cold"] += 1
            if policy == "ample":
                bad = disagreeing_bits(trace[cue])
                trace[cue, bad] = majority(trace[cue])
                c["scrubs"] += len(bad)
            else:
                repair_one_bit(trace[cue], policy_rng)
                c["scrubs"] += 1
            ticks_since_scrub[cue] = 0
        ticks_since_scrub += 1

        wrong_now = (trace.sum(axis=1) * 2 >= bits).astype(np.int8) != truth
        c["hot_cue_ticks"] += int(hot.sum())
        c["hot_wrong_ticks"] += int((wrong_now & hot).sum())
        c["cold_cue_ticks"] += int((~hot).sum())
        c["cold_wrong_ticks"] += int((wrong_now & ~hot).sum())

    def rate(num: str, den: str) -> float:
        return c[num] / c[den] if c[den] else float("nan")

    row = {
        "policy": policy,
        "seed": seed,
        "env_digest": digest.hexdigest(),
        "overall_accuracy": rate("correct", "queries"),
        "post_return_accuracy": rate("post_return_correct", "post_return_n"),
        "steady_accuracy": rate("steady_correct", "steady_n"),
        "cold_accuracy": rate("cold_correct", "cold_n"),
        "truth0_accuracy": rate("truth0_correct", "truth0_n"),
        "truth1_accuracy": rate("truth1_correct", "truth1_n"),
        "hot_wrong_fraction": rate("hot_wrong_ticks", "hot_cue_ticks"),
        "cold_wrong_fraction": rate("cold_wrong_ticks", "cold_cue_ticks"),
        "lost_at_return_fraction": rate("returns_lost", "returns"),
        "repairs_per_hot_cue_tick": rate("scrubs_hot", "hot_cue_ticks"),
        "repairs_per_cold_cue_tick": rate("scrubs_cold", "cold_cue_ticks"),
        "harmful_repair_fraction": rate("scrubs_harmful", "scrubs"),
        "tie_repair_fraction": rate("scrubs_at_tie", "scrubs"),
        **c,
    }
    if record_events:
        row["events_query"] = events_query
    return row


def _bootstrap_ci(values: np.ndarray, reps: int = 10000, seed: int = 20260914) -> list[float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(values), size=(reps, len(values)))
    means = values[idx].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def paired_differences(rows: list[dict]) -> dict:
    by = {(r["policy"], r["seed"]): r for r in rows}
    seeds = sorted({r["seed"] for r in rows})
    out = {}
    for a, b in PAIRED_COMPARISONS:
        for metric in METRICS:
            d = np.array([by[(a, s)][metric] - by[(b, s)][metric] for s in seeds])
            d = d[~np.isnan(d)]
            out[f"{a}-{b}:{metric}"] = {
                "mean": float(d.mean()),
                "ci95_bootstrap_descriptive": _bootstrap_ci(d),
                "seeds_positive": int((d > 0).sum()),
                "seeds_negative": int((d < 0).sum()),
                "n_seeds": int(len(d)),
            }
    return out


def summarize(rows: list[dict]) -> dict:
    keys = [k for k, v in rows[0].items() if isinstance(v, float)]
    out = {}
    for policy in POLICIES:
        sub = [r for r in rows if r["policy"] == policy]
        if sub:
            out[policy] = {k: float(np.nanmean([r[k] for r in sub])) for k in keys}
    return out


def _job(args):
    return run_one(*args)


def run_config(p: Params, seeds: int, workers: int) -> list[dict]:
    jobs = [(policy, s, p) for s in range(seeds) for policy in POLICIES]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_job, jobs))


def main() -> None:
    ap = argparse.ArgumentParser(description="E3 binary-trace maintenance toy, audit build (engineering seed).")
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--ticks", type=int, default=Params.ticks)
    ap.add_argument("--budget", type=int, default=Params.budget)
    ap.add_argument("--trace-bits", type=int, default=Params.trace_bits)
    ap.add_argument("--corrupt-p", type=float, default=Params.corrupt_p)
    ap.add_argument("--legacy-shared-rng", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", type=str, required=True, help="new JSON file; refuses to overwrite")
    args = ap.parse_args()

    out = Path(args.out)
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}")
    p = replace(
        Params(),
        ticks=args.ticks,
        budget=args.budget,
        trace_bits=args.trace_bits,
        corrupt_p=args.corrupt_p,
        legacy_shared_rng=args.legacy_shared_rng,
    )
    rows = run_config(p, args.seeds, args.workers)
    digests = {s: {r["env_digest"] for r in rows if r["seed"] == s} for s in range(args.seeds)}
    paired_ok = all(len(v) == 1 for v in digests.values())
    result = {
        "engineering_seed_only": True,
        "params": asdict(p),
        "oracle_horizon": ORACLE_HORIZON,
        "environment_paired_across_policies": paired_ok,
        "expected_flips_per_tick": p.n_cues * p.trace_bits * p.corrupt_p,
        "summary": summarize(rows),
        "paired_differences": paired_differences(rows),
        "rows": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1))
    print(f"wrote {out}; environment paired across policies: {paired_ok}")


if __name__ == "__main__":
    main()
