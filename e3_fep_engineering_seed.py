"""E3 engineering seed: does an uncertainty-aware (precision/UCB) local
maintenance allocator recover a dormant-then-reactivated association faster
than a matched-material-budget recency-only allocator?

See E3_REVISED_HYPOTHESIS_v1.md for the claim, causal dependency chain,
controls, and failure criteria this probes.

ENGINEERING SEED ONLY.
- Not part of the e3/ package and not covered by E3_DESIGN_FREEZE_v0_11.json.
- Not a frozen protocol, not a confirmatory run, not an E3 experiment.
- Excluded from any future confirmatory sample by construction.
- Small, fast, and meant to be thrown away or superseded, per
  NEW_AGENT_GUIDE.md Phase E ("use clearly labeled engineering seeds").

World, briefly:
- N_CUES independent binary associations, each with a fixed ground-truth bit.
- Each association is stored as TRACE_BITS redundant material bits, decoded by
  majority vote (a repetition code, the same family E3a's rival ECC uses).
  Bits corrupt independently and are readable only through the substrate: a
  scrub fixes one disagreeing bit toward the *current majority*, never toward
  a privileged ground-truth copy, so a trace that has already lost majority
  cannot be silently repaired from nowhere.
- Each cue's relevance follows an independent two-state Markov chain
  (hot/cold). Queries are drawn cue-weighted by state, so cold cues are queried
  rarely but not never. A "return" is a cold->hot transition; the post-return
  window is the discriminating measurement.
- Each tick, a shared, scarce scrub budget is spent on the cues with the
  highest policy-computed priority among those that currently need it
  (have at least one disagreeing bit). All policies compete for the same
  budget and the same substrate.

Policies compared:
- random     : reflex control, no information used.
- uniform    : round-robin by longest-since-scrubbed (matched standard method:
               ignores relevance entirely).
- recency    : priority = EMA of query frequency (sharp rival: exploitation
               only, no exploration term).
- precision  : priority = EMA of query frequency + UCB-style exploration bonus
               growing with ticks since last visit (local proxy for epistemic
               value; not full active inference).
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field

import numpy as np

N_CUES = 16
TRACE_BITS = 8
CORRUPT_P = 0.03
BUDGET_PER_TICK = 5
TICKS = 6000
P_HOT_TO_COLD = 0.02
P_COLD_TO_HOT = 0.01
RECENCY_DECAY = 0.05
UCB_C = 0.05  # scaled so the bonus is comparable to recency_ema's ~[0,1] range
              # at typical cold-state dwell times (~1/P_COLD_TO_HOT ticks)
POST_RETURN_WINDOW = 20
POLICIES = ("random", "uniform", "recency", "precision")


@dataclass
class CueState:
    truth: int
    trace: np.ndarray
    hot: bool
    ticks_since_scrub: int = 0
    ticks_since_query: int = 0
    recency_ema: float = 0.0
    ticks_since_return: int = -1  # -1 means "not in a post-return window"


def init_cues(rng: np.random.Generator) -> list[CueState]:
    cues = []
    for _ in range(N_CUES):
        truth = int(rng.integers(0, 2))
        trace = np.full(TRACE_BITS, truth, dtype=np.int8)
        hot = bool(rng.random() < 0.5)
        cues.append(CueState(truth=truth, trace=trace, hot=hot))
    return cues


def majority(trace: np.ndarray) -> int:
    return int(trace.sum() * 2 >= len(trace))


def disagreeing_bits(trace: np.ndarray) -> np.ndarray:
    maj = majority(trace)
    return np.flatnonzero(trace != maj)


def priority_score(policy: str, cue: CueState, t: int) -> float:
    if policy == "random":
        return 0.0  # tie-break handles randomness
    if policy == "uniform":
        return float(cue.ticks_since_scrub)
    if policy == "recency":
        return cue.recency_ema
    if policy == "precision":
        # Uncertainty about current relevance grows the longer a cue has gone
        # unobserved (classic staleness-as-epistemic-uncertainty proxy), so
        # this must INCREASE with ticks_since_query, not decrease. The first
        # draft of this function had the ratio inverted (see git history /
        # scratch_fep_seed_run.json for the buggy run this replaced), which
        # made the bonus largest for just-queried cues and produced a
        # spurious negative result.
        exploration_bonus = UCB_C * np.sqrt(cue.ticks_since_query)
        return cue.recency_ema + exploration_bonus
    raise ValueError(policy)


def run_one(policy: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    cues = init_cues(rng)

    correct = 0
    total_queries = 0
    post_return_correct = 0
    post_return_total = 0
    steady_correct = 0
    steady_total = 0
    scrubs_spent = 0

    for t in range(TICKS):
        # 1. relevance drift (independent two-state Markov chain per cue)
        for cue in cues:
            if cue.hot:
                if rng.random() < P_HOT_TO_COLD:
                    cue.hot = False
            else:
                if rng.random() < P_COLD_TO_HOT:
                    cue.hot = True
                    cue.ticks_since_return = 0

        # 2. query one cue, weighted by hot/cold state
        weights = np.array([1.0 if c.hot else 0.05 for c in cues])
        weights /= weights.sum()
        qi = int(rng.choice(N_CUES, p=weights))
        for i, cue in enumerate(cues):
            cue.ticks_since_query += 1
            if cue.ticks_since_return >= 0:
                cue.ticks_since_return += 1
            cue.recency_ema *= (1 - RECENCY_DECAY)
        queried = cues[qi]
        queried.ticks_since_query = 0
        queried.recency_ema += RECENCY_DECAY

        decoded = majority(queried.trace)
        is_correct = int(decoded == queried.truth)
        correct += is_correct
        total_queries += 1
        if 0 <= queried.ticks_since_return < POST_RETURN_WINDOW:
            post_return_correct += is_correct
            post_return_total += 1
        elif queried.hot:
            steady_correct += is_correct
            steady_total += 1
        if queried.ticks_since_return >= POST_RETURN_WINDOW:
            queried.ticks_since_return = -1

        # 3. corruption
        for cue in cues:
            flips = rng.random(TRACE_BITS) < CORRUPT_P
            cue.trace = np.where(flips, 1 - cue.trace, cue.trace)

        # 4. scrub budget allocation
        needing = [c for c in cues if len(disagreeing_bits(c.trace)) > 0]
        if needing:
            if policy == "random":
                order = list(rng.permutation(len(needing)))
            else:
                scores = [priority_score(policy, c, t) for c in needing]
                order = list(np.argsort(scores)[::-1])
            for idx in order[:BUDGET_PER_TICK]:
                cue = needing[idx]
                bad_bits = disagreeing_bits(cue.trace)
                bit = int(rng.choice(bad_bits))
                cue.trace[bit] = majority(cue.trace)
                cue.ticks_since_scrub = 0
                scrubs_spent += 1
        for cue in cues:
            cue.ticks_since_scrub += 1

    return {
        "policy": policy,
        "seed": seed,
        "overall_accuracy": correct / max(total_queries, 1),
        "post_return_accuracy": post_return_correct / max(post_return_total, 1),
        "post_return_n": post_return_total,
        "steady_accuracy": steady_correct / max(steady_total, 1),
        "steady_n": steady_total,
        "scrubs_spent": scrubs_spent,
    }


def summarize(rows: list[dict]) -> dict:
    out = {}
    for policy in POLICIES:
        sub = [r for r in rows if r["policy"] == policy]
        out[policy] = {
            "overall_accuracy_mean": float(np.mean([r["overall_accuracy"] for r in sub])),
            "post_return_accuracy_mean": float(np.mean([r["post_return_accuracy"] for r in sub])),
            "post_return_accuracy_ci95": _ci95([r["post_return_accuracy"] for r in sub]),
            "steady_accuracy_mean": float(np.mean([r["steady_accuracy"] for r in sub])),
            "scrubs_spent_mean": float(np.mean([r["scrubs_spent"] for r in sub])),
            "n_seeds": len(sub),
        }
    return out


def _ci95(vals: list[float]) -> list[float]:
    arr = np.array(vals)
    if len(arr) < 2:
        return [float(arr.mean()), float(arr.mean())]
    mean = arr.mean()
    se = arr.std(ddof=1) / np.sqrt(len(arr))
    return [float(mean - 1.96 * se), float(mean + 1.96 * se)]


def main():
    global N_CUES, TRACE_BITS, CORRUPT_P, BUDGET_PER_TICK, TICKS
    global P_HOT_TO_COLD, P_COLD_TO_HOT, UCB_C

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seeds", type=int, default=12, help="number of engineering seeds")
    ap.add_argument("--out", type=str, default=None, help="optional JSON output path")
    ap.add_argument("--budget", type=int, default=BUDGET_PER_TICK,
                     help="scrub-material units spendable per tick, shared across all cues")
    ap.add_argument("--trace-bits", type=int, default=TRACE_BITS,
                     help="redundant material bits per cue (repetition-code width)")
    ap.add_argument("--corrupt-p", type=float, default=CORRUPT_P,
                     help="per-bit, per-tick corruption probability")
    ap.add_argument("--ucb-c", type=float, default=UCB_C,
                     help="exploration-bonus scale for the precision policy")
    args = ap.parse_args()
    BUDGET_PER_TICK = args.budget
    TRACE_BITS = args.trace_bits
    CORRUPT_P = args.corrupt_p
    UCB_C = args.ucb_c

    # Paired seeds: every policy sees the identical relevance/query/corruption
    # stream for a given seed index, so differences reflect the allocator,
    # not an accidental difference in environment difficulty. An earlier
    # version keyed the seed off hash(policy), which CPython randomizes per
    # process by default -- that gave each policy an uncontrolled, unpaired
    # sample and produced a paradoxical result (recency losing to uniform).
    rows = []
    for s in range(args.seeds):
        for policy in POLICIES:
            rows.append(run_one(policy, seed=s))

    summary = summarize(rows)

    print(f"{'policy':<10} {'overall':>8} {'post-return':>12} {'95% CI':>18} {'steady':>8} {'scrubs':>8}")
    for policy in POLICIES:
        s = summary[policy]
        ci = s["post_return_accuracy_ci95"]
        print(
            f"{policy:<10} {s['overall_accuracy_mean']:>8.3f} "
            f"{s['post_return_accuracy_mean']:>12.3f} "
            f"[{ci[0]:.3f}, {ci[1]:.3f}]     "
            f"{s['steady_accuracy_mean']:>8.3f} {s['scrubs_spent_mean']:>8.0f}"
        )

    if args.out:
        with open(args.out, "w") as f:
            json.dump({"rows": rows, "summary": summary}, f, indent=2)
        print(f"\nWrote {args.out}")

    print(
        "\nEngineering seed only: exploratory, not a confirmatory E3 result. "
        "See E3_REVISED_HYPOTHESIS_v1.md for the failure criteria this speaks to."
    )


if __name__ == "__main__":
    main()
