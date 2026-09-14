"""E3 allocation toy v3: maintenance by predicted recoverability and consequence.

Exploratory side branch (see E3_BRANCH_RECORD_2026-09-14.md and
E3_ALLOCATION_PROTOCOL_v1.md). Not part of e3/, not covered by the v0.11 design
freeze. v1 and v2 are preserved unchanged.

World rules are v2's, restricted to odd trace widths so that majority decode has
no ties. audit_e3_allocation.py checks that v3 reproduces v2 exactly for every
policy the two share.

Changes from v2:
- The environment (initial truths and relevance, relevance transitions, queries,
  corruption masks) is generated up front from env_rng in v2's draw order. Every
  policy for a seed replays the same arrays, so pairing holds by construction,
  and a truth-independent oracle can read future queries.
- The evaluator truth can be relabelled without changing the stored traces.
  Truth-blind policies must then make identical repair decisions (leak test).
- New policies:
  recov_supplied  ranks damaged cues by the expected number of future queries
                  whose answer one repair keeps from being lost. Inputs: its own
                  current traces, the identity of each queried cue (never
                  correctness), and the true corruption and relevance-chain rates.
  recov_learned   the same rule, but the corruption rate is estimated online
                  from its own traces: new minority bits in cues that were fully
                  consistent after the previous tick's repair. It retains one
                  integer per cue (that count), never a copy of trace bits.
  blind_oracle    ceiling: the same loss model with the true corruption rate and
                  the true future query times of each cue. It never reads truth,
                  so it cannot relearn answers by choosing when to repair.
  truth_oracle    v2's "oracle", retained only to demonstrate the timing leak.
- Instrumentation: budget-binding fraction, accuracy by thirds of the run,
  learned rate, and a digest of every repair decision.

Loss model shared by the recov policies and blind_oracle. For a cue with
current minority count d (width n, failure at f=(n+1)/2 minority bits), after r
rounds of independent flips with probability p each and no repair, each bit
differs from its present value with probability q_r=(1-(1-2p)^r)/2. Current
majority is lost when Bin(n-d, q_r) + Bin(d, 1-q_r) >= f. One repair lowers d by
one; its benefit at r rounds is P_lost(d, r) - P_lost(d-1, r). It is myopic: it
ignores later repairs. The agent treats its current majority as its memory,
because it cannot know whether that majority is already wrong.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass

import numpy as np

POLICIES = (
    "none", "random", "uniform", "recency", "precision",
    "recov_supplied", "recov_learned", "blind_oracle", "truth_oracle", "ample",
)
CONTROL_POLICIES = ("none", "random", "uniform", "blind_oracle", "ample")
BUDGETED = ("random", "uniform", "recency", "precision", "recov_supplied",
            "recov_learned", "blind_oracle", "truth_oracle")
HORIZON = 300          # rounds of future damage considered by the loss model
LEARN_REFRESH = 20     # ticks between recomputing recov_learned's tables
TRUTH_ORACLE_HORIZON = 50  # v2's oracle horizon, kept for equivalence


@dataclass(frozen=True)
class Params:
    n_cues: int = 16
    trace_bits: int = 7
    corrupt_p: float = 0.03
    budget: int = 5
    ticks: int = 6000
    p_hot_to_cold: float = 0.02
    p_cold_to_hot: float = 0.01
    cold_query_weight: float = 0.05
    recency_decay: float = 0.05
    ucb_c: float = 0.05
    post_return_window: int = 20
    initial_hot_p: float = 0.5

    def __post_init__(self):
        if self.trace_bits % 2 == 0:
            raise ValueError("v3 uses odd trace widths only (majority ties are biased)")


@dataclass
class Environment:
    truth: np.ndarray
    hot0: np.ndarray
    to_hot: np.ndarray
    hot: np.ndarray
    queries: np.ndarray
    flips: np.ndarray
    digest: str


def generate_environment(seed: int, p: Params) -> Environment:
    rng = np.random.default_rng([seed, 0])
    n, bits, T = p.n_cues, p.trace_bits, p.ticks
    truth = np.zeros(n, dtype=np.int8)
    hot0 = np.zeros(n, dtype=bool)
    for i in range(n):  # v2's interleaved init order
        truth[i] = int(rng.integers(0, 2))
        hot0[i] = bool(rng.random() < 0.5)
    to_hot = np.zeros((T, n), dtype=bool)
    hot = np.zeros((T, n), dtype=bool)
    queries = np.zeros(T, dtype=np.int64)
    flips = np.zeros((T, n, bits), dtype=bool)
    digest = hashlib.sha256()
    now = hot0.copy()
    for t in range(T):
        r = rng.random(n)
        to_cold = now & (r < p.p_hot_to_cold)
        th = ~now & (r < p.p_cold_to_hot)
        now = (now & ~to_cold) | th
        weights = np.where(now, 1.0, p.cold_query_weight)
        weights = weights / weights.sum()
        qi = int(rng.choice(n, p=weights))
        f = rng.random((n, bits)) < p.corrupt_p
        to_hot[t], hot[t], queries[t], flips[t] = th, now, qi, f
        digest.update(now.tobytes())
        digest.update(np.int64(qi).tobytes())
        digest.update(np.packbits(f).tobytes())
    return Environment(truth, hot0, to_hot, hot, queries, flips, digest.hexdigest())


def majority(trace: np.ndarray) -> int:
    return int(trace.sum() * 2 >= len(trace))


def disagreeing_bits(trace: np.ndarray) -> np.ndarray:
    return np.flatnonzero(trace != majority(trace))


def repair_one_bit(trace: np.ndarray, rng: np.random.Generator) -> int:
    """Set one random disagreeing bit to the current majority; return it or -1."""
    bad = disagreeing_bits(trace)
    if len(bad) == 0:
        return -1
    bit = int(rng.choice(bad))
    trace[bit] = majority(trace)
    return bit


def _binom_pmf(m: int, q: np.ndarray) -> np.ndarray:
    j = np.arange(m + 1)
    coef = np.array([math.comb(m, int(x)) for x in j], dtype=float)
    return coef * q[:, None] ** j * (1 - q[:, None]) ** (m - j)


def loss_probability_table(bits: int, p_flip: float, rounds: int = HORIZON) -> np.ndarray:
    """P(current majority lost) for minority count d (rows) after r = 0..rounds-1 rounds."""
    f = (bits + 1) // 2
    r = np.arange(rounds)
    q = (1 - (1 - 2 * p_flip) ** r) / 2
    table = np.zeros((f, rounds))
    for d in range(f):
        x_pmf = _binom_pmf(bits - d, q)
        y_pmf = _binom_pmf(d, 1 - q)
        y_surv = np.cumsum(y_pmf[:, ::-1], axis=1)[:, ::-1]  # [:, j] = P(Y >= j)
        for x in range(bits - d + 1):
            need = f - x
            if need <= 0:
                table[d] += x_pmf[:, x]
            elif need <= d:
                table[d] += x_pmf[:, x] * y_surv[:, need]
    return table


def repair_benefit_table(bits: int, p_flip: float, rounds: int = HORIZON) -> np.ndarray:
    loss = loss_probability_table(bits, p_flip, rounds)
    benefit = np.zeros_like(loss)
    benefit[1:] = loss[1:] - loss[:-1]
    return benefit


def query_probability_ahead(p: Params, horizon: int = HORIZON) -> tuple[np.ndarray, np.ndarray]:
    """Per-tick query probability k = 1..horizon ticks ahead, starting hot or cold."""
    a, b, cw = p.p_hot_to_cold, p.p_cold_to_hot, p.cold_query_weight
    pi = b / (a + b)
    lam = 1 - a - b
    k = np.arange(1, horizon + 1)
    expected_weight = p.n_cues * (pi + (1 - pi) * cw)
    p_hot_from_hot = pi + (1 - pi) * lam ** k
    p_hot_from_cold = pi - pi * lam ** k
    qh = (p_hot_from_hot + (1 - p_hot_from_hot) * cw) / expected_weight
    qc = (p_hot_from_cold + (1 - p_hot_from_cold) * cw) / expected_weight
    return qh, qc


def _value_by_minority(benefit: np.ndarray, qh: np.ndarray, qc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # A query k ticks ahead follows k-1 further damage rounds after this repair.
    return benefit @ qh, benefit @ qc


def _truth_oracle_weight(hot: bool, p: Params) -> float:
    a, b = p.p_hot_to_cold, p.p_cold_to_hot
    stationary = b / (a + b)
    k = np.arange(1, TRUTH_ORACLE_HORIZON + 1)
    p_hot = stationary + ((1.0 if hot else 0.0) - stationary) * (1 - a - b) ** k
    return float(np.mean(p_hot + (1 - p_hot) * p.cold_query_weight))


def _flips_until_failure(wrong: int, truth: int, bits: int) -> int:
    fail_at = bits // 2 + 1 if truth == 1 else (bits + 1) // 2
    return fail_at - wrong


def run_one(policy: str, seed: int, p: Params, relabel: np.ndarray | None = None,
            env: Environment | None = None) -> dict:
    if policy not in POLICIES:
        raise ValueError(policy)
    env = env if env is not None else generate_environment(seed, p)
    policy_rng = np.random.default_rng([seed, 1])
    n, bits, T = p.n_cues, p.trace_bits, p.ticks
    truth_eval = env.truth ^ (relabel.astype(np.int8) if relabel is not None else 0)

    trace = np.repeat(env.truth[:, None], bits, axis=1).astype(np.int8)
    ticks_since_scrub = np.zeros(n, dtype=np.int64)
    ticks_since_query = np.zeros(n, dtype=np.int64)
    recency_ema = np.zeros(n)
    ticks_since_return = np.full(n, -1, dtype=np.int64)

    a, b, cw = p.p_hot_to_cold, p.p_cold_to_hot, p.cold_query_weight
    belief_hot = np.full(n, p.initial_hot_p)
    qh, qc = query_probability_ahead(p)
    benefit_true = repair_benefit_table(bits, p.corrupt_p)
    vh_true, vc_true = _value_by_minority(benefit_true, qh, qc)
    flips_seen = opportunities = 0
    prev_minority = np.zeros(n, dtype=np.int64)
    p_hat = 0.45
    if policy == "recov_learned":
        vh_learned, vc_learned = _value_by_minority(repair_benefit_table(bits, p_hat), qh, qc)
    query_ticks = [np.flatnonzero(env.queries == i) for i in range(n)] if policy == "blind_oracle" else None
    truth_hot_w = _truth_oracle_weight(True, p)
    truth_cold_w = _truth_oracle_weight(False, p)

    repair_digest = hashlib.sha256()
    c = dict.fromkeys(
        (
            "queries correct post_return_n post_return_correct steady_n steady_correct "
            "cold_n cold_correct truth0_n truth0_correct truth1_n truth1_correct "
            "flips scrubs scrubs_hot scrubs_cold scrubs_harmful scrubs_at_tie "
            "hot_cue_ticks hot_wrong_ticks cold_cue_ticks cold_wrong_ticks "
            "returns returns_lost binding_ticks third0_n third0_correct third2_n third2_correct"
        ).split(),
        0,
    )

    for t in range(T):
        # 1. relevance transitions (replayed)
        to_hot = env.to_hot[t]
        if to_hot.any():
            c["returns"] += int(to_hot.sum())
            ones = trace[to_hot].sum(axis=1)
            decoded = (ones * 2 >= bits).astype(np.int8)
            c["returns_lost"] += int((decoded != truth_eval[to_hot]).sum())
        hot = env.hot[t]
        ticks_since_return[to_hot] = 0

        # 2. query, decode, score (the agent sees only which cue was queried)
        qi = int(env.queries[t])
        ticks_since_query += 1
        ticks_since_return[ticks_since_return >= 0] += 1
        recency_ema *= 1 - p.recency_decay
        ticks_since_query[qi] = 0
        recency_ema[qi] += p.recency_decay
        if policy in ("recov_supplied", "recov_learned"):
            prior = belief_hot * (1 - a) + (1 - belief_hot) * b
            expected_weight = float(np.sum(prior + (1 - prior) * cw))
            like_hot = np.full(n, 1 - 1 / expected_weight)
            like_cold = np.full(n, 1 - cw / expected_weight)
            like_hot[qi], like_cold[qi] = 1 / expected_weight, cw / expected_weight
            num = prior * like_hot
            belief_hot = num / (num + (1 - prior) * like_cold)

        ok = int(majority(trace[qi]) == truth_eval[qi])
        c["queries"] += 1
        c["correct"] += ok
        c[f"truth{int(truth_eval[qi])}_n"] += 1
        c[f"truth{int(truth_eval[qi])}_correct"] += ok
        third = min(3 * t // T, 2)
        if third != 1:
            c[f"third{third}_n"] += 1
            c[f"third{third}_correct"] += ok
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

        # 3. corruption (replayed)
        flips = env.flips[t]
        c["flips"] += int(flips.sum())
        trace = np.where(flips, 1 - trace, trace).astype(np.int8)

        ones = trace.sum(axis=1)
        minority = np.minimum(ones, bits - ones)
        if policy == "recov_learned":
            clean_before = prev_minority == 0
            flips_seen += int(minority[clean_before].sum())
            opportunities += bits * int(clean_before.sum())

        # 4. repair
        maj = (ones * 2 >= bits).astype(np.int8)
        damaged = minority > 0
        chosen: list[int] = []
        if policy == "ample":
            chosen = list(np.flatnonzero(damaged))
        elif policy != "none":
            needing = np.flatnonzero(damaged)
            c["binding_ticks"] += int(len(needing) > p.budget)
            if len(needing):
                if policy == "random":
                    order = list(policy_rng.permutation(len(needing)))
                elif policy == "truth_oracle":
                    wrong = (trace[needing] != truth_eval[needing, None]).sum(axis=1)
                    scores, eligible = [], []
                    for j, cue in enumerate(needing):
                        margin = _flips_until_failure(int(wrong[j]), int(truth_eval[cue]), bits)
                        if maj[cue] == truth_eval[cue] and margin > 0:
                            eligible.append(j)
                            w = truth_hot_w if hot[cue] else truth_cold_w
                            scores.append(w / margin + 1e-9 * policy_rng.random())
                    order = [eligible[k] for k in np.argsort(scores)[::-1]]
                elif policy in ("uniform", "recency", "precision"):
                    if policy == "uniform":
                        scores = ticks_since_scrub[needing].astype(float)
                    elif policy == "recency":
                        scores = recency_ema[needing]
                    else:
                        scores = recency_ema[needing] + p.ucb_c * np.sqrt(ticks_since_query[needing])
                    order = list(np.argsort(list(scores))[::-1])
                else:
                    d = minority[needing]
                    if policy == "blind_oracle":
                        scores = np.zeros(len(needing))
                        for j, cue in enumerate(needing):
                            qt = query_ticks[cue]
                            lo = np.searchsorted(qt, t, side="right")
                            hi = np.searchsorted(qt, t + HORIZON, side="right")
                            rounds = qt[lo:hi] - t - 1  # damage rounds before each future query
                            scores[j] = benefit_true[d[j], rounds].sum()
                    else:
                        vh, vc = (vh_true, vc_true) if policy == "recov_supplied" else (vh_learned, vc_learned)
                        bh = belief_hot[needing]
                        scores = bh * vh[d] + (1 - bh) * vc[d]
                    scores = scores + 1e-12 * policy_rng.random(len(needing))
                    order = list(np.argsort(scores)[::-1])
                chosen = [int(needing[k]) for k in order[: p.budget]]

        repair_digest.update(np.int64(t).tobytes())
        for cue in chosen:
            if maj[cue] != truth_eval[cue]:
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
                repair_digest.update(np.int64(cue).tobytes() + bad.astype(np.int64).tobytes())
            else:
                bit = repair_one_bit(trace[cue], policy_rng)
                c["scrubs"] += 1
                repair_digest.update(np.int64(cue).tobytes() + np.int64(bit).tobytes())
            ticks_since_scrub[cue] = 0
        ticks_since_scrub += 1

        ones_after = trace.sum(axis=1)
        if policy == "recov_learned":
            prev_minority = np.minimum(ones_after, bits - ones_after)
            if t % LEARN_REFRESH == LEARN_REFRESH - 1:
                p_hat = float(np.clip((flips_seen + 1) / (opportunities + 2), 1e-4, 0.45))
                vh_learned, vc_learned = _value_by_minority(repair_benefit_table(bits, p_hat), qh, qc)

        wrong_now = (ones_after * 2 >= bits).astype(np.int8) != truth_eval
        c["hot_cue_ticks"] += int(hot.sum())
        c["hot_wrong_ticks"] += int((wrong_now & hot).sum())
        c["cold_cue_ticks"] += int((~hot).sum())
        c["cold_wrong_ticks"] += int((wrong_now & ~hot).sum())

    def rate(num: str, den: str) -> float:
        return c[num] / c[den] if c[den] else float("nan")

    return {
        "policy": policy,
        "seed": seed,
        "env_digest": env.digest,
        "repair_digest": repair_digest.hexdigest(),
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
        "binding_fraction": c["binding_ticks"] / T if policy in BUDGETED else float("nan"),
        "accuracy_first_third": rate("third0_correct", "third0_n"),
        "accuracy_last_third": rate("third2_correct", "third2_n"),
        "p_hat_final": p_hat if policy == "recov_learned" else float("nan"),
        **c,
    }
