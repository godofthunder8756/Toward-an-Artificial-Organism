"""Minimal precarious organism and exact solvers (rational arithmetic).

Organism
  Body variable e in {0..E}. A 1-bit register holds a cue c (uniform on {0,1})
  across a delay of d decision steps; fidelity f = 2*P(register == c) - 1.
  At each delay step the register is erased to a fair coin with probability
  eta(e) (e read before the energy transition), so f <- f * (1 - eta(e)).
  Each step e' = clip(e + 2*food - decay, 0, E): decay hits w.p. p_decay under
  either action; forage finds food w.p. p_food and costs kappa in objective
  units; rest finds none.

Dynamics factors
  fate  : eta(e) = (E - e) / (2E)  (machinery reliability depends on the body)
          vs eta = eta_flat         (host-guaranteed machinery, same noise scale)
  death : reaching e = 0 is absorbing with zero future reward, vs e = 0 being
          only the lowest level.

Objectives never read e unless they are the homeostatic objective `H`.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction as Fr
from functools import lru_cache
from itertools import product
from typing import Callable, Dict, List, Optional, Tuple

REST, FORAGE = 0, 1


@dataclass(frozen=True)
class Params:
    E: int = 4
    d: int = 4
    N: int = 4
    kappa: Fr = Fr(1, 200)
    p_decay: Fr = Fr(1, 2)
    p_food: Fr = Fr(1, 2)
    eta_flat: Fr = Fr(1, 4)
    fate: bool = True
    death: bool = False
    shift: Fr = Fr(0)           # reward added at every decision step while alive
    e_start: Optional[int] = None

    def eta(self, e: int) -> Fr:
        return Fr(self.E - e, 2 * self.E) if self.fate else self.eta_flat

    @property
    def start(self) -> int:
        return self.E if self.e_start is None else self.e_start

    def energy_next(self, e: int, a: int) -> List[Tuple[int, Fr]]:
        """e' = clip(e + 2*food - decay, 0, E): metabolic decay hits w.p. p_decay
        whatever the action; foraging finds food (+2) w.p. p_food."""
        out: Dict[int, Fr] = {}
        foods = [(1, self.p_food), (0, 1 - self.p_food)] if a == FORAGE else [(0, Fr(1))]
        for food, pf in foods:
            for dec, pd in ((1, self.p_decay), (0, 1 - self.p_decay)):
                e2 = max(0, min(self.E, e + 2 * food - dec))
                out[e2] = out.get(e2, Fr(0)) + pf * pd
        return [(e2, pr) for e2, pr in sorted(out.items()) if pr]


@dataclass(frozen=True)
class Objective:
    """Report payoffs as affine functions of q = P(register == c).

    options: label -> (intercept, slope), payoff = intercept + slope * q.
    homeo: per-decision-step reward -homeo when e <= e_low (the only e-reading term).
    """
    name: str
    options: Tuple[Tuple[str, Fr, Fr], ...]
    homeo: Fr = Fr(0)
    e_low: int = 1
    needs_memory: bool = True

    def report(self, q: Fr) -> Tuple[Fr, str]:
        best = None
        for label, a, b in self.options:
            v = a + b * q
            if best is None or v > best[0]:
                best = (v, label)
        return best


def _affine(uc: Fr, uw: Fr):
    """Options 'm' (report register), 'not_m', 'const' for payoffs uc/uw."""
    return (("m", uw, uc - uw), ("not_m", uc, uw - uc), ("const", (uc + uw) / 2, Fr(0)))


def objectives() -> Dict[str, Objective]:
    one, zero = Fr(1), Fr(0)
    return {
        "T1_gain": Objective("T1_gain", _affine(one, zero)),
        "T2_penalty": Objective("T2_penalty", _affine(zero, -one)),
        "T3_signed": Objective("T3_signed", _affine(one, -one)),
        "T4_anti": Objective("T4_anti", _affine(-one, one)),
        "T5_memfree": Objective("T5_memfree", (("const", one, zero),), needs_memory=False),
        "T6_abstain": Objective("T6_abstain", (("m", Fr(-4), Fr(5)), ("abstain", zero, zero))),
        "H_homeo": Objective("H_homeo", (("const", zero, zero),), homeo=one, needs_memory=False),
    }


# ---------------------------------------------------------------------------
# Fully observed body: exact finite-horizon DP
# ---------------------------------------------------------------------------

class Solution:
    def __init__(self, p: Params, obj: Objective):
        self.p, self.obj = p, obj
        self._V: Dict[Tuple[int, int, int, Fr], Fr] = {}
        self._A: Dict[Tuple[int, int, int, Fr], Tuple[int, bool]] = {}

    def step_reward(self, e: int, a: int) -> Fr:
        r = self.p.shift - (self.p.kappa if a == FORAGE else 0)
        if self.obj.homeo and e <= self.obj.e_low:
            r -= self.obj.homeo
        return r

    def successors(self, n: int, k: int, e: int, f: Fr, a: int):
        """[(prob, next_state or None-if-dead-or-end, report_payoff)]"""
        p = self.p
        f2 = f * (1 - p.eta(e))
        out = []
        for e2, pr in p.energy_next(e, a):
            if pr == 0:
                continue
            if k + 1 < p.d:
                dead = p.death and e2 == 0
                out.append((pr, None if dead else (n, k + 1, e2, f2), Fr(0)))
            else:
                pay, _ = self.obj.report((1 + f2) / 2)
                dead = p.death and e2 == 0
                nxt = None if (dead or n + 1 >= p.N) else (n + 1, 0, e2, Fr(1))
                out.append((pr, nxt, pay))
        return out

    def q_value(self, s, a: int) -> Fr:
        n, k, e, f = s
        tot = self.step_reward(e, a)
        for pr, nxt, pay in self.successors(n, k, e, f, a):
            tot += pr * (pay + (self.value(nxt) if nxt is not None else 0))
        return tot

    def value(self, s) -> Fr:
        if s in self._V:
            return self._V[s]
        q0, q1 = self.q_value(s, REST), self.q_value(s, FORAGE)
        a = FORAGE if q1 > q0 else REST          # ties -> rest
        self._V[s] = max(q0, q1)
        self._A[s] = (a, q0 != q1)
        return self._V[s]

    def action(self, s) -> int:
        self.value(s)
        return self._A[s][0]

    @property
    def start(self):
        return (0, 0, self.p.start, Fr(1))

    def optimum(self) -> Fr:
        return self.value(self.start)


def rollout(sol: Solution, policy: Optional[Callable] = None,
            eval_obj: Optional[Objective] = None) -> Dict[str, Fr]:
    """Exact forward distribution under `policy` (default: sol's optimum).
    `eval_obj` re-scores the same behaviour under another objective with the
    report option re-chosen for that objective (reports do not move the body)."""
    p = sol.p
    scorer = Solution(p, eval_obj) if eval_obj is not None else sol
    policy = policy or sol.action
    dist = {sol.start: Fr(1)}
    stats = {"value": Fr(0), "forages": Fr(0), "energy_sum": Fr(0), "steps": Fr(0),
             "fidelity_sum": Fr(0), "reports": Fr(0)}
    while dist:
        new: Dict[Tuple, Fr] = {}
        for s, w in dist.items():
            n, k, e, f = s
            a = policy(s)
            stats["value"] += w * scorer.step_reward(e, a)
            stats["forages"] += w * a
            stats["energy_sum"] += w * e
            stats["steps"] += w
            for pr, nxt, _ in sol.successors(n, k, e, f, a):
                if k + 1 == p.d:
                    f2 = f * (1 - p.eta(e))
                    stats["value"] += w * pr * scorer.obj.report((1 + f2) / 2)[0]
                    stats["fidelity_sum"] += w * pr * f2
                    stats["reports"] += w * pr
                if nxt is not None:
                    new[nxt] = new.get(nxt, Fr(0)) + w * pr
        dist = new
    return stats


def survival(sol: Solution, policy: Optional[Callable] = None) -> Fr:
    """P(not dead by the end of the horizon) under the policy."""
    p = sol.p
    if not p.death:
        return Fr(1)
    policy = policy or sol.action
    dist = {sol.start: Fr(1)}
    alive_end = Fr(0)
    while dist:
        new: Dict[Tuple, Fr] = {}
        for s, w in dist.items():
            n, k, e, f = s
            a = policy(s)
            for e2, pr in p.energy_next(e, a):
                if pr == 0 or e2 == 0:
                    continue
                if k + 1 < p.d:
                    nxt = (n, k + 1, e2, f * (1 - p.eta(e)))
                elif n + 1 < p.N:
                    nxt = (n + 1, 0, e2, Fr(1))
                else:
                    alive_end += w * pr
                    continue
                new[nxt] = new.get(nxt, Fr(0)) + w * pr
        dist = new
    return alive_end


def summarize(sol: Solution, policy=None, eval_obj=None) -> Dict[str, Fr]:
    st = rollout(sol, policy, eval_obj)
    return {
        "value": st["value"],
        "expected_forages": st["forages"],
        "mean_energy": st["energy_sum"] / st["steps"] if st["steps"] else Fr(0),
        "mean_report_fidelity": st["fidelity_sum"] / st["reports"] if st["reports"] else Fr(0),
        "expected_reports": st["reports"],
        "survival": survival(sol, policy),
    }


def never_forage(_s) -> int:
    return REST


def all_states(sol: Solution) -> List[Tuple]:
    seen, frontier = {sol.start}, [sol.start]
    while frontier:
        s = frontier.pop()
        n, k, e, f = s
        for a in (REST, FORAGE):
            for pr, nxt, _ in sol.successors(n, k, e, f, a):
                if nxt is not None and nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
    return sorted(seen)


# ---------------------------------------------------------------------------
# Hidden body: the agent sees neither e nor food outcomes (open-loop optimum)
# ---------------------------------------------------------------------------

def blind_optimum(p: Params, obj: Objective) -> Tuple[Fr, Tuple[int, ...]]:
    """Exact optimum when e is unobserved (death must be off). With no
    e-dependent observation the information state is the action history, so
    the optimum is a maximum over the 2^(N*d) action sequences; at each report
    the option is chosen on the belief mean of q (options are affine in q)."""
    if p.death:
        raise ValueError("blind optimum is defined here for death = False")
    scorer = Solution(p, obj)
    best = None
    for seq in product((REST, FORAGE), repeat=p.N * p.d):
        dist = {(p.start, Fr(1)): Fr(1)}
        total = Fr(0)
        t = 0
        for n in range(p.N):
            for k in range(p.d):
                a = seq[t]
                t += 1
                new: Dict[Tuple[int, Fr], Fr] = {}
                for (e, f), w in dist.items():
                    total += w * scorer.step_reward(e, a)
                    f2 = f * (1 - p.eta(e))
                    for e2, pr in p.energy_next(e, a):
                        if pr:
                            new[(e2, f2)] = new.get((e2, f2), Fr(0)) + w * pr
                dist = new
            mean_f = sum(w * f for (e, f), w in dist.items())
            total += obj.report((1 + mean_f) / 2)[0]
            merged: Dict[Tuple[int, Fr], Fr] = {}
            for (e, f), w in dist.items():
                merged[(e, Fr(1))] = merged.get((e, Fr(1)), Fr(0)) + w
            dist = merged
        if best is None or total > best[0]:
            best = (total, seq)
    return best


# ---------------------------------------------------------------------------
# Scrambling intervention (viability-relative semantic information)
# ---------------------------------------------------------------------------

def scrambled(sol: Solution) -> Dict[str, Fr]:
    """Run sol's optimal policy with its body input replaced, at every step, by
    an independent draw from the time-matched marginal of e under the intact
    optimal process. The agent's own fidelity estimate is computed from the
    scrambled inputs; the true body and register evolve under the true law."""
    p, obj = sol.p, sol.obj
    if p.death:
        raise ValueError("scrambling is defined here for death = False")
    # time-matched marginals of e under the intact optimum
    marg: Dict[Tuple[int, int], Dict[int, Fr]] = {}
    dist = {sol.start: Fr(1)}
    while dist:
        new: Dict[Tuple, Fr] = {}
        for s, w in dist.items():
            n, k, e, f = s
            m = marg.setdefault((n, k), {})
            m[e] = m.get(e, Fr(0)) + w
            for pr, nxt, _ in sol.successors(n, k, e, f, sol.action(s)):
                if nxt is not None:
                    new[nxt] = new.get(nxt, Fr(0)) + w * pr
        dist = new
    stats = {"value": Fr(0), "forages": Fr(0), "fidelity_sum": Fr(0), "reports": Fr(0),
             "energy_sum": Fr(0), "steps": Fr(0)}
    # joint state: (n, k, true e, true f, believed f)
    joint = {(0, 0, p.start, Fr(1), Fr(1)): Fr(1)}
    while joint:
        new = {}
        for (n, k, e, f, fb), w in joint.items():
            tot_m = sum(marg[(n, k)].values())
            for e_obs, pm in marg[(n, k)].items():
                wm = w * pm / tot_m
                a = sol.action((n, k, e_obs, fb))
                stats["value"] += wm * sol.step_reward(e, a)
                stats["forages"] += wm * a
                stats["energy_sum"] += wm * e
                stats["steps"] += wm
                f2 = f * (1 - p.eta(e))
                fb2 = fb * (1 - p.eta(e_obs))
                for e2, pr in p.energy_next(e, a):
                    if pr == 0:
                        continue
                    if k + 1 < p.d:
                        key = (n, k + 1, e2, f2, fb2)
                        new[key] = new.get(key, Fr(0)) + wm * pr
                    else:
                        _, label = obj.report((1 + fb2) / 2)       # option chosen on belief
                        a0, b0 = next((x, y) for lab, x, y in obj.options if lab == label)
                        stats["value"] += wm * pr * (a0 + b0 * (1 + f2) / 2)  # paid on truth
                        stats["fidelity_sum"] += wm * pr * f2
                        stats["reports"] += wm * pr
                        if n + 1 < p.N:
                            key = (n + 1, 0, e2, Fr(1), Fr(1))
                            new[key] = new.get(key, Fr(0)) + wm * pr
        joint = new
    return {
        "value": stats["value"],
        "expected_forages": stats["forages"],
        "mean_energy": stats["energy_sum"] / stats["steps"],
        "mean_report_fidelity": stats["fidelity_sum"] / stats["reports"],
    }

