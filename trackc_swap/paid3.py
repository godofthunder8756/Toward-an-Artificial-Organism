"""Track C swap, option R3: a derived agent that is also paid, and a paid agent with a sparse payment.

Additive module; every earlier module is unchanged. Option R2 (TRACKC_PAID2_RESULTS.md) found
that derived regulators hold back from a second meal after an unsensed meal more than paid
regulators do, and that tying a paid agent's position to its own E does not produce this. A
derived agent differs from a paid one in two ways that R2 could not separate: its memory
depends on its own E, and it receives no payment. The payment also differs from erasure in
its statistics: it is charged at every step and with certainty, while erasure is rare and
random. R3 adds one arm for each question to option R's three.

  DPAID  own fate, as DERIVED (its own E decides its erasure and relocation), plus the same
         homeostatic payment as PAID. It differs from DERIVED only in the payment, and from
         R2's PAIDR only in whose E decides the memory erasure.
  PAIDS  replayed fate, as PAID, with a sparse payment in place of the dense one: at every
         step, with probability `lump_rate` times the SAT gain of its own E, a fixed penalty
         `lump` is charged. With lump_rate equal to the erasure rate, penalties arrive when
         an erasure of a derived agent in the same state would; with lump = pay / lump_rate
         the expected payment in every state equals PAID's. The draw comes from the world's
         own stream and is not observable.

DERIVED, YOKED and PAID are built exactly as in options R and R2 (same classes and seeding).
YOKED, PAID and PAIDS replay the gains of DERIVED. DPAID's gains are replayed to no one.
Every agent loads its own deep copy of the phase-1 state (TRACKC_SWAP_ERRATUM_1.md).

Downstream measures are option R2's (paid2.downstream2), on the frozen weights, erasure off.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .env import SwapWorld, WorldConfig, fate_gain
from .erasure import _NoEcho
from .factorial import state_from_bytes, state_to_bytes
from .paid import ArmRunner, PaidRelocWorld, load_independent
from .paid2 import downstream2
from .relocate import RelocAgent, _Relocate, run_phase1_reloc
from .train import TrainConfig

DPAID_TAG = 8                                  # world and generator streams (1, 2, 4-7 are options R and R2)
PAIDS_TAG = 9
LUMP_STREAM = 19                               # PAIDS's penalty draws


class _LumpPaid:
    """World mixin: with probability `lump_rate` times the SAT gain of the agent's own E after
    the step, a penalty `lump` is charged. The observation is unchanged."""
    lump = 0.0
    lump_rate = 0.0
    lumps = 0

    def step(self, action):
        obs, reward, done = super().step(action)
        p = np.clip(self.lump_rate * fate_gain(self.E, self.cfg), 0.0, 1.0)
        hit = self.rng_lump.random(p.shape) < p
        self.lumps += int(hit.sum())
        return obs, reward - self.lump * hit, done


class LumpRelocWorld(_LumpPaid, _Relocate, _NoEcho, SwapWorld):
    pass


class OwnPaidRunner(ArmRunner):
    """The DPAID arm: the paid world with an agent under its own fate. Built as option R's PAID
    runner with its own streams; it is driven with rollout(None), as the derived agent is."""

    def __init__(self, seed: int, wc: WorldConfig, tc: TrainConfig, pay=("gain", 1.0)):
        self.arm, self.tc, self.wc, self.gain_rule = "DPAID", tc, wc, "SAT"
        tag = DPAID_TAG
        self.world = PaidRelocWorld(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
        self.world.pay_kind, self.world.pay = pay
        torch.manual_seed(seed)
        self.agent = RelocAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


class LumpRunner(ArmRunner):
    """The PAIDS arm: replayed fate, sparse payment. lump = (rate, size)."""

    def __init__(self, seed: int, wc: WorldConfig, tc: TrainConfig, lump=(0.0, 0.0)):
        self.arm, self.tc, self.wc, self.gain_rule = "PAIDS", tc, wc, "SAT"
        tag = PAIDS_TAG
        self.world = LumpRelocWorld(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
        self.world.lump_rate, self.world.lump = lump
        self.world.rng_lump = np.random.default_rng(np.random.SeedSequence([seed, tag, LUMP_STREAM]))
        torch.manual_seed(seed)
        self.agent = RelocAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


def _evaluate3(lead: ArmRunner, own: Dict[str, ArmRunner], followers: Dict[str, ArmRunner]):
    """DERIVED and every `own` arm under their own fate; followers replay DERIVED's gains."""
    ev, gains, _ = lead.evaluate("own")
    out = {"DERIVED": ev}
    for name, r in own.items():
        out[name] = r.evaluate("own")[0]
    for name, r in followers.items():
        out[name] = r.evaluate("replay", gains)[0]
    return out


def _lockstep3(lead: ArmRunner, own: Dict[str, ArmRunner], followers: Dict[str, ArmRunner], iters: int):
    """Train `iters` updates: DERIVED and every `own` arm under their own fate, followers
    replaying DERIVED's gains. Returns per-episode in-band and rho curves for every arm."""
    runners = [("DERIVED", lead), *own.items(), *followers.items()]
    curves = {n: {"in_band": [], "rho": []} for n, _ in runners}
    for _ in range(iters):
        used, _ = lead.rollout(None, learn=True)
        for r in own.values():
            r.rollout(None, learn=True)
        for r in followers.values():
            r.rollout(used, learn=True)
        for name, r in runners:
            st = r.end_episode_if_due()
            if st is not None:
                curves[name]["in_band"].append(round(st["in_band"], 4))
                curves[name]["rho"].append(round(st["rho"], 3))
    return curves


def run_seed3(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, p2_iters, pay, lump, sizes, stages).
    pay = (kind, weight) of the dense payment (PAID, DPAID); lump = (rate, size) of the sparse one.
    sizes = (n_envs, probe episodes, causal episodes) for the downstream measures.
    stages: 1 = training and evaluation only (calibration); 2 = also the downstream measures."""
    seed, wcd, tcd, rate, p2_iters, pay, lump, sizes, stages = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    state = state_from_bytes(p1["state"])
    fate = ArmRunner("FATE", seed, wc, tc)
    own = {"DPAID": OwnPaidRunner(seed, wc, tc, pay=pay)}
    followers = {"YOKED": ArmRunner("YOKED", seed, wc, tc),
                 "PAID": ArmRunner("PAID", seed, wc, tc, paid=True, pay=pay),
                 "PAIDS": LumpRunner(seed, wc, tc, lump=lump)}
    runners = {"DERIVED": fate, **own, **followers}
    for r in runners.values():
        load_independent(r, state)
    out: Dict[str, object] = {"seed": seed, "rate": rate, "pay": list(pay), "lump": list(lump), "p2_iters": p2_iters,
                              "nofate": {"eval": p1["S-NOFATE"]["eval"],
                                         "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}}
    out["curves1"] = _lockstep3(fate, own, followers, p2_iters)
    out["lumps1"] = followers["PAIDS"].world.lumps            # penalties charged in training
    out["stage1"] = _evaluate3(fate, own, followers)
    out["relocations1"] = {k: r.world.relocations for k, r in runners.items()}
    weights = {k: {n: v.clone() for n, v in r.agent.state_dict().items()} for k, r in runners.items()}
    out["seconds_stage1"] = round(time.time() - t0, 1)
    if stages >= 2:
        n_envs, probe_eps, causal_eps = sizes
        out["downstream"] = {k: downstream2(sd, seed, rate, wcd, n_envs, probe_eps, causal_eps)
                             for k, sd in weights.items()}
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {k: state_to_bytes(sd) for k, sd in weights.items()}
    return out
