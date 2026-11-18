"""P1 analytic stage: does a precarious substrate give self-evaluation a referent? (exact, rational)

Additive module; grounding/model.py is unchanged and supplies the body dynamics (Params). It
extends G1's abstain task with an evidence factor and three arms, and computes the exact
optimum and the two interventions of the P1 design.

Trial n of N: a cue is stored in a 1-bit register with initial fidelity f0, drawn as F_HI or F_LO
with probability 1/2 and observed by the agent (the evidence). Over d delay steps the register is
erased to a fair coin with probability eta per step (so f <- f * (1 - eta)); the agent forages or
rests each step, exactly as in G1. At the probe it reports the register (payoff -4 + 5q, q = (1+f)/2,
so reporting pays iff f > 3/5) or abstains (payoff 0). Corruption is undetectable: the register's
content looks the same whether or not it was erased, so the agent's fidelity is a belief computed
from what it knows (f0, and under fate its body history).

Arms:
  FATE  eta = (E - e) / (2E): the register's reliability depends on the agent's own body (G1);
        task reward only.
  HOST  eta constant (host-guaranteed machinery), matched so the mean reliability per trial equals
        FATE's under FATE's optimum; task reward only.
  PAID  as HOST, plus G1's homeostatic payment (-1 per step with e <= 1): an evaluator pays for the
        body, but the register does not depend on it.

Interventions, under each arm's own optimal policy:
  drain     the agent's belief at the probe is computed as if its body had been 2 lower at every
            delay step, while the register's actual fidelity is unchanged (system manipulated,
            evidence fixed). A self-evaluator whose referent is the body abstains more and is wrong
            to; one whose referent is not the body does not change.
  evidence  every trial gets f0 = F_LO (evidence manipulated, body dynamics unchanged).

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as Fr
from functools import lru_cache
from typing import Dict, Tuple

from .model import FORAGE, REST, Params

F_HI, F_LO = Fr(1), Fr(7, 10)         # initial register fidelity for clear and unclear evidence
DRAIN = 2                             # body levels removed from the belief in the drain intervention
THRESH = Fr(3, 5)                     # report pays iff f > THRESH  (q > 4/5)
ARMS = ("FATE", "HOST", "PAID")


def report_value(f: Fr) -> Fr:
    q = (1 + f) / 2
    return max(-4 + 5 * q, Fr(0))


def reports(f: Fr) -> bool:
    return f > THRESH


class SelfEval:
    """Exact optimum of the abstain task with evidence, for one arm."""

    def __init__(self, p: Params, arm: str, eta_host: Fr = Fr(1, 4)):
        if arm not in ARMS:
            raise ValueError(arm)
        self.p, self.arm, self.eta_host = p, arm, eta_host
        self.homeo = arm == "PAID"
        self._V: Dict[Tuple, Fr] = {}
        self._A: Dict[Tuple, int] = {}

    def eta(self, e: int) -> Fr:
        return Fr(self.p.E - e, 2 * self.p.E) if self.arm == "FATE" else self.eta_host

    def step_reward(self, e: int, a: int) -> Fr:
        r = -(self.p.kappa if a == FORAGE else 0)
        if self.homeo and e <= 1:
            r -= 1
        return r

    def trial_start(self, n: int, e: int) -> Fr:
        """Value at the start of trial n with body e, before f0 is drawn."""
        if n >= self.p.N:
            return Fr(0)
        return (self.value((n, 0, e, F_HI)) + self.value((n, 0, e, F_LO))) / 2

    def q_value(self, s, a: int) -> Fr:
        n, k, e, f = s
        tot = self.step_reward(e, a)
        f2 = f * (1 - self.eta(e))
        for e2, pr in self.p.energy_next(e, a):
            if k + 1 < self.p.d:
                tot += pr * self.value((n, k + 1, e2, f2))
            else:
                tot += pr * (report_value(f2) + self.trial_start(n + 1, e2))
        return tot

    def value(self, s) -> Fr:
        if s not in self._V:
            q0, q1 = self.q_value(s, REST), self.q_value(s, FORAGE)
            self._A[s] = FORAGE if q1 > q0 else REST
            self._V[s] = max(q0, q1)
        return self._V[s]

    def action(self, s) -> int:
        self.value(s)
        return self._A[s]

    def optimum(self) -> Fr:
        return self.trial_start(0, self.p.start)


def measure(sol: SelfEval, f0_override: Fr = None, report_rule=None) -> Dict[str, Fr]:
    """Exact forward pass under sol's optimal foraging. Per probe it tracks the actual fidelity f, the
    belief b under the drain intervention, and the body. Returns the task value, the probability of
    abstaining (natural and drained), the probability of abstaining when reporting would have paid
    under drain (a selective mistake), the mean reliability prod(1 - eta), and the in-band share.
    report_rule(f0, f) overrides the report decision (for the evidence-only rival)."""
    p = sol.p
    rule = report_rule or (lambda f0, f: reports(f))
    eta_drain = (lambda e: sol.eta(max(0, e - DRAIN))) if sol.arm == "FATE" else sol.eta
    dist: Dict[Tuple, Fr] = {(p.start,): Fr(1)}            # body distribution at the start of a trial
    out = {k: Fr(0) for k in ("value", "abstain", "abstain_drain", "wrong_abstain_drain", "reliability", "forage")}
    for n in range(p.N):
        cur: Dict[Tuple, Fr] = {}
        for (e,), pr in dist.items():
            for f0 in ((f0_override,) if f0_override is not None else (F_HI, F_LO)):
                w = pr if f0_override is not None else pr / 2
                key = (e, f0, f0, f0, Fr(1))
                cur[key] = cur.get(key, Fr(0)) + w
        for k in range(p.d):
            nxt: Dict[Tuple, Fr] = {}
            for (e, f0, f, b, rel), pr in cur.items():
                a = sol.action((n, k, e, f))
                out["value"] += pr * sol.step_reward(e, a)
                out["forage"] += pr * (a == FORAGE)
                f2, b2, rel2 = f * (1 - sol.eta(e)), b * (1 - eta_drain(e)), rel * (1 - sol.eta(e))
                for e2, pe in p.energy_next(e, a):
                    key = (e2, f0, f2, b2, rel2)
                    nxt[key] = nxt.get(key, Fr(0)) + pr * pe
            cur = nxt
        dist = {}
        for (e, f0, f, b, rel), pr in cur.items():
            rep, rep_d = rule(f0, f), rule(f0, b)
            out["value"] += pr * ((-4 + 5 * (1 + f) / 2) if rep else 0)
            out["abstain"] += pr * (not rep)
            out["abstain_drain"] += pr * (not rep_d)
            out["wrong_abstain_drain"] += pr * ((not rep_d) and reports(f))
            out["reliability"] += pr * rel
            dist[(e,)] = dist.get((e,), Fr(0)) + pr
    for k in ("abstain", "abstain_drain", "wrong_abstain_drain", "reliability"):
        out[k] /= p.N
    out["forage"] /= p.N * p.d
    return out


def evidence_only_rule(sol: SelfEval):
    """The strongest first-order rival for the report decision: the best rule that uses the evidence
    (f0) but not the body history, given sol's foraging. Chooses, for each f0, report or abstain by
    the expected payoff over the body histories that the optimum produces."""
    p = sol.p
    gain = {F_HI: Fr(0), F_LO: Fr(0)}
    dist: Dict[Tuple, Fr] = {(p.start,): Fr(1)}
    for n in range(p.N):
        cur = {}
        for (e,), pr in dist.items():
            for f0 in (F_HI, F_LO):
                cur[(e, f0, f0)] = cur.get((e, f0, f0), Fr(0)) + pr / 2
        for k in range(p.d):
            nxt = {}
            for (e, f0, f), pr in cur.items():
                a = sol.action((n, k, e, f))
                f2 = f * (1 - sol.eta(e))
                for e2, pe in p.energy_next(e, a):
                    nxt[(e2, f0, f2)] = nxt.get((e2, f0, f2), Fr(0)) + pr * pe
            cur = nxt
        dist = {}
        for (e, f0, f), pr in cur.items():
            gain[f0] += pr * (-4 + 5 * (1 + f) / 2)
            dist[(e,)] = dist.get((e,), Fr(0)) + pr
    choice = {f0: g > 0 for f0, g in gain.items()}
    return lambda f0, f: choice[f0]


def matched_eta(p: Params, d: int, target: Fr) -> Fr:
    """Constant eta with (1 - eta)^d = target, as a rational within 1e-9 (bisection)."""
    lo, hi = Fr(0), Fr(1)
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 - mid) ** d > target:
            lo = mid
        else:
            hi = mid
    return Fr((lo + hi) / 2).limit_denominator(10 ** 9)


def analyse(p: Params) -> Dict[str, object]:
    """All arms at one parameter point."""
    fate = SelfEval(p, "FATE")
    mf = measure(fate)
    eta_m = matched_eta(p, p.d, mf["reliability"])
    res: Dict[str, object] = {"eta_matched": eta_m}
    for arm in ARMS:
        sol = fate if arm == "FATE" else SelfEval(p, arm, eta_m)
        nat = mf if arm == "FATE" else measure(sol)
        ev = measure(sol, f0_override=F_LO)
        rival = measure(sol, report_rule=evidence_only_rule(sol))
        v = sol.optimum()
        res[arm] = {"optimum": v, "value_check": nat["value"], "abstain": nat["abstain"],
                    "abstain_drain": nat["abstain_drain"], "drain_effect": nat["abstain_drain"] - nat["abstain"],
                    "wrong_abstain_drain": nat["wrong_abstain_drain"], "evidence_effect": ev["abstain"] - nat["abstain"],
                    "reliability": nat["reliability"], "forage_rate": nat["forage"],
                    "evidence_only_value": rival["value"], "value_of_body_for_report": v - rival["value"]}
    return res
