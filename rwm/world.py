"""Simulated forage world, exact objective-admission certificate, closed loop.

Everything here is SIMULATED state inside a toy world (Track B exclusion X1):
no host resource, process, file or runtime is read or acted on.

World
  L in {0 den, 1 field}; energy H in {0..H_MAX}; food F ~ Bernoulli(1/2), fresh
  every step. Observations at t: oR = F if L = 1 else 0 (the den is dark and
  perfectly predictable); oH = [H <= H_LOW] (interoceptive alarm).
  Transition: L' = action; H' = min(H_MAX, H - 1 + GAIN * [L = 1 and F = 1]).
  H' <= 0 is death. A dead organism emits oR = 0, oH = 1 forever.

Objective (per-step cost in bits, exact rationals)
  exteroceptive prediction error: expected surprisal of oR under the true
  observation law = 1 bit in the field, 0 bits in the den (and when dead);
  interoceptive prediction error: surprisal of oH relative to the SUPPLIED
  setpoint prior's mode, K_INTERO bits when oH = 1, else 0.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Dict, List, Optional, Tuple

import numpy as np

from .primitives import Network

H_MAX = 5
H_LOW = 2
GAIN = 3
GAMMA = Fraction(9, 10)
K_INTERO = 3  # supplied setpoint prior: alarm costs 3 bits relative to its mode
P_FOOD = Fraction(1, 2)

LIVE = [(L, H) for L in (0, 1) for H in range(1, H_MAX + 1)]
DEAD = "dead"


def observe(L: int, H: int, F: int) -> Tuple[int, int]:
    if H <= 0:
        return 0, 1
    return (F if L == 1 else 0), int(H <= H_LOW)


def next_energy(L: int, H: int, F: int) -> int:
    return min(H_MAX, H - 1 + GAIN * int(L == 1 and F == 1))


def step_cost(L: int, H: int, w_ext: int, w_int: int) -> Fraction:
    if H <= 0:
        return Fraction(w_int * K_INTERO)
    ext = Fraction(1) if L == 1 else Fraction(0)
    intero = Fraction(K_INTERO) if H <= H_LOW else Fraction(0)
    return w_ext * ext + w_int * intero


# ---------------------------------------------------------------------------
# Exact rational linear algebra
# ---------------------------------------------------------------------------

def solve_fraction(A: List[List[Fraction]], b: List[Fraction]) -> List[Fraction]:
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        inv = 1 / M[col][col]
        M[col] = [v * inv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def policy_chain(policy: Dict[Tuple[int, int], int]):
    """Transition law over LIVE + [DEAD] for a memoryless policy (L,H) -> action."""
    states = LIVE + [DEAD]
    idx = {s: k for k, s in enumerate(states)}
    P = [[Fraction(0)] * len(states) for _ in states]
    for (L, H) in LIVE:
        a = policy[(L, H)]
        for F, pf in ((0, 1 - P_FOOD), (1, P_FOOD)):
            H2 = next_energy(L, H, F)
            dst = DEAD if H2 <= 0 else (a, H2)
            P[idx[(L, H)]][idx[dst]] += pf
    P[idx[DEAD]][idx[DEAD]] = Fraction(1)
    return states, idx, P


def evaluate_policy(policy, w_ext: int, w_int: int) -> Dict[Tuple, Fraction]:
    states, idx, P = policy_chain(policy)
    n = len(states)
    A = [[(Fraction(1) if i == j else Fraction(0)) - GAMMA * P[i][j] for j in range(n)] for i in range(n)]
    b = [step_cost(*(s if s != DEAD else (0, 0)), w_ext, w_int) for s in states]
    V = solve_fraction(A, b)
    return {s: V[idx[s]] for s in states}


def expected_lifetime(policy) -> Dict[Tuple, Fraction]:
    """Expected number of live steps before death (death is certain: finite food luck)."""
    states, idx, P = policy_chain(policy)
    live = [s for s in states if s != DEAD]
    A = [[(Fraction(1) if i == j else Fraction(0)) - P[idx[si]][idx[sj]]
          for j, sj in enumerate(live)] for i, si in enumerate(live)]
    tau = solve_fraction(A, [Fraction(1)] * len(live))
    return dict(zip(live, tau))


def all_policies() -> List[Dict[Tuple[int, int], int]]:
    return [dict(zip(LIVE, acts)) for acts in product((0, 1), repeat=len(LIVE))]


def objective_certificate(start=(0, H_MAX)) -> Dict[str, object]:
    """Exhaustive exact evaluation of all 2^8 memoryless policies under three objectives."""
    pols = all_policies()
    out: Dict[str, object] = {"n_policies": len(pols), "start": list(start),
                              "gamma": str(GAMMA), "k_intero_bits": K_INTERO,
                              "h_max": H_MAX, "h_low": H_LOW, "gain": GAIN}
    lifetimes = [expected_lifetime(p)[start] for p in pols]
    field_visit = [any(p[s] == 1 for s in LIVE) for p in pols]
    for label, (we, wi) in {"extero_only": (1, 0), "extero_plus_intero": (1, 1),
                            "intero_only": (0, 1)}.items():
        vals = [evaluate_policy(p, we, wi)[start] for p in pols]
        best = min(vals)
        opt = [k for k, v in enumerate(vals) if v == best]
        out[label] = {
            "optimal_value": str(best),
            "optimal_value_float": float(best),
            "n_optimal": len(opt),
            "optimal_lifetimes": sorted({str(lifetimes[k]) for k in opt}),
            "optimal_lifetime_float_min": float(min(lifetimes[k] for k in opt)),
            "optimal_lifetime_float_max": float(max(lifetimes[k] for k in opt)),
            "an_optimal_policy": {f"L{L}H{H}": pols[opt[0]][(L, H)] for (L, H) in LIVE},
            "all_optimal_never_forage_from_start": all(not _visits_field(pols[k], start) for k in opt),
        }
    dark = {s: 0 for s in LIVE}
    out["dark_room_lifetime"] = str(expected_lifetime(dark)[start])
    out["max_lifetime_any_policy"] = str(max(lifetimes))
    return out


def _visits_field(policy, start) -> bool:
    """Does the chain started at `start` reach L = 1 with positive probability?"""
    seen = {start}
    frontier = [start]
    while frontier:
        L, H = frontier.pop()
        if L == 1:
            return True
        a = policy[(L, H)]
        for F in (0, 1):
            H2 = next_energy(L, H, F)
            if H2 > 0 and (a, H2) not in seen:
                seen.add((a, H2))
                frontier.append((a, H2))
    return False


# ---------------------------------------------------------------------------
# Closed loop: a gate network acting in the world
# ---------------------------------------------------------------------------

def closed_loop_chain(net: Network, action_node: str = "A", respawn: bool = True,
                      init_state: int = 0):
    """Exact joint Markov chain over (agent state, L, H, F) reachable from the
    respawn configuration. Death respawns to (init_state, L=0, H=H_MAX) when
    `respawn`, else is absorbing (state 'dead')."""
    a_idx = net.index(action_node)
    start_states = [(init_state, 0, H_MAX, F) for F in (0, 1)]
    trans: Dict[Tuple, Dict[Tuple, float]] = {}
    deaths: Dict[Tuple, float] = {}
    frontier = list(start_states)
    seen = set(start_states)
    while frontier:
        st = frontier.pop()
        s, L, H, F = st
        oR, oH = observe(L, H, F)
        ps = net.step_p1(s, {"oR": oR, "oH": oH})
        nxt_dist = _state_dist(ps)
        act = (s >> a_idx) & 1
        H2 = next_energy(L, H, F)
        row: Dict[Tuple, float] = {}
        died = H2 <= 0
        deaths[st] = 1.0 if died else 0.0
        for s2, pr in nxt_dist.items():
            for F2 in (0, 1):
                dst = (init_state, 0, H_MAX, F2) if (died and respawn) else \
                    ("dead",) if died else (s2, act, H2, F2)
                row[dst] = row.get(dst, 0.0) + pr * 0.5
        trans[st] = row
        for dst in row:
            if dst != ("dead",) and dst not in seen:
                seen.add(dst)
                frontier.append(dst)
    return trans, deaths


def _state_dist(ps: List[float]) -> Dict[int, float]:
    dist = {0: 1.0}
    for i, p in enumerate(ps):
        new: Dict[int, float] = {}
        for s, w in dist.items():
            if p > 0:
                new[s | (1 << i)] = new.get(s | (1 << i), 0.0) + w * p
            if p < 1:
                new[s] = new.get(s, 0.0) + w * (1 - p)
        dist = new
    return dist


def stationary(trans: Dict[Tuple, Dict[Tuple, float]]) -> Dict[Tuple, float]:
    states = sorted(trans, key=repr)
    idx = {s: k for k, s in enumerate(states)}
    n = len(states)
    P = np.zeros((n, n))
    for s, row in trans.items():
        for d, p in row.items():
            P[idx[s], idx[d]] += p
    A = np.vstack([P.T - np.eye(n), np.ones((1, n))])
    b = np.zeros(n + 1)
    b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(A, b, rcond=None)
    resid = float(np.abs(pi @ P - pi).max())
    if resid > 1e-9 or pi.min() < -1e-9:
        raise RuntimeError(f"stationary solve failed (residual {resid})")
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()
    return {s: float(pi[idx[s]]) for s in states}


def closed_loop_summary(net: Network, action_node: str = "A") -> Dict[str, object]:
    """Lifetime (absorbing chain), stationary statistics (respawn chain)."""
    trans, deaths = closed_loop_chain(net, action_node, respawn=True)
    pi = stationary(trans)
    death_rate = sum(p * deaths[s] for s, p in pi.items())
    field = sum(p for (s, L, H, F), p in pi.items() if L == 1)
    alarm = sum(p for (s, L, H, F), p in pi.items() if H <= H_LOW)
    # absorbing chain: expected live steps from the start configuration
    t_abs, _ = closed_loop_chain(net, action_node, respawn=False)
    live = sorted(t_abs, key=repr)
    idx = {s: k for k, s in enumerate(live)}
    n = len(live)
    Q = np.zeros((n, n))
    for s, row in t_abs.items():
        for d, p in row.items():
            if d != ("dead",):
                Q[idx[s], idx[d]] += p
    tau = np.linalg.solve(np.eye(n) - Q, np.ones(n))
    start = [(0, 0, H_MAX, F) for F in (0, 1)]
    lifetime = float(np.mean([tau[idx[s]] for s in start]))
    agent_states = sorted({s for (s, L, H, F) in pi if pi[(s, L, H, F)] > 0})
    return {
        "reachable_joint_states": len(pi),
        "reachable_agent_states": len(agent_states),
        "stationary_death_rate": death_rate,
        "mean_lifetime_steps": 1.0 / death_rate if death_rate > 0 else float("inf"),
        "expected_lifetime_from_start": lifetime,
        "stationary_field_fraction": field,
        "stationary_alarm_fraction": alarm,
        "_pi": pi,
    }


def agent_state_weights(net: Network, pi: Dict[Tuple, float]) -> Dict[Tuple[int, Tuple], float]:
    """Stationary joint weight over (agent state, external-input tuple)."""
    w: Dict[Tuple[int, Tuple], float] = {}
    for (s, L, H, F), p in pi.items():
        oR, oH = observe(L, H, F)
        key = (s, tuple({"oR": oR, "oH": oH}[e] for e in net.external))
        w[key] = w.get(key, 0.0) + p
    return w
