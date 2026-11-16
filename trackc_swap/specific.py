"""Track C swap, option G2: is post-meal suppression specific to the variable that was fed?

Option G's two-variable cell (B2) found no difference between derived and paid regulators in
the combined index K. After the fact it also showed that a meal of one kind suppresses the
readiness for the other kind ("cross" K), and that this other-meal suppression was closer to
the own-meal suppression in paid agents than in derived agents. Option T then showed that the
K difference of the base cell is a stage of learning. This module reruns the B2 cell on fresh
seeds so that the specificity contrast can be tested as a claim fixed in advance, and trains
on past B2's length so that it can be asked whether the contrast, if found, is itself a stage.

Nothing about the cell changes. The job below is option G's B2 job up to the first measurement
point: the same phase 1, runners, seeds and streams, the same lockstep training and the same
evaluation. As in option T, after each point's evaluation (fresh episodes, no learning)
training continues from a fresh episode with the same agents, optimizers and streams, and the
downstream probes of every point are run on copies of the weights after all training has
ended, so they cannot touch the training streams.

One measure is added to option G's: `own_clean`, the own-meal suppression over steps with no
meal of the other kind in the last 10 steps. It is the mirror image of option G's cross
measure (other-meal suppression over steps with no own-kind meal in the last 10 steps), so
the two can be compared on an equal footing. Everything else in a downstream record is
option G's, computed from the same probe run.

Additive: no earlier module is changed. Simulated variables only; there is no operator
variable in the world or in any agent's return.
"""
from __future__ import annotations

import time
from typing import Dict, List

import numpy as np
import torch

from .causal import CTRL_MIN, suppression
from .env import WorldConfig
from .factorial import state_to_bytes
from .general import TwoRunner, cross_suppression, run_phase1_two, run_probe_g
from .paid import _evaluate, _lockstep, load_independent
from .paid2 import approach_suppression, flat_readiness
from .train import TrainConfig

HIDDEN, N_RES = 64, 2                                # option G's B2 cell


def own_clean(rec: List[Dict[str, np.ndarray]], r: int) -> Dict[str, object]:
    """S and M for variable r timed from its own last meal, over steps with no meal of the
    OTHER variable in the last 10 steps, matched on r's reading. The mirror of
    general.cross_suppression."""
    keep = rec[1 - r]["since"] >= CTRL_MIN
    sub = {k: rec[r][k][keep] for k in ("psi", "app", "intero", "since")}
    return {"S": suppression(sub)["S"], "M": approach_suppression(sub)["M"]}


def downstream_s(sd, seed: int, rate: float, wcd: Dict[str, object], n_envs: int, episodes: int) -> Dict[str, object]:
    """general.downstream_g for a B2 agent (same probe run, same records) plus `own_clean`."""
    off = run_probe_g(sd, HIDDEN, N_RES, rate, seed, WorldConfig(**wcd), n_envs, episodes)
    rec = off.pop("_rec")
    res = []
    for rr in rec:
        supp = suppression(rr)
        res.append({"suppression": supp, "flat": flat_readiness(supp), "approach": approach_suppression(rr)})
    return {"res": res, "base": off, "cross": [cross_suppression(rec, r) for r in range(N_RES)],
            "own_clean": [own_clean(rec, r) for r in range(N_RES)]}


def run_seed_s(job) -> Dict[str, object]:
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
    t0 = time.time()
    tc = TrainConfig(**(tcd | {"kappa_f": rate}))
    assert all((p * tc.rollout) % wc.horizon == 0 for p in points)
    p1 = run_phase1_two(seed, wc, TrainConfig(**tcd), rate)
    nofate = {"eval": p1["eval"], "eval_full_erasure": p1["eval_full_erasure"]}
    fate = TwoRunner("FATE", seed, wc, tc)
    followers = {"YOKED": TwoRunner("YOKED", seed, wc, tc), "PAID": TwoRunner("PAID", seed, wc, tc, pay=pay)}
    runners = {"DERIVED": fate, **followers}
    for r in runners.values():
        load_independent(r, p1["state"])
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
        pts.append({"iters": p, "episodes": len(curves["DERIVED"]["in_band"]),
                    "stage1": _evaluate(fate, followers, "DERIVED"),
                    "relocations1": {k: r.world.relocations for k, r in runners.items()},
                    "seconds_training": round(time.time() - t0, 1)})
        weights[p] = {k: {n: v.clone() for n, v in r.agent.state_dict().items()} for k, r in runners.items()}
    out["curves"] = curves
    if stages >= 2:
        n_envs, episodes = sizes
        for pt in pts:
            pt["downstream"] = {k: downstream_s(sd, seed, rate, wcd, n_envs, episodes)
                                for k, sd in weights[pt["iters"]].items()}
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
