"""Track C swap, option T: training length in the base cell.

Options R2 to R4 found that derived regulators hold back after a meal they cannot yet sense and
that paid regulators mostly do not, after 3600 phase-2 updates. Option G found the difference
smaller with a larger learner and absent in a two-variable world trained three times as long.
This module asks whether, in the base cell itself, the difference is a stage of learning: the
same three arms (derived, yoked, paid) are trained on, and measured at several points.

Nothing about the cell changes. The job below is option G's base-cell job (which is options
R2 to R4's pipeline) up to the first measurement point: the same phase 1, the same runners,
seeds and streams, the same lockstep training and the same evaluation. After each point's
evaluation (fresh episodes, no learning) training continues from a fresh episode with the same
agents, optimizers and streams. The downstream probes of every point are run on copies of the
weights after all training has ended, so they cannot touch the training streams.

Additive: no earlier module is changed. Simulated variables only; there is no operator
variable in the world or in any agent's return.
"""
from __future__ import annotations

import time
from typing import Dict

import torch

from .env import WorldConfig
from .factorial import state_from_bytes, state_to_bytes
from .general import downstream_g
from .paid import ArmRunner, _evaluate, _lockstep, load_independent
from .relocate import run_phase1_reloc
from .train import TrainConfig

HIDDEN, N_RES = 64, 1                                # the base cell


def run_seed_t(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, rate, points, pay, sizes, stages).
    points: increasing cumulative numbers of phase-2 updates at which the agents are measured.
    pay: weight of the payment (option R's "gain" kind).
    sizes = (n_envs, probe episodes) for the downstream measures.
    stages: 1 = training and evaluation only; 2 = also the downstream measures at every point."""
    seed, wcd, tcd, rate, points, pay, sizes, stages = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc = WorldConfig(**wcd)
    tcd = tcd | {"hidden": HIDDEN}
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert all((p * tc.rollout) % wc.horizon == 0 for p in points)
    t0 = time.time()
    p1 = run_phase1_reloc(("M1", seed, wcd, tcd, [rate]))
    nofate = {"eval": p1["S-NOFATE"]["eval"], "eval_full_erasure": p1["S-NOFATE"]["eval_full_erasure"][str(rate)]}
    state = state_from_bytes(p1["state"])
    fate = ArmRunner("FATE", seed, wc, tc)
    followers = {"YOKED": ArmRunner("YOKED", seed, wc, tc),
                 "PAID": ArmRunner("PAID", seed, wc, tc, paid=True, pay=("gain", pay))}
    runners = {"DERIVED": fate, **followers}
    for r in runners.values():
        load_independent(r, state)
    out: Dict[str, object] = {"seed": seed, "hidden": HIDDEN, "n_res": N_RES, "rate": rate, "pay": pay,
                              "points_at": points, "nofate": nofate}
    curves = {k: {"in_band": [], "rho": []} for k in runners}
    pts, weights, done = [], {}, 0
    for p in points:
        seg = _lockstep(fate, followers, "DERIVED", p - done)
        done = p
        for k in curves:
            for name in ("in_band", "rho"):
                curves[k][name] += seg[k][name]
        pt = {"iters": p, "episodes": len(curves["DERIVED"]["in_band"]),
              "stage1": _evaluate(fate, followers, "DERIVED"),
              "relocations1": {k: r.world.relocations for k, r in runners.items()},
              "seconds_training": round(time.time() - t0, 1)}
        weights[p] = {k: {n: v.clone() for n, v in r.agent.state_dict().items()} for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    if stages >= 2:
        n_envs, episodes = sizes
        for pt in pts:
            pt["downstream"] = {k: downstream_g(sd, HIDDEN, N_RES, seed, rate, wcd, n_envs, episodes)
                                for k, sd in weights[pt["iters"]].items()}
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
