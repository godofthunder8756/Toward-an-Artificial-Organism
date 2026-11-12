"""Track C swap, option R: derived against paid regulators.

Additive module; every earlier module is unchanged. Three agents are trained in lockstep
from the same phase-1 weights, in the v7/v8 world (echo-free, erasure also relocates):

  DERIVED  the fate agent: its own E decides its erasure; task reward only (as v7/v8 FATE);
  YOKED    replays the derived agent's erasure gains; task reward only (as v7/v8 YOKED);
  PAID     replays the same gains as YOKED; task reward plus an evaluator's homeostatic
           reward: the Track B drive-reduction reward on eating (the DRIVE objective's
           term, unchanged), times `pay`.

So PAID is a yoked agent with payment for regulation added. Its erasure history has the
same source as the yoked partner's and does not depend on its own E.

Withdrawal stage (continued training, four agents in lockstep):
  DKEEP  the derived agent, unchanged (its gains are replayed to the other three);
  DCUT   the derived agent's weights, erasure now replayed: the dependence is removed;
  PKEEP  the paid agent, unchanged;
  PCUT   the paid agent's weights, homeostatic reward removed: the payment is removed.
DCUT and PCUT are then in the same condition (replayed erasure, task reward only).

Downstream measures on the frozen stage-1 weights reuse options P and Q (probe.py,
causal.py) and add world shifts, all evaluated with erasure off.

Independent optimizers. In v2-v8 the fate and yoked agents of a pair were loaded from one
phase-1 state object. torch's Optimizer.load_state_dict does not copy tensors, so the two
agents shared Adam's step count and moment buffers (TRACKC_SWAP_ERRATUM_1.md). Here every
agent loads its own deep copy, so no optimizer state is shared between agents.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import copy
import time
from typing import Dict

import numpy as np
import torch

from .causal import run_mode, suppression
from .env import SwapWorld, WorldConfig, drive
from .erasure import _NoEcho
from .factorial import state_from_bytes, state_to_bytes
from .longrun import _restart
from .probe import decode, run_agent
from .relocate import RelocAgent, RelocRunner, RelocSwapWorld, _Relocate, run_phase1_reloc
from .train import TrainConfig

TAGS = {"FATE": 1, "YOKED": 2, "PAID": 4, "DCUT": 5, "PCUT": 6}     # 3 is NOFATE (phase 1)
SHIFTS = {"bolus_0.10": {"bolus": 0.10}, "wear_x2": {"wear": 0.002},
          "delay_10": {"intero_delay": 10}, "noise_0.05": {"intero_sd": 0.05}}


class _PaidDrive:
    """World mixin: adds `pay` times the Track B drive-reduction reward on eating to the reward.
    The observation is unchanged (the previous reward is zeroed in the echo-free world)."""
    pay = 1.0

    def step(self, action):
        e0 = self.E.copy()
        eats0 = self.stats["eats"].copy()
        obs, reward, done = super().step(action)
        ate = self.stats["eats"] > eats0
        e1 = np.minimum(1.0, e0 + self.cfg.bolus)
        reward = reward + self.pay * np.where(ate, drive(e0) - drive(e1), 0.0)
        return obs, reward, done


class PaidRelocWorld(_PaidDrive, _Relocate, _NoEcho, SwapWorld):
    pass


class ArmRunner(RelocRunner):
    """RelocRunner for a named arm of option R. FATE and YOKED keep v7's seeding (tags 1, 2)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, paid: bool = False, pay: float = 1.0):
        self.arm, self.tc, self.wc, self.gain_rule = arm, tc, wc, "SAT"
        tag = TAGS[arm]
        cls = PaidRelocWorld if paid else RelocSwapWorld
        self.world = cls(tc.n_envs, "M1", wc, np.random.SeedSequence([seed, tag, 11]))
        if paid:
            self.world.pay = pay
        torch.manual_seed(seed)
        self.agent = RelocAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


def load_independent(runner: ArmRunner, state: Dict[str, object]) -> None:
    """Load weights and optimizer state from a private deep copy, so nothing is shared."""
    runner.load_state(copy.deepcopy(state))


def _evaluate(lead: ArmRunner, followers: Dict[str, ArmRunner], lead_name: str) -> Dict[str, Dict[str, float]]:
    """Lead under its own fate; every follower replays the lead's gains."""
    ev, gains, _ = lead.evaluate("own")
    out = {lead_name: ev}
    for name, r in followers.items():
        out[name] = r.evaluate("replay", gains)[0]
    return out


def _lockstep(lead: ArmRunner, followers: Dict[str, ArmRunner], lead_name: str, iters: int):
    """Train `iters` updates: the lead under its own fate, followers replaying its gains.
    Returns per-episode in-band and rho curves for every arm."""
    curves = {n: {"in_band": [], "rho": []} for n in [lead_name, *followers]}
    for _ in range(iters):
        used, _ = lead.rollout(None, learn=True)
        for r in followers.values():
            r.rollout(used, learn=True)
        for name, r in [(lead_name, lead), *followers.items()]:
            st = r.end_episode_if_due()
            if st is not None:
                curves[name]["in_band"].append(round(st["in_band"], 4))
                curves[name]["rho"].append(round(st["rho"], 3))
    return curves


def downstream(sd, seed: int, rate: float, wcd: Dict[str, object], n_envs: int, probe_eps: int,
               causal_eps: int) -> Dict[str, object]:
    """Options P and Q measures and the world shifts for one frozen agent, erasure off."""
    wc = WorldConfig(**wcd)
    out: Dict[str, object] = {}
    intact = run_agent(sd, "M1", seed, wc, n_envs, probe_eps, False, True)
    out.update(decode(intact.pop("_rec")))
    out["intact"] = intact
    out["shuffled"] = run_agent(sd, "M1", seed, wc, n_envs, probe_eps, True, False)
    off = run_mode(sd, "M1", "SAT", rate, seed, wc, n_envs, causal_eps, "off", probe=True)
    out["suppression"] = suppression(off.pop("_rec"))
    out["base"] = off
    out["shifts"] = {name: run_mode(sd, "M1", "SAT", rate, seed, WorldConfig(**(wcd | kw)), n_envs, probe_eps, "off")
                     for name, kw in SHIFTS.items()}
    return out


def run_seed(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, p2_iters, w_iters, pay, sizes, stages).
    sizes = (n_envs, probe episodes, causal episodes) for the downstream measures.
    stages: 1 = training and evaluation only (calibration); 3 = also downstream and withdrawal."""
    seed, wcd, tcd, rate, p2_iters, w_iters, pay, sizes, stages = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    t0 = time.time()
    p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0 and (w_iters * tc.rollout) % wc.horizon == 0
    state = state_from_bytes(p1["state"])
    fate = ArmRunner("FATE", seed, wc, tc)
    yoked = ArmRunner("YOKED", seed, wc, tc)
    paid = ArmRunner("PAID", seed, wc, tc, paid=True, pay=pay)
    for r in (fate, yoked, paid):
        load_independent(r, state)
    out: Dict[str, object] = {"seed": seed, "rate": rate, "pay": pay, "p2_iters": p2_iters, "w_iters": w_iters,
                              "nofate": {"eval": p1["S-NOFATE"]["eval"],
                                         "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}}
    # stage 1: training
    out["curves1"] = _lockstep(fate, {"YOKED": yoked, "PAID": paid}, "DERIVED", p2_iters)
    out["stage1"] = _evaluate(fate, {"YOKED": yoked, "PAID": paid}, "DERIVED")
    out["relocations1"] = {"DERIVED": fate.world.relocations, "YOKED": yoked.world.relocations,
                           "PAID": paid.world.relocations}
    weights = {"DERIVED": fate.agent.state_dict(), "YOKED": yoked.agent.state_dict(), "PAID": paid.agent.state_dict()}
    weights = {k: {n: v.clone() for n, v in sd.items()} for k, sd in weights.items()}
    out["seconds_stage1"] = round(time.time() - t0, 1)
    if stages >= 3:
        # stage 2: downstream measures on the frozen stage-1 weights
        n_envs, probe_eps, causal_eps = sizes
        out["downstream"] = {k: downstream(sd, seed, rate, wcd, n_envs, probe_eps, causal_eps)
                             for k, sd in weights.items()}
        # stage 3: withdrawal
        dcut = ArmRunner("DCUT", seed, wc, tc)
        pcut = ArmRunner("PCUT", seed, wc, tc)
        load_independent(dcut, fate.export_state())
        load_independent(pcut, paid.export_state())
        for r in (fate, paid, dcut, pcut):
            _restart(r, tc)
        followers = {"DCUT": dcut, "PKEEP": paid, "PCUT": pcut}
        out["curves3"] = _lockstep(fate, followers, "DKEEP", w_iters)
        out["stage3"] = _evaluate(fate, followers, "DKEEP")
        for k, r in [("DKEEP", fate), *followers.items()]:
            weights[k] = {n: v.clone() for n, v in r.agent.state_dict().items()}
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {k: state_to_bytes(sd) for k, sd in weights.items()}
    return out
