"""Track C swap v3: erasure-type fate with a scaffolded start (protocol v3).

Additive module; env.py, agent.py, train.py and factorial.py are unchanged.

Fate mechanism ERASE (replaces v1/v2 additive noise):
  after the recurrent update and the readouts of step t, the state carried to
  step t+1 is reset to zero (the episode-start state) with probability
  p_t = min(1, rate * g_t), drawn independently per env. g_t is the gain rule
  (SAT = Track B D19, or GRADED). `rate` is the dose and is held in the agent's
  `kappa_f` attribute so that v2's runner plumbing applies unchanged. Erasure
  removes what is held in memory; unlike additive noise, no code can absorb it.

Echo channels removed (all arms, declared deviation from Track B A-list):
  the previous-action and previous-reward inputs are set to zero. Under
  erasure they are an outside register: an agent can idle with STAY for cue 0
  and INTERACT for cue 1 and read the bit back after an erasure. G1's register
  had no such bypass.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import numpy as np
import torch

from .agent import Agent
from .env import VIEW, N_ACT, SwapWorld, WorldConfig
from .factorial import (GAIN_RULES, FactorialRunner, GradedSwapWorld, _train, state_from_bytes,
                        state_to_bytes)
from .train import TrainConfig

ECHO = slice(2 * VIEW * VIEW + 1, 2 * VIEW * VIEW + 1 + N_ACT + 1)   # previous action (8) + previous reward (1)


class ErasureAgent(Agent):
    """Same network as v1/v2. `kappa_f` is the per-step erasure probability at gain 1."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, gain: torch.Tensor, gen: torch.Generator):
        h = self.core(torch.relu(self.enc(obs)), h)
        logits, value = self.pi(h), self.v(h).squeeze(-1)
        if gain is not None:
            p = torch.clamp(self.kappa_f * gain, 0.0, 1.0)
            erase = torch.rand(p.shape, generator=gen) < p
            h = h * (~erase).to(h.dtype)[:, None]
        return logits, value, h


class _NoEcho:
    def observe(self) -> np.ndarray:
        o = super().observe()
        o[:, ECHO] = 0.0
        return o


class NoEchoSwapWorld(_NoEcho, SwapWorld):
    pass


class NoEchoGradedWorld(_NoEcho, GradedSwapWorld):
    pass


class ErasureRunner(FactorialRunner):
    """v2's FactorialRunner with the erasure agent and the echo-free world. Same seeding."""

    def __init__(self, arm: str, objective: str, seed: int, wc: WorldConfig, tc: TrainConfig,
                 gain_rule: str = "SAT"):
        if gain_rule not in GAIN_RULES:
            raise ValueError(gain_rule)
        self.arm, self.tc, self.wc, self.gain_rule = arm, tc, wc, gain_rule
        tag = {"FATE": 1, "YOKED": 2, "NOFATE": 3}[arm]
        cls = NoEchoGradedWorld if gain_rule == "GRADED" else NoEchoSwapWorld
        self.world = cls(tc.n_envs, objective, wc, np.random.SeedSequence([seed, tag, 11]))
        torch.manual_seed(seed)
        self.agent = ErasureAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


def run_phase1(job) -> Dict[str, object]:
    """No-fate agent (also the scaffold's phase 1). job = (objective, seed, wcd, tcd, rates).
    After training it is evaluated with erasure imposed at gain 1 at each rate (task load)."""
    objective, seed, wcd, tcd, rates = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    r = ErasureRunner("NOFATE", objective, seed, wc, tc)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = _train(r, tc.iters, zeros)
    state = r.export_state()
    ev, _, hsd = r.evaluate("zero")
    full = {}
    for rate in rates:
        r.agent.kappa_f = rate
        full[str(rate)] = r.evaluate("full")[0]
    return {"kind": "phase1", "objective": objective, "seed": seed,
            "S-NOFATE": {"eval": ev, "curve": curve, "hidden_sd": hsd, "eval_full_erasure": full},
            "state": state_to_bytes(state), "seconds": round(time.time() - t0, 1)}


def run_pair(job) -> Dict[str, object]:
    """Scaffolded fate/yoked pair. job = (objective, seed, gain_rule, rate, wcd, tcd, phase1_state_bytes)."""
    objective, seed, gain_rule, rate, wcd, tcd, p1 = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    t0 = time.time()
    fate = ErasureRunner("FATE", objective, seed, wc, tc, gain_rule)
    yoked = ErasureRunner("YOKED", objective, seed, wc, tc, gain_rule)
    state = state_from_bytes(p1)
    fate.load_state(state)
    yoked.load_state(state)
    for p_f, p_y in zip(fate.agent.parameters(), yoked.agent.parameters()):
        assert torch.equal(p_f, p_y)
    out: Dict[str, object] = {"kind": "pair", "objective": objective, "seed": seed,
                              "gain_rule": gain_rule, "start": "SCAFFOLD", "rate": rate}
    onset, onset_gains, _ = fate.evaluate("own")              # fate on, before any phase-2 update
    onset_y, _, _ = yoked.evaluate("replay", onset_gains)
    out["onset"] = {"S-FATE": onset, "S-YOKED": onset_y}
    for r in (fate, yoked):
        r.obs = torch.from_numpy(r.world.reset())
        r.h = r.agent.init_state(tc.n_envs)
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
                     "eval_full_erasure": fate.evaluate("full")[0], "eval_no_erasure": fate.evaluate("zero")[0]}
    out["S-YOKED"] = {"eval": ev_y, "curve": curves["YOKED"], "hidden_sd": hsd_y,
                      "eval_no_erasure": yoked.evaluate("zero")[0]}
    out["seconds"] = round(time.time() - t0, 1)
    return out
