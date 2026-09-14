"""E3-OB2 policies and simulator (see E3_OBSOLESCENCE_PROTOCOL_v2.md).

The environment, substrate and repair are unchanged from e3_obsolescence_world.py
(imported). Changes, following the 2026-09-14 review:

1. Target. Predict the probability that a cue is queried within the next H ticks,
   given its current silence (ticks since its last query). This is not
   "permanently obsolete".
2. Observable episodes. A silence starts at a cue's last query (or at tick 0) and
   ends at its next query. The start and end are query events the policy
   observes whatever state the memory or its repair is in. Silences still
   running at estimation time are right-censored, not dropped.
3. Identical decision rule for learned and supplied predictions: a cue is
   eligible for repair iff its predicted return probability >= cutoff c
   (a supplied policy parameter). Repair economics are unchanged.
4. Eligibility and budget are separate, and applied the same way by every
   eligibility policy:
   - eligibility: an ineligible cue receives no repair
   - budget: at most `budget` repairs per tick, one bit per cue; unused budget
     is not redirected to ineligible cues
   `ample` ignores both and is a control. A cue becomes eligible again as soon
   as its prediction rises, for example after a new query, so maintenance can
   resume. Content already lost stays lost.
5. Accounting. Each policy declares the integers and floats it retains (query
   history, estimator state, supplied tables). This state lives in protected
   host memory: a declared scaffold, not charged to the repair budget.

Policies see only ob.Observation (read-only traces, the tick and, for
depth_flag, flags) plus query identities through observe_query. The supplied
return table reaches only return_supplied* policies, through PolicyParams2.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

import e3_obsolescence_world as ob

HORIZON = 500
CUTOFF = 0.10
SILENCE_EDGES = np.array([0, 1, 2, 5, 10, 20, 50, 100, 150, 200, 300, 400, 500, 700, 1000, 1500, 2000, 3000,
                          4000, 10 ** 9])
TIME_STEP = 500
KM_BIN, KM_BINS = 10, 601          # completed-silence histogram: 10-tick bins, last bin is overflow
KM_REFRESH, KM_WARMUP_LONG = 50, 30
CALIBRATION_EVERY = 25
CALIBRATION_SILENCE_EDGES = (0, 100, 400, 1000, 2000, 10 ** 9)


@dataclass(frozen=True)
class PolicyParams2:
    n_cues: int
    trace_bits: int
    budget: int
    timeout: int | None = None
    cutoff: float = CUTOFF
    return_table: np.ndarray | None = None


def silence_bin(s: np.ndarray) -> np.ndarray:
    return np.searchsorted(SILENCE_EDGES, s, side="right") - 1


def build_return_table(w: ob.WorldParams, seeds) -> dict:
    """Supplied knowledge: P(query within HORIZON | silence bin, time bin), estimated from independent runs."""
    n_time = int(np.ceil(w.ticks / TIME_STEP))
    counts = np.zeros((n_time, len(SILENCE_EDGES) - 1))
    hits = np.zeros_like(counts)
    for seed in seeds:
        env = ob.generate_environment(seed, w)
        t = np.arange(w.ticks)
        for cue in range(w.n_cues):
            qt = np.flatnonzero(env.queries == cue)
            idx = np.searchsorted(qt, t, side="right")
            last = np.where(idx > 0, qt[np.maximum(idx - 1, 0)] if len(qt) else 0, 0)
            nxt = np.where(idx < len(qt), qt[np.minimum(idx, len(qt) - 1)] if len(qt) else 10 ** 9, 10 ** 9)
            valid = t + HORIZON < w.ticks
            tb, sb = t[valid] // TIME_STEP, silence_bin(t[valid] - last[valid])
            np.add.at(counts, (tb, sb), 1)
            np.add.at(hits, (tb, sb), (nxt[valid] - t[valid]) <= HORIZON)
    marginal = (hits.sum(axis=0) + 0.5) / (counts.sum(axis=0) + 1)
    prob = np.where(counts > 0, (hits + 0.5) / (counts + 1), marginal[None, :])
    # Final time bins have no valid horizon; carry the last estimable row forward.
    last_valid = int(np.flatnonzero(counts.sum(axis=1) > 0)[-1])
    prob[last_valid + 1:] = prob[last_valid]
    return {"prob": prob, "counts": counts, "hits": hits, "seeds": list(seeds), "horizon": HORIZON,
            "time_step": TIME_STEP, "silence_edges": SILENCE_EDGES.tolist()}


# ---------------------------------------------------------------- policies


class Policy2:
    receives_flags = False
    full_repair = False
    predicts = False

    def __init__(self, pp: PolicyParams2, rng: np.random.Generator):
        self.pp, self.rng = pp, rng
        self.last_query = np.zeros(pp.n_cues, dtype=np.int64)
        self.last_repair = np.zeros(pp.n_cues, dtype=np.int64)
        self._eligible = np.ones(pp.n_cues, dtype=bool)

    def observe_query(self, t: int, queried: int) -> None:
        self.last_query[queried] = t

    def eligible(self) -> np.ndarray:
        return self._eligible.copy()

    def state_size(self) -> dict:
        return {"integers": 2 * self.pp.n_cues, "floats": 0, "supplied_floats": 0}

    def eligibility(self, obs: ob.Observation) -> np.ndarray:
        return np.ones(self.pp.n_cues, dtype=bool)

    def choose(self, obs: ob.Observation) -> list[int]:
        self._eligible = self.eligibility(obs)
        traces = obs.traces
        ones = traces.sum(axis=1)
        depth = np.minimum(ones, traces.shape[1] - ones)
        candidates = np.flatnonzero((depth > 0) & self._eligible)
        if len(candidates) == 0:
            return []
        stale = obs.t - self.last_repair[candidates]
        order = np.lexsort([-self.rng.random(len(candidates)), -stale, -depth[candidates]])
        chosen = [int(candidates[i]) for i in order[: self.pp.budget]]
        self.last_repair[chosen] = obs.t
        return chosen


class None2(Policy2):
    def choose(self, obs):
        return []


class Ample2(Policy2):
    full_repair = True

    def choose(self, obs):
        ones = obs.traces.sum(axis=1)
        return [int(i) for i in np.flatnonzero(np.minimum(ones, obs.traces.shape[1] - ones) > 0)]


class DepthFirst2(Policy2):
    pass


class DepthFlag2(Policy2):
    receives_flags = True

    def eligibility(self, obs):
        return ~obs.obsolete_flags


class Timeout2(Policy2):
    def eligibility(self, obs):
        return (obs.t - self.last_query) <= self.pp.timeout


class ReturnSupplied(Policy2):
    """Eligible iff the supplied table's P(query within H | silence, time) >= cutoff."""

    predicts = True

    def predict_all(self, t: int) -> np.ndarray:
        table = self.pp.return_table
        tb = min(t // TIME_STEP, table.shape[0] - 1)
        return table[tb, silence_bin(t - self.last_query)]

    def eligibility(self, obs):
        return self.predict_all(obs.t) >= self.pp.cutoff

    def state_size(self):
        return {"integers": 2 * self.pp.n_cues, "floats": 0, "supplied_floats": int(self.pp.return_table.size)}


class ReturnLearned(Policy2):
    """Eligible iff a Kaplan-Meier estimate of P(return within H | silence) >= cutoff.

    Data: completed silences, from the policy's own observed queries, in 10-tick
    bins; plus every cue's ongoing silence, right-censored at the estimation
    time. The survival curve is recomputed every KM_REFRESH ticks.

    Declared assumptions:
    - Silences are exchangeable across cues and over time. The world violates
      this, because obsolescence happens only in [1000, 3000).
    - The hazard is not extrapolated: past the longest observed returns,
      survival stays flat, so predicted return tends to zero.
    - Warm-up: until 30 completed silences of at least 100 ticks have been
      seen, every cue is predicted to return (probability 1).
    """

    predicts = True
    freeze_at: int | None = None

    def __init__(self, pp, rng):
        super().__init__(pp, rng)
        self.events = np.zeros(KM_BINS)
        self.long_events = 0
        self.survival = np.ones(KM_BINS + 1)
        self.ready = False

    def observe_query(self, t, queried):
        duration = t - int(self.last_query[queried])
        learning = self.freeze_at is None or t < self.freeze_at
        if duration > 0 and learning:
            self.events[min(duration // KM_BIN, KM_BINS - 1)] += 1
            self.long_events += int(duration >= 100)
        super().observe_query(t, queried)

    def _refresh(self, t):
        if self.freeze_at is not None and t >= self.freeze_at:
            return
        ongoing = np.minimum((t - self.last_query) // KM_BIN, KM_BINS - 1)
        censored = np.bincount(ongoing, minlength=KM_BINS).astype(float)
        at_risk = np.cumsum((self.events + censored)[::-1])[::-1]
        hazard = np.divide(self.events, at_risk, out=np.zeros(KM_BINS), where=at_risk > 0)
        self.survival = np.concatenate([[1.0], np.cumprod(1 - hazard)])
        self.ready = self.long_events >= KM_WARMUP_LONG

    def predict_all(self, t: int) -> np.ndarray:
        if not self.ready:
            return np.ones(self.pp.n_cues)
        s = t - self.last_query
        k1 = np.minimum(s // KM_BIN, KM_BINS)
        k2 = np.minimum((s + HORIZON) // KM_BIN, KM_BINS)
        s1, s2 = self.survival[k1], self.survival[k2]
        return np.where(s1 > 0, 1 - s2 / np.where(s1 > 0, s1, 1), 0.0)

    def eligibility(self, obs):
        if obs.t % KM_REFRESH == 0:
            self._refresh(obs.t)
        return self.predict_all(obs.t) >= self.pp.cutoff

    def state_size(self):
        return {"integers": 2 * self.pp.n_cues + 2, "floats": KM_BINS + KM_BINS + 1, "supplied_floats": 0}


class ReturnLearnedFrozen(ReturnLearned):
    freeze_at = 1500


POLICY_CLASSES = {
    "none": None2, "ample": Ample2, "depth_first": DepthFirst2, "depth_flag": DepthFlag2,
    "timeout_2000": Timeout2, "timeout_tuned": Timeout2,
    "return_supplied": ReturnSupplied, "return_learned": ReturnLearned,
    "return_supplied_c0.05": ReturnSupplied, "return_supplied_c0.2": ReturnSupplied,
    "return_learned_c0.05": ReturnLearned, "return_learned_c0.2": ReturnLearned,
    "return_learned_frozen1500": ReturnLearnedFrozen,
}
POLICIES = tuple(POLICY_CLASSES)
CONTROL_POLICIES = ("none", "ample", "depth_first", "depth_flag")


def policy_params(name: str, w: ob.WorldParams, table: np.ndarray, tuned_timeout: int | None) -> PolicyParams2:
    cutoff = 0.05 if name.endswith("c0.05") else 0.2 if name.endswith("c0.2") else CUTOFF
    timeout = 2000 if name == "timeout_2000" else tuned_timeout if name == "timeout_tuned" else None
    return PolicyParams2(w.n_cues, w.trace_bits, w.budget, timeout=timeout, cutoff=cutoff,
                         return_table=table if name.startswith("return_supplied") else None)


# ---------------------------------------------------------------- simulator


def run_one(name: str, seed: int, w: ob.WorldParams, table: np.ndarray, tuned_timeout: int | None = None,
            env: ob.Environment | None = None, relabel: np.ndarray | None = None,
            policy_class=None) -> dict:
    env = env if env is not None else ob.generate_environment(seed, w)
    rng = np.random.default_rng([seed, 1])
    n, bits, T = w.n_cues, w.trace_bits, w.ticks
    cls = policy_class or POLICY_CLASSES[name]
    policy = cls(policy_params(name, w, table, tuned_timeout), rng)
    truth = env.truth ^ (relabel.astype(np.int8) if relabel is not None else 0)
    trace = np.repeat(env.truth[:, None], bits, axis=1).astype(np.int8)
    next_query = np.full((T, n), 10 ** 9, dtype=np.int64)  # evaluator only: next query tick after t
    for cue in range(n):
        qt = np.flatnonzero(env.queries == cue)
        idx = np.searchsorted(qt, np.arange(T), side="right")
        has = idx < len(qt)
        next_query[has, cue] = qt[idx[has]]
    since_return = np.full(n, -1, dtype=np.int64)
    elig_prev = np.ones(n, dtype=bool)
    digest = hashlib.sha256()
    n_cal_s = len(CALIBRATION_SILENCE_EDGES) - 1
    cal = {k: np.zeros((n_cal_s, 10)) for k in ("n", "sum_p", "sum_y", "sum_sq")}
    c = dict.fromkeys((
        "queries correct post_n post_correct returns returns_lost long_returns long_returns_lost "
        "returns_while_ineligible repairs repairs_obsolete repairs_to_ineligible binding_ticks unspent "
        "obsolete_cue_ticks obsolete_ineligible_ticks dormant_cue_ticks dormant_ineligible_ticks "
        "last_third_queries last_third_correct"
    ).split(), 0)

    for t in range(T):
        state = env.state[t]
        ret = np.flatnonzero(env.returns[t])
        for cue in ret:
            lost = ob.majority(trace[cue]) != truth[cue]
            c["returns"] += 1
            c["returns_lost"] += int(lost)
            c["returns_while_ineligible"] += int(not elig_prev[cue])
            if env.long_returns[t, cue]:
                c["long_returns"] += 1
                c["long_returns_lost"] += int(lost)
        since_return[ret] = 0
        since_return[since_return >= 0] += 1

        q = int(env.queries[t])
        if q >= 0:
            ok = int(ob.majority(trace[q]) == truth[q])
            c["queries"] += 1
            c["correct"] += ok
            if 0 <= since_return[q] <= w.post_return_window:
                c["post_n"] += 1
                c["post_correct"] += ok
            if since_return[q] > w.post_return_window:
                since_return[q] = -1
            if t >= 2 * T // 3:
                c["last_third_queries"] += 1
                c["last_third_correct"] += ok
            policy.observe_query(t, q)

        trace = np.where(env.flips[t], 1 - trace, trace).astype(np.int8)
        view = trace.copy()
        view.flags.writeable = False
        flags = None
        if policy.receives_flags:
            flags = state == ob.OBSOLETE
            flags.flags.writeable = False
        chosen = policy.choose(ob.Observation(t, view, flags))
        if len(set(chosen)) != len(chosen) or any(not 0 <= x < n for x in chosen):
            raise RuntimeError(f"{name}: invalid repair list at tick {t}")
        if not policy.full_repair and len(chosen) > w.budget:
            raise RuntimeError(f"{name}: budget exceeded at tick {t}")
        eligible = policy.eligible()

        ones = trace.sum(axis=1)
        depth = np.minimum(ones, bits - ones)
        damaged_eligible = int(((depth > 0) & eligible).sum())
        c["binding_ticks"] += int((depth > 0).sum() > w.budget)
        if not policy.full_repair and name != "none":
            c["unspent"] += w.budget - len(chosen)
        obsolete = state == ob.OBSOLETE
        dormant = (state == ob.SHORT) | (state == ob.LONG)
        c["obsolete_cue_ticks"] += int(obsolete.sum())
        c["obsolete_ineligible_ticks"] += int((obsolete & ~eligible).sum())
        c["dormant_cue_ticks"] += int(dormant.sum())
        c["dormant_ineligible_ticks"] += int((dormant & ~eligible).sum())

        if policy.predicts and t % CALIBRATION_EVERY == 0 and t + HORIZON < T:
            p_hat = policy.predict_all(t)
            y = (next_query[t] - t) <= HORIZON
            sb = np.searchsorted(CALIBRATION_SILENCE_EDGES, t - policy.last_query, side="right") - 1
            pb = np.minimum((p_hat * 10).astype(int), 9)
            np.add.at(cal["n"], (sb, pb), 1)
            np.add.at(cal["sum_p"], (sb, pb), p_hat)
            np.add.at(cal["sum_y"], (sb, pb), y)
            np.add.at(cal["sum_sq"], (sb, pb), (p_hat - y) ** 2)

        digest.update(np.int64(t).tobytes())
        for cue in chosen:
            if policy.full_repair:
                bad = np.flatnonzero(trace[cue] != ob.majority(trace[cue]))
                trace[cue, bad] = ob.majority(trace[cue])
                spent = len(bad)
                digest.update(np.int64(cue).tobytes() + bad.astype(np.int64).tobytes())
            else:
                bit = ob.repair_one_bit(trace[cue], rng)
                spent = 1
                digest.update(np.int64(cue).tobytes() + np.int64(bit).tobytes())
                c["repairs_to_ineligible"] += int(not eligible[cue])
            c["repairs"] += spent
            c["repairs_obsolete"] += spent * int(obsolete[cue])
        elig_prev = eligible

    def rate(a, b):
        return c[a] / c[b] if c[b] else float("nan")

    return {
        "policy": name, "seed": seed, "env_digest": env.digest, "repair_digest": digest.hexdigest(),
        "overall_accuracy": rate("correct", "queries"),
        "post_return_accuracy": rate("post_correct", "post_n"),
        "last_third_accuracy": rate("last_third_correct", "last_third_queries"),
        "lost_at_return_fraction": rate("returns_lost", "returns"),
        "long_return_lost_fraction": rate("long_returns_lost", "long_returns"),
        "mistaken_abandonment_fraction": rate("returns_while_ineligible", "returns"),
        "obsolete_repair_share": rate("repairs_obsolete", "repairs"),
        "repairs_per_tick": c["repairs"] / T,
        "unspent_per_tick": c["unspent"] / T,
        "binding_fraction": c["binding_ticks"] / T,
        "relinquished_obsolete_fraction": rate("obsolete_ineligible_ticks", "obsolete_cue_ticks"),
        "ineligible_dormant_fraction": rate("dormant_ineligible_ticks", "dormant_cue_ticks"),
        "state_size": policy.state_size(),
        "calibration": {k: v.tolist() for k, v in cal.items()},
        **c,
    }
