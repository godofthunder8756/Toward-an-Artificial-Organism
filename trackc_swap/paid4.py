"""Track C swap, option R4: a paid agent with undisturbed memory, and a derived agent that also
receives replayed erasures.

Additive module; every earlier module is unchanged. Option R3 (TRACKC_PAID3_RESULTS.md) found
that an agent whose memory depends on its own body state holds back from a second meal after an
unsensed meal, whether or not it is also paid, and that the form of the payment does not matter.
It left one alternative that the yoked design itself creates. In every arm without the
behaviour, memory was erased at times set by another agent's body. So the paid agents' weaker
suppression could be a cost of erasures unrelated to their own state, and a paid agent whose
memory is left alone might behave like a derived one. R4 adds one arm for each side of that
alternative to option R's three.

  PAID0   the same homeostatic payment as PAID, and no fate at all: its memory is never erased
          and it is never relocated. It differs from PAID only in the replayed fate.
  DNOISE  own fate, as DERIVED, plus the erasures replayed to PAID: at every step it is erased
          (and relocated) if an erasure from its own E or a replayed one would occur. With
          rate r, own gain g and replayed gain g', the probability is 1 - (1 - r g)(1 - r g').
          It differs from DERIVED only in the added replayed erasures, and receives the same
          replayed gains, in the same order, as YOKED and PAID.

DERIVED, YOKED and PAID are built exactly as in options R, R2 and R3 (same classes and
seeding). YOKED, PAID and DNOISE receive the gains of DERIVED; PAID0 receives none.
Every agent loads its own deep copy of the phase-1 state (TRACKC_SWAP_ERRATUM_1.md).

Downstream measures are option R2's (paid2.downstream2), on the frozen weights, erasure off.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict, Optional

import numpy as np
import torch

from .env import WorldConfig
from .factorial import state_from_bytes, state_to_bytes
from .paid import ArmRunner, PaidRelocWorld, load_independent
from .paid2 import downstream2
from .relocate import RelocAgent, RelocSwapWorld, run_phase1_reloc
from .train import TrainConfig

PAID0_TAG = 10                                 # world and generator streams (1, 2, 4-9 are options R to R3)
DNOISE_TAG = 12                                # 11 is the world stream key of every runner


def combine_gains(own: np.ndarray, extra: np.ndarray, rate: float) -> np.ndarray:
    """The gain g with rate * g = 1 - (1 - rate * own)(1 - rate * extra): the probability that an
    erasure from the agent's own state or an independent replayed one occurs."""
    p = 1.0 - (1.0 - np.clip(rate * own, 0.0, 1.0)) * (1.0 - np.clip(rate * extra, 0.0, 1.0))
    return (p / rate).astype(np.float32)


class _ExtraGain:
    """World mixin for DNOISE: gain() returns the agent's own SAT gain combined with a replayed
    gain. The runner sets `extra` ([L, N], one row per step of the coming rollout) and resets
    `extra_i`; each call of gain() uses the next row, and the bootstrap call after the last step
    reuses the last row, as a replaying follower does."""
    extra: Optional[np.ndarray] = None
    extra_i = 0
    extra_rate = 0.0

    def gain(self) -> np.ndarray:
        own = super().gain()
        if self.extra is None:
            return own
        row = self.extra[min(self.extra_i, len(self.extra) - 1)]
        self.extra_i += 1
        return combine_gains(own, row, self.extra_rate)


class NoisyRelocWorld(_ExtraGain, RelocSwapWorld):
    pass


def _build(runner: ArmRunner, arm: str, tag: int, world_cls, seed: int, wc: WorldConfig, tc: TrainConfig) -> None:
    """Option R's ArmRunner construction with a new arm name, stream tag and world class."""
    runner.arm, runner.tc, runner.wc, runner.gain_rule = arm, tc, wc, "SAT"
    runner.world = world_cls(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
    torch.manual_seed(seed)
    runner.agent = RelocAgent(tc.hidden, tc.kappa_f, tc.s_core)
    runner.agent.__dict__["_world"] = runner.world
    runner.opt = torch.optim.Adam(runner.agent.parameters(), lr=tc.lr)
    runner.gen = torch.Generator().manual_seed(seed * 7919 + tag)
    runner.obs = torch.from_numpy(runner.world.reset())
    runner.h = runner.agent.init_state(tc.n_envs)


class NoFatePaidRunner(ArmRunner):
    """The PAID0 arm: the paid world, gain zero at every step. Whatever gains it is handed, it
    applies none, so it can be driven and evaluated as a follower."""

    def __init__(self, seed: int, wc: WorldConfig, tc: TrainConfig, pay=("gain", 1.0)):
        _build(self, "PAID0", PAID0_TAG, PaidRelocWorld, seed, wc, tc)
        self.world.pay_kind, self.world.pay = pay

    def rollout(self, gains, learn: bool, record_h: bool = False):
        zeros = np.zeros((self.tc.rollout, self.tc.n_envs), dtype=np.float32)
        return super().rollout(zeros, learn, record_h)


class NoisyRunner(ArmRunner):
    """The DNOISE arm: own fate plus replayed erasures. The gains it is handed are the replayed
    ones; it runs under its own fate with them combined in. Task reward only."""

    def __init__(self, seed: int, wc: WorldConfig, tc: TrainConfig):
        _build(self, "DNOISE", DNOISE_TAG, NoisyRelocWorld, seed, wc, tc)
        self.world.extra_rate = tc.kappa_f

    def rollout(self, gains, learn: bool, record_h: bool = False):
        self.world.extra, self.world.extra_i = np.asarray(gains, dtype=np.float32), 0
        try:
            return super().rollout(None, learn, record_h)
        finally:
            self.world.extra = None


def _evaluate4(lead: ArmRunner, followers: Dict[str, ArmRunner]):
    """DERIVED under its own fate; every follower is handed DERIVED's gains (PAID0 applies none,
    DNOISE adds them to its own)."""
    ev, gains, _ = lead.evaluate("own")
    out = {"DERIVED": ev}
    for name, r in followers.items():
        out[name] = r.evaluate("replay", gains)[0]
    return out


def _lockstep4(lead: ArmRunner, followers: Dict[str, ArmRunner], iters: int):
    """Train `iters` updates: DERIVED under its own fate, every follower handed its gains.
    Returns per-episode in-band and rho curves for every arm."""
    runners = [("DERIVED", lead), *followers.items()]
    curves = {n: {"in_band": [], "rho": []} for n, _ in runners}
    for _ in range(iters):
        used, _ = lead.rollout(None, learn=True)
        for r in followers.values():
            r.rollout(used, learn=True)
        for name, r in runners:
            st = r.end_episode_if_due()
            if st is not None:
                curves[name]["in_band"].append(round(st["in_band"], 4))
                curves[name]["rho"].append(round(st["rho"], 3))
    return curves


def run_seed4(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, p2_iters, pay, sizes, stages).
    pay = (kind, weight) of the payment (PAID, PAID0).
    sizes = (n_envs, probe episodes, causal episodes) for the downstream measures.
    stages: 1 = training and evaluation only (calibration); 2 = also the downstream measures."""
    seed, wcd, tcd, rate, p2_iters, pay, sizes, stages = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    state = state_from_bytes(p1["state"])
    fate = ArmRunner("FATE", seed, wc, tc)
    followers = {"YOKED": ArmRunner("YOKED", seed, wc, tc),
                 "PAID": ArmRunner("PAID", seed, wc, tc, paid=True, pay=pay),
                 "PAID0": NoFatePaidRunner(seed, wc, tc, pay=pay),
                 "DNOISE": NoisyRunner(seed, wc, tc)}
    runners = {"DERIVED": fate, **followers}
    for r in runners.values():
        load_independent(r, state)
    out: Dict[str, object] = {"seed": seed, "rate": rate, "pay": list(pay), "p2_iters": p2_iters,
                              "nofate": {"eval": p1["S-NOFATE"]["eval"],
                                         "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}}
    out["curves1"] = _lockstep4(fate, followers, p2_iters)
    out["stage1"] = _evaluate4(fate, followers)
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
