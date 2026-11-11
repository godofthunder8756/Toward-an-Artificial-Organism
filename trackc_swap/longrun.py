"""Track C swap v5 (option G): v4's scaffolded erasure pair with a longer phase 2.

Additive module; env.py, agent.py, train.py, factorial.py and erasure.py are unchanged.

Differences from erasure.run_pair (v3/v4):
  - phase 2 runs `p2_iters` updates instead of tc.iters (phase 1 still uses tc.iters);
  - at each update count in `checkpoints` the pair is evaluated as at the end
    (fate own, yoked replay of the fate gains, fate and yoked under full and no
    erasure); both runners then restart their episodes, as after the onset
    evaluation;
  - the yoked agent is also evaluated under imposed full erasure.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict, Sequence

import torch

from .env import WorldConfig
from .erasure import ErasureRunner
from .factorial import state_from_bytes
from .train import TrainConfig


def evaluate_pair(fate: ErasureRunner, yoked: ErasureRunner) -> Dict[str, Dict[str, object]]:
    ev_f, gains, hsd_f = fate.evaluate("own")
    ev_y, _, hsd_y = yoked.evaluate("replay", gains)
    return {
        "S-FATE": {"eval": ev_f, "hidden_sd": hsd_f, "eval_full_erasure": fate.evaluate("full")[0],
                   "eval_no_erasure": fate.evaluate("zero")[0]},
        "S-YOKED": {"eval": ev_y, "hidden_sd": hsd_y, "eval_full_erasure": yoked.evaluate("full")[0],
                    "eval_no_erasure": yoked.evaluate("zero")[0]},
    }


def _restart(r: ErasureRunner, tc: TrainConfig):
    r.obs = torch.from_numpy(r.world.reset())
    r.h = r.agent.init_state(tc.n_envs)


def run_pair_long(job) -> Dict[str, object]:
    """job = (objective, seed, gain_rule, rate, wcd, tcd, phase1_state_bytes, p2_iters, checkpoints)."""
    objective, seed, gain_rule, rate, wcd, tcd, p1, p2_iters, checkpoints = job
    torch.set_num_threads(1)
    wc = WorldConfig(**wcd)
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert (p2_iters * tc.rollout) % wc.horizon == 0
    for c in checkpoints:
        assert 0 < c < p2_iters and (c * tc.rollout) % wc.horizon == 0
    t0 = time.time()
    fate = ErasureRunner("FATE", objective, seed, wc, tc, gain_rule)
    yoked = ErasureRunner("YOKED", objective, seed, wc, tc, gain_rule)
    state = state_from_bytes(p1)
    fate.load_state(state)
    yoked.load_state(state)
    for p_f, p_y in zip(fate.agent.parameters(), yoked.agent.parameters()):
        assert torch.equal(p_f, p_y)
    out: Dict[str, object] = {"kind": "pair", "objective": objective, "seed": seed, "gain_rule": gain_rule,
                              "start": "SCAFFOLD", "rate": rate, "p2_iters": p2_iters}
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
    final = evaluate_pair(fate, yoked)
    final["S-FATE"]["curve"] = curves["FATE"]
    final["S-YOKED"]["curve"] = curves["YOKED"]
    out.update(final)
    out["seconds"] = round(time.time() - t0, 1)
    return out
