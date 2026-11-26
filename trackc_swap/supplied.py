"""P1n: separately trained rival with a supplied damage analyzer (supplied substrate).

Additive module; every earlier module is imported, never modified. Protocol: P1N_SUPPLIED_PROTOCOL.md.

P1m credited the damage-trained agent's endogenous integrity variable against the strongest reduction of itself.
The remaining rival is separately trained: the same network, the same training (P1g's PFATE arm: phase 1, then
3600 updates with damage driven by its own body, BASE_F 0.012, graded K), and an EXTERNAL damage analyzer whose
verdict is supplied as input from the step after a damage event to the probe:
    flag_damaged   1 if the trial's memory was overwritten
    flag_conflict  1 if the overwrite carried the other value (the memory's content is now unreliable)
    flag_size      K / 70, the size of the overwrite
This is the constitution's supplied-substrate rival ("the analyzer is supplied substrate ... test a rival in
which the network gets the same information directly"). It gets strictly more information than the endogenous
agent while the analyzer works. At evaluation the analyzer can also be silent (flags withheld): the failure
mode of a supplied analyzer.

FlagRunner reproduces P1g's PFATE runner exactly when the flags are off: the extra input columns start at zero
weight and receive zero input (tested). It extends LesionRunner, so every P1j-P1m measurement applies.
Simulated variables only.
"""
from __future__ import annotations

import copy
from typing import Dict

import numpy as np
import torch

from .gradmon import BASE_G, KS_G, GradWorld
from .selfeval import H_PLAIN, Q_LO
from .selfmon import P_MAX_M, RATE_M, TAGS_M
from .necessity import LesionRunner

N_FLAG = 3


class FlagWorld(GradWorld):
    """GradWorld whose observation carries the supplied analyzer's verdict on the current trial."""
    flag_on: bool = True

    def observe(self) -> np.ndarray:
        obs = super().observe()
        n = obs.shape[0]
        extra = np.zeros((n, N_FLAG), dtype=np.float32)
        if self.flag_on:
            dm = self.damaged & self.active
            extra[:, 0] = dm
            extra[:, 1] = dm & self.conflict
            extra[:, 2] = np.where(dm, self.dmg_k / float(H_PLAIN), 0.0)
        return np.concatenate([obs, extra], axis=1)


def widen_enc(agent, n_extra: int = N_FLAG) -> None:
    """Replace the encoder by one with n_extra more inputs; the new columns start at zero."""
    old = agent.enc
    new = torch.nn.Linear(old.in_features + n_extra, old.out_features)
    with torch.no_grad():
        new.weight.zero_()
        new.weight[:, :old.in_features] = old.weight
        new.bias.copy_(old.bias)
    agent.enc = new


def pad_state(state: Dict[str, object], n_extra: int = N_FLAG) -> Dict[str, object]:
    """Phase-1 agent and Adam state with zero-padded encoder columns (Adam moments zero for them)."""
    st = copy.deepcopy(state)
    w = st["agent"]["enc.weight"]
    st["agent"]["enc.weight"] = torch.cat([w, torch.zeros(w.shape[0], n_extra, dtype=w.dtype)], 1)
    for k, s in st["opt"]["state"].items():
        for m in ("exp_avg", "exp_avg_sq"):
            if m in s and s[m].shape == w.shape:
                s[m] = torch.cat([s[m], torch.zeros(w.shape[0], n_extra, dtype=s[m].dtype)], 1)
    return st


class FlagRunner(LesionRunner):
    """P1g's runner for one arm with the supplied analyzer's flags in the observation."""

    def __init__(self, arm: str, seed: int, wc, tc, pay: float = 0.0, q_lo: float = Q_LO, tag_offset: int = 0,
                 rate: float = RATE_M, p_max: float = P_MAX_M, base: float = BASE_G, ks=KS_G, flag_on: bool = True):
        super().__init__(arm, seed, wc, tc, pay, q_lo, tag_offset, rate, p_max, base, ks)
        self.world = FlagWorld(tc.n_envs, wc, np.random.SeedSequence([seed, TAGS_M[arm] + tag_offset, 19]), q_lo, pay)
        self.world.flag_on = flag_on
        widen_enc(self.agent)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)

    def set_flag(self, on: bool) -> None:
        self.world.flag_on = on
