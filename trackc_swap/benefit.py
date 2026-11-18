"""Track C swap, option B: does selective post-meal suppression help? (no training)

Additive module; every earlier module is unchanged. Options G and G2 found that in the
two-variable cell (B2) derived regulators hold back after a meal more specifically to the
variable that was fed than paid regulators do; option W found that both arms' states carry
the same memory of the last meal, so the difference is in how the policy acts on it. This
module asks whether that difference helps the agent keep its body in band when the world
makes it matter.

Each stored agent is run with erasure off, exactly as the source run's downstream probe ran it
(specific.downstream_s: same seeds, streams and sampling), in the base world and in fixed
variants of it. Only world parameters change; the agent is not changed or trained. In V0, the
base world, the record equals the stored downstream record (a test checks this).

Variants (frozen):
  V0  the base world (wear 0.001 on each variable, 3 items of each kind);
  V1  wear 0.002 on each variable: both run down twice as fast, so both are more often low
      at once and a meal of one kind is more often followed by a need for the other;
  V2  wear 0.003 on each variable;
  V3  2 items of each kind (scarcer);
  V4  5 items of each kind (denser: an item of the other kind is more often close by).

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import torch

from .specific import downstream_s

VARIANTS = {"V0": {}, "V1": {"wear": 0.002}, "V2": {"wear": 0.003}, "V3": {"n_food": 2}, "V4": {"n_food": 5}}


def run_agent_b(job) -> Dict[str, object]:
    """job = (label dict, state dict, seed, rate, wcd, n_envs, episodes).
    Returns the downstream record of the agent in every variant."""
    label, sd, seed, rate, wcd, n_envs, episodes = job
    torch.set_num_threads(1)
    t0 = time.time()
    out: Dict[str, object] = dict(label)
    out["variants"] = {v: downstream_s(sd, seed, rate, wcd | ch, n_envs, episodes) for v, ch in VARIANTS.items()}
    out["seconds"] = round(time.time() - t0, 1)
    return out
