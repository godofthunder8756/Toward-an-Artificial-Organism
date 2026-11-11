"""Track C swap v6 (option J): v5's long pair, also returning the final agent weights.

Additive module; every earlier module is unchanged. `run_pair_saved` follows
longrun.run_pair_long step for step (a unit test checks that the records are
identical) and adds the fate and yoked agents' final weights, so that the
erasure bypass can be diagnosed later without retraining.

Simulated variables only. No operator, stop or shutdown variable exists.
"""
from __future__ import annotations

import time
from typing import Dict

import torch

from .env import WorldConfig
from .erasure import ErasureRunner
from .factorial import state_from_bytes, state_to_bytes
from .longrun import _restart, evaluate_pair
from .train import TrainConfig


def run_pair_saved(job) -> Dict[str, object]:
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
    weights = {"FATE": state_to_bytes(fate.agent.state_dict()), "YOKED": state_to_bytes(yoked.agent.state_dict())}
    final = evaluate_pair(fate, yoked)
    final["S-FATE"]["curve"] = curves["FATE"]
    final["S-YOKED"]["curve"] = curves["YOKED"]
    out.update(final)
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = weights
    return out
