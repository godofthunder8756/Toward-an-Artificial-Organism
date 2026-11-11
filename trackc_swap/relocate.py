"""Track C swap v7 (option K step 2): erasure also relocates the agent.

Additive module; every earlier module is unchanged. The option K diagnosis
(TRACKC_BYPASS_DIAG_RESULTS.md) found that v6's bypass agents hold the cue bit in
where they stand: after the cue they walk to a cue-specific place and read the bit
back from the wall view at the probe. The world change fixed in advance for a
position bypass (TRACKC_BYPASS_DIAG_PROTOCOL.md section 4) is applied here:

  every erasure event resets the carried state (as in v3-v6) AND moves the agent
  to a uniformly random cell of the grid, after that step's movement and eating.

Erasure events are each agent's own draws, so yoked replay and imposed erasure
relocate too; with gain 0 (phase 1, no fate) nothing is erased or moved, and the
world is v6's world exactly. Relocation draws come from their own random stream,
so every other stream is as in v6 until the first relocation.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict, Optional

import numpy as np
import torch

from .env import SwapWorld, WorldConfig
from .erasure import ErasureAgent, ErasureRunner, _NoEcho
from .factorial import GAIN_RULES, GradedSwapWorld, _train, state_from_bytes, state_to_bytes
from .longrun import _restart, evaluate_pair
from .train import TrainConfig

RELOCATE_STREAM = 1000            # spawn key of the relocation random stream


class _Relocate:
    """World mixin: `relocate_next` (bool per env, set by the agent's erasure draw) moves
    those agents to a uniformly random cell at the end of the next step."""

    def __init__(self, n_envs, objective, cfg, seed_seq):
        self.rng_relocate = np.random.default_rng(np.random.SeedSequence(seed_seq.entropy,
                                                                         spawn_key=(RELOCATE_STREAM,)))
        self.relocate_next: Optional[np.ndarray] = None
        self.relocations = 0
        super().__init__(n_envs, objective, cfg, seed_seq)

    def reset(self) -> np.ndarray:
        self.relocate_next = None
        return super().reset()

    def step(self, action: np.ndarray):
        obs, reward, done = super().step(action)
        m, self.relocate_next = self.relocate_next, None
        if m is not None and m.any():
            k = int(m.sum())
            self.x[m] = self.rng_relocate.integers(0, self.cfg.grid, k)
            self.y[m] = self.rng_relocate.integers(0, self.cfg.grid, k)
            self.relocations += k
            obs = self.observe()
        return obs, reward, done


class RelocSwapWorld(_Relocate, _NoEcho, SwapWorld):
    pass


class RelocGradedWorld(_Relocate, _NoEcho, GradedSwapWorld):
    pass


class RelocAgent(ErasureAgent):
    """ErasureAgent that tells its world which environments were erased this step."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, gain: torch.Tensor, gen: torch.Generator):
        h = self.core(torch.relu(self.enc(obs)), h)
        logits, value = self.pi(h), self.v(h).squeeze(-1)
        if gain is not None:
            p = torch.clamp(self.kappa_f * gain, 0.0, 1.0)
            erase = torch.rand(p.shape, generator=gen) < p
            h = h * (~erase).to(h.dtype)[:, None]
            world = self.__dict__.get("_world")
            if world is not None:
                world.relocate_next = erase.numpy().copy()
        return logits, value, h


class RelocRunner(ErasureRunner):
    """ErasureRunner with relocation on erasure. Same seeding as v3-v6."""

    def __init__(self, arm: str, objective: str, seed: int, wc: WorldConfig, tc: TrainConfig,
                 gain_rule: str = "SAT"):
        if gain_rule not in GAIN_RULES:
            raise ValueError(gain_rule)
        self.arm, self.tc, self.wc, self.gain_rule = arm, tc, wc, gain_rule
        tag = {"FATE": 1, "YOKED": 2, "NOFATE": 3}[arm]
        cls = RelocGradedWorld if gain_rule == "GRADED" else RelocSwapWorld
        self.world = cls(tc.n_envs, objective, wc, np.random.SeedSequence([seed, tag, 11]))
        torch.manual_seed(seed)
        self.agent = RelocAgent(tc.hidden, tc.kappa_f, tc.s_core)
        self.agent.__dict__["_world"] = self.world
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)


def run_phase1_reloc(job) -> Dict[str, object]:
    """As erasure.run_phase1, in the relocation world. job = (objective, seed, wcd, tcd, rates)."""
    objective, seed, wcd, tcd, rates = job
    torch.set_num_threads(1)
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    r = RelocRunner("NOFATE", objective, seed, wc, tc)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = _train(r, tc.iters, zeros)
    relocations_training = r.world.relocations          # 0: gain 0 erases nothing
    state = r.export_state()
    ev, _, hsd = r.evaluate("zero")
    full = {}
    for rate in rates:
        r.agent.kappa_f = rate
        full[str(rate)] = r.evaluate("full")[0]
    return {"kind": "phase1", "objective": objective, "seed": seed,
            "S-NOFATE": {"eval": ev, "curve": curve, "hidden_sd": hsd, "eval_full_erasure": full},
            "state": state_to_bytes(state), "relocations_phase1_training": relocations_training,
            "seconds": round(time.time() - t0, 1)}


def run_pair_reloc(job) -> Dict[str, object]:
    """As confirm.run_pair_saved, in the relocation world.
    job = (objective, seed, gain_rule, rate, wcd, tcd, phase1_state_bytes, p2_iters, checkpoints)."""
    objective, seed, gain_rule, rate, wcd, tcd, p1, p2_iters, checkpoints = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    for c in checkpoints:
        assert 0 < c < p2_iters and (c * tc.rollout) % wc.horizon == 0
    t0 = time.time()
    fate = RelocRunner("FATE", objective, seed, wc, tc, gain_rule)
    yoked = RelocRunner("YOKED", objective, seed, wc, tc, gain_rule)
    state = state_from_bytes(p1)
    fate.load_state(state)
    yoked.load_state(state)
    for p_f, p_y in zip(fate.agent.parameters(), yoked.agent.parameters()):
        assert torch.equal(p_f, p_y)
    out: Dict[str, object] = {"kind": "pair", "objective": objective, "seed": seed, "gain_rule": gain_rule,
                              "start": "SCAFFOLD", "rate": rate, "p2_iters": p2_iters, "relocate": True}
    onset, onset_gains, _ = fate.evaluate("own")
    onset_y, _, _ = yoked.evaluate("replay", onset_gains)
    out["onset"] = {"S-FATE": onset, "S-YOKED": onset_y}
    for r in (fate, yoked):
        _restart(r, tc)
    curves = {"FATE": [], "YOKED": []}
    out["checkpoints"] = {}
    for it in range(1, p2_iters + 1):
        used, _ = fate.rollout(None, learn=True)
        yoked.rollout(used, learn=True)
        for name, r in (("FATE", fate), ("YOKED", yoked)):
            st = r.end_episode_if_due()
            if st is not None:
                curves[name].append(st)
        if it in checkpoints:
            out["checkpoints"][str(it)] = evaluate_pair(fate, yoked)
            for r in (fate, yoked):
                _restart(r, tc)
    weights = {"FATE": state_to_bytes(fate.agent.state_dict()), "YOKED": state_to_bytes(yoked.agent.state_dict())}
    out["relocations_before_final"] = {"FATE": fate.world.relocations, "YOKED": yoked.world.relocations}
    final = evaluate_pair(fate, yoked)
    final["S-FATE"]["curve"] = curves["FATE"]
    final["S-YOKED"]["curve"] = curves["YOKED"]
    out.update(final)
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = weights
    return out
