"""E3-OB1 obsolescence world (exploratory side branch; see E3_OBSOLESCENCE_PROTOCOL_v1.md).

Substrate and repair are the confirmed binary-trace rules of
e3_fep_engineering_seed_v4.py:
- each cue stores its truth as TRACE_BITS copies (odd width)
- decode is majority vote
- each copy flips with probability corrupt_p per tick
- one repair sets one disagreeing copy to the current majority, never reading truth

New world rules, declared because they create unequal future consequences:
- Relevance states per cue: HOT (query weight 1), SHORT dormancy (weight
  short_query_weight), LONG dormancy (weight 0, silent) and OBSOLETE (weight 0,
  absorbing).
- A HOT cue goes dormant with p_hot_to_cold per tick. The episode is LONG with
  p_long_dormancy, otherwise SHORT.
- A SHORT cue returns with p_return_short per tick; a LONG cue with p_return_long.
- Exactly n_obsolete cues, chosen at random, become OBSOLETE at a tick drawn
  uniformly from [obsolete_start, obsolete_end). They are never queried again.
  Silent LONG dormancy looks the same as obsolescence until the cue returns.
- One query per tick, drawn by weight. If every weight is zero, there is no query.

Information interface, enforced structurally. The simulator gives a policy only:
- observe_query(t, queried): the tick and which cue was queried (never correctness)
- choose(Observation): a read-only copy of the current traces, the tick, and,
  only for policies that declare receives_flags, the current OBSOLETE flags
Policies are constructed from PolicyParams (size and budget) and their own
generator. Truth, relevance states, future events and the environment object are
never passed to them.

Environment randomness comes from default_rng([seed, 0]) with a fixed number of
draws per tick, so every policy replays the same environment. Policy and repair
randomness come from default_rng([seed, 1]).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

HOT, SHORT, LONG, OBSOLETE = 0, 1, 2, 3


@dataclass(frozen=True)
class WorldParams:
    n_cues: int = 24
    trace_bits: int = 9
    corrupt_p: float = 0.02
    budget: int = 3
    ticks: int = 6000
    p_hot_to_cold: float = 0.02
    p_long_dormancy: float = 0.2
    p_return_short: float = 0.01
    p_return_long: float = 1 / 800
    short_query_weight: float = 0.05
    n_obsolete: int = 12
    obsolete_start: int = 1000
    obsolete_end: int = 3000
    post_return_window: int = 20

    def __post_init__(self):
        if self.trace_bits % 2 == 0:
            raise ValueError("odd trace widths only")
        if not 0 <= self.n_obsolete <= self.n_cues:
            raise ValueError("n_obsolete out of range")
        if not 0 < self.obsolete_start < self.obsolete_end <= self.ticks:
            raise ValueError("obsolescence window out of range")


@dataclass(frozen=True)
class PolicyParams:
    n_cues: int
    trace_bits: int
    budget: int


@dataclass(frozen=True)
class Observation:
    t: int
    traces: np.ndarray
    obsolete_flags: np.ndarray | None


@dataclass
class Environment:
    truth: np.ndarray
    state: np.ndarray
    returns: np.ndarray
    long_returns: np.ndarray
    obsolete_at: np.ndarray
    queries: np.ndarray
    flips: np.ndarray
    digest: str


def generate_environment(seed: int, w: WorldParams) -> Environment:
    rng = np.random.default_rng([seed, 0])
    n, bits, T = w.n_cues, w.trace_bits, w.ticks
    truth = rng.integers(0, 2, n).astype(np.int8)
    now = np.where(rng.random(n) < 0.5, HOT, SHORT).astype(np.int8)
    obsolete_cues = rng.choice(n, w.n_obsolete, replace=False)
    obsolete_at = np.full(n, -1, dtype=np.int64)
    obsolete_at[obsolete_cues] = rng.integers(w.obsolete_start, w.obsolete_end, w.n_obsolete)

    state = np.zeros((T, n), dtype=np.int8)
    returns = np.zeros((T, n), dtype=bool)
    long_returns = np.zeros((T, n), dtype=bool)
    queries = np.full(T, -1, dtype=np.int64)
    flips = np.zeros((T, n, bits), dtype=bool)
    digest = hashlib.sha256()
    for t in range(T):
        r, r_type, u = rng.random(n), rng.random(n), rng.random()
        f = rng.random((n, bits)) < w.corrupt_p
        new = now.copy()
        go_cold = (now == HOT) & (r < w.p_hot_to_cold)
        new[go_cold & (r_type < w.p_long_dormancy)] = LONG
        new[go_cold & (r_type >= w.p_long_dormancy)] = SHORT
        back_short = (now == SHORT) & (r < w.p_return_short)
        back_long = (now == LONG) & (r < w.p_return_long)
        new[back_short | back_long] = HOT
        new[obsolete_at == t] = OBSOLETE
        ret = (back_short | back_long) & (new == HOT)
        weights = np.where(new == HOT, 1.0, np.where(new == SHORT, w.short_query_weight, 0.0))
        total = weights.sum()
        if total > 0:
            q = int(np.searchsorted(np.cumsum(weights) / total, u, side="right"))
            q = min(q, n - 1)
            if weights[q] == 0:
                q = int(np.flatnonzero(weights)[-1])
            queries[t] = q
        state[t], returns[t], long_returns[t], flips[t] = new, ret, ret & back_long, f
        digest.update(new.tobytes())
        digest.update(np.int64(queries[t]).tobytes())
        digest.update(np.packbits(f).tobytes())
        now = new
    return Environment(truth, state, returns, long_returns, obsolete_at, queries, flips, digest.hexdigest())


def majority(trace: np.ndarray) -> int:
    return int(trace.sum() * 2 >= len(trace))


def repair_one_bit(trace: np.ndarray, rng: np.random.Generator) -> int:
    bad = np.flatnonzero(trace != majority(trace))
    if len(bad) == 0:
        return -1
    bit = int(rng.choice(bad))
    trace[bit] = majority(trace)
    return bit


# ---------------------------------------------------------------- policies


class Policy:
    """Base policy. Subclasses see only what the simulator passes in."""

    receives_flags = False
    full_repair = False

    def __init__(self, pp: PolicyParams, rng: np.random.Generator):
        self.pp, self.rng = pp, rng
        self.last_query = np.zeros(pp.n_cues, dtype=np.int64)
        self.ever_queried = np.zeros(pp.n_cues, dtype=bool)
        self.last_repair = np.zeros(pp.n_cues, dtype=np.int64)
        self._deprioritized = np.zeros(pp.n_cues, dtype=bool)

    def observe_query(self, t: int, queried: int) -> None:
        self.last_query[queried] = t
        self.ever_queried[queried] = True

    def deprioritized(self) -> np.ndarray:
        return self._deprioritized.copy()

    @staticmethod
    def minority(traces: np.ndarray) -> np.ndarray:
        ones = traces.sum(axis=1)
        return np.minimum(ones, traces.shape[1] - ones)

    def _pick(self, obs: Observation, *keys_descending: np.ndarray) -> list[int]:
        """Top-budget damaged cues by lexicographic keys, most significant first."""
        depth = self.minority(obs.traces)
        damaged = np.flatnonzero(depth > 0)
        if len(damaged) == 0:
            return []
        tiebreak = self.rng.random(len(damaged))
        # np.lexsort sorts ascending by the LAST key; negate for descending order.
        order = np.lexsort([-tiebreak] + [-np.asarray(k, dtype=float)[damaged] for k in reversed(keys_descending)])
        chosen = [int(damaged[i]) for i in order[: self.pp.budget]]
        self.last_repair[chosen] = obs.t
        return chosen

    def choose(self, obs: Observation) -> list[int]:
        raise NotImplementedError


class NonePolicy(Policy):
    def choose(self, obs):
        return []


class AmplePolicy(Policy):
    full_repair = True

    def choose(self, obs):
        return [int(i) for i in np.flatnonzero(self.minority(obs.traces) > 0)]


class UniformPolicy(Policy):
    def choose(self, obs):
        return self._pick(obs, obs.t - self.last_repair)


class RecencyPolicy(Policy):
    decay = 0.05

    def __init__(self, pp, rng):
        super().__init__(pp, rng)
        self.ema = np.zeros(pp.n_cues)

    def observe_query(self, t, queried):
        super().observe_query(t, queried)
        self.ema *= 1 - self.decay
        self.ema[queried] += self.decay

    def choose(self, obs):
        return self._pick(obs, self.ema)


class DepthFirstPolicy(Policy):
    def choose(self, obs):
        return self._pick(obs, self.minority(obs.traces), obs.t - self.last_repair)


class DepthFlagPolicy(Policy):
    """Depth triage that is told which cues are currently obsolete."""

    receives_flags = True

    def choose(self, obs):
        self._deprioritized = obs.obsolete_flags.copy()
        return self._pick(obs, ~self._deprioritized, self.minority(obs.traces), obs.t - self.last_repair)


class DepthTimeoutPolicy(Policy):
    """Depth triage that deprioritizes cues silent for longer than a fixed, hand-set timeout."""

    timeout = 400

    def choose(self, obs):
        self._deprioritized = (obs.t - self.last_query) > self.timeout
        return self._pick(obs, ~self._deprioritized, self.minority(obs.traces), obs.t - self.last_repair)


class DepthTimeout2000Policy(DepthTimeoutPolicy):
    timeout = 2000


class DepthLearnedPolicy(Policy):
    """Depth triage with a silence threshold learned from the policy's own query history.

    Every completed gap between consecutive queries of the same cue is recorded.
    Once min_gaps gaps exist, the threshold is their quantile-th empirical
    quantile, recomputed every refresh ticks. Cues silent longer than the
    threshold go to the back of the repair queue, and return to the front the
    moment they are queried. The risk level `quantile` is supplied. What is
    learned is the gap distribution, never obsolescence itself.
    """

    quantile, min_gaps, refresh = 0.99, 50, 50
    override_factor: float | None = None
    override_tick = 1500

    def __init__(self, pp, rng):
        super().__init__(pp, rng)
        self.gaps: list[int] = []
        self.threshold = np.inf

    def observe_query(self, t, queried):
        if self.ever_queried[queried]:
            self.gaps.append(t - int(self.last_query[queried]))
        super().observe_query(t, queried)

    def choose(self, obs):
        if obs.t % self.refresh == 0:
            if self.override_factor is not None and obs.t >= self.override_tick:
                if not hasattr(self, "_frozen"):
                    self._frozen = self.threshold * self.override_factor
                self.threshold = self._frozen
            elif len(self.gaps) >= self.min_gaps:
                self.threshold = float(np.quantile(self.gaps, self.quantile))
        self._deprioritized = (obs.t - self.last_query) > self.threshold
        return self._pick(obs, ~self._deprioritized, self.minority(obs.traces), obs.t - self.last_repair)


class LearnedOverrideQuarter(DepthLearnedPolicy):
    override_factor = 0.25


class LearnedOverrideFour(DepthLearnedPolicy):
    override_factor = 4.0


POLICY_CLASSES = {
    "none": NonePolicy, "ample": AmplePolicy, "uniform": UniformPolicy, "recency": RecencyPolicy,
    "depth_first": DepthFirstPolicy, "depth_flag": DepthFlagPolicy,
    "depth_timeout_400": DepthTimeoutPolicy, "depth_timeout_2000": DepthTimeout2000Policy,
    "depth_learned": DepthLearnedPolicy,
    "learned_override_x0.25": LearnedOverrideQuarter, "learned_override_x4": LearnedOverrideFour,
}
CONTROL_POLICIES = ("none", "ample", "uniform", "depth_first", "depth_flag")
POLICIES = tuple(POLICY_CLASSES)


# ---------------------------------------------------------------- simulator


def run_one(policy_name: str, seed: int, w: WorldParams, env: Environment | None = None,
            relabel: np.ndarray | None = None) -> dict:
    env = env if env is not None else generate_environment(seed, w)
    rng = np.random.default_rng([seed, 1])
    n, bits, T = w.n_cues, w.trace_bits, w.ticks
    policy = POLICY_CLASSES[policy_name](PolicyParams(n, bits, w.budget), rng)
    truth = env.truth ^ (relabel.astype(np.int8) if relabel is not None else 0)
    trace = np.repeat(env.truth[:, None], bits, axis=1).astype(np.int8)
    since_return = np.full(n, -1, dtype=np.int64)
    dep_prev = np.zeros(n, dtype=bool)
    digest = hashlib.sha256()
    gaps_realized: list[int] = []
    last_q = np.full(n, -1, dtype=np.int64)
    c = dict.fromkeys((
        "queries correct post_n post_correct returns returns_lost long_returns long_returns_lost "
        "returns_while_deprioritized repairs repairs_obsolete repairs_wasted binding_ticks "
        "obsolete_cue_ticks obsolete_deprioritized_ticks dormant_cue_ticks dormant_deprioritized_ticks "
        "live_queries_last_third live_correct_last_third"
    ).split(), 0)

    for t in range(T):
        state = env.state[t]
        ret = np.flatnonzero(env.returns[t])
        for cue in ret:
            lost = majority(trace[cue]) != truth[cue]
            c["returns"] += 1
            c["returns_lost"] += int(lost)
            c["returns_while_deprioritized"] += int(dep_prev[cue])
            if env.long_returns[t, cue]:
                c["long_returns"] += 1
                c["long_returns_lost"] += int(lost)
        since_return[ret] = 0
        since_return[since_return >= 0] += 1

        q = int(env.queries[t])
        if q >= 0:
            ok = int(majority(trace[q]) == truth[q])
            c["queries"] += 1
            c["correct"] += ok
            if 0 <= since_return[q] <= w.post_return_window:
                c["post_n"] += 1
                c["post_correct"] += ok
            if since_return[q] > w.post_return_window:
                since_return[q] = -1
            if t >= 2 * T // 3:
                c["live_queries_last_third"] += 1
                c["live_correct_last_third"] += ok
            if last_q[q] >= 0:
                gaps_realized.append(t - int(last_q[q]))
            last_q[q] = t
            policy.observe_query(t, q)

        trace = np.where(env.flips[t], 1 - trace, trace).astype(np.int8)
        view = trace.copy()
        view.flags.writeable = False
        flags = None
        if policy.receives_flags:
            flags = state == OBSOLETE
            flags.flags.writeable = False
        chosen = policy.choose(Observation(t, view, flags))
        if len(set(chosen)) != len(chosen) or any(not 0 <= cue < n for cue in chosen):
            raise RuntimeError(f"{policy_name} returned an invalid repair list at tick {t}")
        if not policy.full_repair and len(chosen) > w.budget:
            raise RuntimeError(f"{policy_name} exceeded its budget at tick {t}")

        depth = np.minimum(trace.sum(axis=1), bits - trace.sum(axis=1))
        c["binding_ticks"] += int((depth > 0).sum() > w.budget)
        dep_now = policy.deprioritized()
        obsolete = state == OBSOLETE
        dormant = (state == SHORT) | (state == LONG)
        c["obsolete_cue_ticks"] += int(obsolete.sum())
        c["obsolete_deprioritized_ticks"] += int((obsolete & dep_now).sum())
        c["dormant_cue_ticks"] += int(dormant.sum())
        c["dormant_deprioritized_ticks"] += int((dormant & dep_now).sum())

        digest.update(np.int64(t).tobytes())
        for cue in chosen:
            if policy.full_repair:
                bad = np.flatnonzero(trace[cue] != majority(trace[cue]))
                trace[cue, bad] = majority(trace[cue])
                spent = len(bad)
                digest.update(np.int64(cue).tobytes() + bad.astype(np.int64).tobytes())
            else:
                bit = repair_one_bit(trace[cue], rng)
                spent = 1
                c["repairs_wasted"] += int(bit < 0)
                digest.update(np.int64(cue).tobytes() + np.int64(bit).tobytes())
            c["repairs"] += spent
            c["repairs_obsolete"] += spent * int(obsolete[cue])
        dep_prev = dep_now

    def rate(a, b):
        return c[a] / c[b] if c[b] else float("nan")

    threshold = getattr(policy, "threshold", None)
    return {
        "policy": policy_name, "seed": seed, "env_digest": env.digest, "repair_digest": digest.hexdigest(),
        "overall_accuracy": rate("correct", "queries"),
        "post_return_accuracy": rate("post_correct", "post_n"),
        "last_third_accuracy": rate("live_correct_last_third", "live_queries_last_third"),
        "lost_at_return_fraction": rate("returns_lost", "returns"),
        "long_return_lost_fraction": rate("long_returns_lost", "long_returns"),
        "mistaken_abandonment_fraction": rate("returns_while_deprioritized", "returns"),
        "obsolete_repair_share": rate("repairs_obsolete", "repairs"),
        "repairs_per_tick": c["repairs"] / T,
        "binding_fraction": c["binding_ticks"] / T,
        "correct_relinquishment_fraction": rate("obsolete_deprioritized_ticks", "obsolete_cue_ticks"),
        "false_abandonment_exposure": rate("dormant_deprioritized_ticks", "dormant_cue_ticks"),
        "learned_threshold_final": float(threshold) if threshold is not None and np.isfinite(threshold) else float("nan"),
        "realized_gap_q99": float(np.quantile(gaps_realized, 0.99)) if gaps_realized else float("nan"),
        **c,
    }
