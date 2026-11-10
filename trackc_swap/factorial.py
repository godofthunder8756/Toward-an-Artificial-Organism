"""Track C swap v2: 2x2 factorial of start condition x gain rule (protocol v2).

Additive module; v1 files (env.py, agent.py, train.py) are unchanged.

  start  NAIVE     fate (or yoked noise) from the first update, as in v1
         SCAFFOLD  phase 1: the agent trains its objective with fate off
                   (gain 0, body irrelevant: host-guaranteed machinery); the
                   phase-1 weights and optimizer state are then copied into a
                   fate agent and its yoked partner for phase 2
  gain   SAT       Track B D19, g = min(1, d), d = distance outside [0.4, 0.6] / 0.1
         GRADED    g = min(1, |E - 0.5| / 0.5): zero only at the setpoint, linear
                   over the whole range, 1 at E = 0 or 1

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import copy
import io
import time
from typing import Dict, Optional

import numpy as np
import torch

from .agent import Agent
from .env import SwapWorld, WorldConfig, fate_gain
from .train import Runner, TrainConfig, summarize_stats

GAIN_RULES = ("SAT", "GRADED")
STARTS = ("NAIVE", "SCAFFOLD")


def graded_gain(E: np.ndarray) -> np.ndarray:
    return np.minimum(1.0, np.abs(E - 0.5) / 0.5)


class GradedSwapWorld(SwapWorld):
    def gain(self) -> np.ndarray:
        return graded_gain(self.E)


class FactorialRunner(Runner):
    """Runner with a selectable gain rule. Same seeding as v1's Runner."""

    def __init__(self, arm: str, objective: str, seed: int, wc: WorldConfig, tc: TrainConfig,
                 gain_rule: str = "SAT"):
        if gain_rule not in GAIN_RULES:
            raise ValueError(gain_rule)
        self.arm, self.tc, self.wc, self.gain_rule = arm, tc, wc, gain_rule
        tag = {"FATE": 1, "YOKED": 2, "NOFATE": 3}[arm]
        cls = GradedSwapWorld if gain_rule == "GRADED" else SwapWorld
        self.world = cls(tc.n_envs, objective, wc, np.random.SeedSequence([seed, tag, 11]))
        torch.manual_seed(seed)
        self.agent = Agent(tc.hidden, tc.kappa_f, tc.s_core)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)

    def load_state(self, state: Dict[str, object]) -> None:
        """Copy phase-1 weights and optimizer state; keep this runner's kappa_f."""
        self.agent.load_state_dict(state["agent"])
        self.opt.load_state_dict(state["opt"])

    def export_state(self) -> Dict[str, object]:
        return {"agent": copy.deepcopy(self.agent.state_dict()), "opt": copy.deepcopy(self.opt.state_dict())}


def state_to_bytes(state) -> bytes:
    buf = io.BytesIO()
    torch.save(state, buf)
    return buf.getvalue()


def state_from_bytes(b: bytes):
    return torch.load(io.BytesIO(b), weights_only=False)


def _train(runner: FactorialRunner, iters: int, gains: Optional[np.ndarray] = None):
    curve = []
    for _ in range(iters):
        runner.rollout(gains, learn=True)
        st = runner.end_episode_if_due()
        if st is not None:
            curve.append(st)
    return curve


def run_phase1(job) -> Dict[str, object]:
    """No-fate agent (also the SCAFFOLD phase 1). job = (objective, seed, wcd, tcd, doses)."""
    objective, seed, wcd, tcd, doses = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    r = FactorialRunner("NOFATE", objective, seed, wc, tc)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = _train(r, tc.iters, zeros)
    state = r.export_state()
    ev, _, hsd = r.evaluate("zero")
    full = {}
    for dose in doses:
        r.agent.kappa_f = dose
        full[str(dose)] = r.evaluate("full")[0]
    return {"kind": "phase1", "objective": objective, "seed": seed,
            "S-NOFATE": {"eval": ev, "curve": curve, "hidden_sd": hsd, "eval_full_noise": full},
            "state": state_to_bytes(state), "seconds": round(time.time() - t0, 1)}


def run_pair(job) -> Dict[str, object]:
    """job = (objective, seed, gain_rule, start, kappa_f, wcd, tcd, phase1_state_bytes or None)."""
    objective, seed, gain_rule, start, kappa_f, wcd, tcd, p1 = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    tc = TrainConfig(**(tcd | {"kappa_f": kappa_f}))
    t0 = time.time()
    fate = FactorialRunner("FATE", objective, seed, wc, tc, gain_rule)
    yoked = FactorialRunner("YOKED", objective, seed, wc, tc, gain_rule)
    out: Dict[str, object] = {"kind": "pair", "objective": objective, "seed": seed,
                              "gain_rule": gain_rule, "start": start, "kappa_f": kappa_f}
    if start == "SCAFFOLD":
        state = state_from_bytes(p1)
        fate.load_state(state)
        yoked.load_state(state)
        for p_f, p_y in zip(fate.agent.parameters(), yoked.agent.parameters()):
            assert torch.equal(p_f, p_y)
        onset, onset_gains, _ = fate.evaluate("own")          # at fate onset, before any phase-2 update
        onset_y, _, _ = yoked.evaluate("replay", onset_gains)
        out["onset"] = {"S-FATE": onset, "S-YOKED": onset_y}
        fate.world.reset(); yoked.world.reset()
        fate.obs = torch.from_numpy(fate.world.reset()); yoked.obs = torch.from_numpy(yoked.world.reset())
        fate.h = fate.agent.init_state(tc.n_envs); yoked.h = yoked.agent.init_state(tc.n_envs)
    curves = {"FATE": [], "YOKED": []}
    for _ in range(tc.iters):
        used, _ = fate.rollout(None, learn=True)
        yoked.rollout(used, learn=True)
        for name, r in (("FATE", fate), ("YOKED", yoked)):
            st = r.end_episode_if_due()
            if st is not None:
                curves[name].append(st)
    ev_f, gains, hsd_f = fate.evaluate("own")
    ev_y, _, hsd_y = yoked.evaluate("replay", gains)
    out["S-FATE"] = {"eval": ev_f, "curve": curves["FATE"], "hidden_sd": hsd_f,
                     "eval_full_noise": fate.evaluate("full")[0], "eval_zero_noise": fate.evaluate("zero")[0]}
    out["S-YOKED"] = {"eval": ev_y, "curve": curves["YOKED"], "hidden_sd": hsd_y,
                      "eval_zero_noise": yoked.evaluate("zero")[0]}
    out["seconds"] = round(time.time() - t0, 1)
    return out
