"""Track C P3c: confirmation and cause of the differentiated body readout (Layer 3 -> Layer 4)

P3b (UNDETERMINED; partial reading A_SIDE_SPECIFIC, NO_SPREAD) found, descriptively, that two decisions put at
risk by opposite conditions of one body read the body with opposite signs: A (memory, at risk when the body is
low) abstains MORE when the body looks low; C (perception, at risk when the body is high) abstains LESS when the
body looks low (a release of caution). P3c (i) confirms that pattern on new seeds with P3b's training unchanged,
and (ii) asks whether each readout is carried by a direction of the agent's state that causally moves its own
decision, and whether the two decisions share one body direction read with opposite signs (content in the
readout) or use separate directions (content in the state).

Training: trackc_swap.differentiate.run_seed_x, called unchanged (P3b's frozen training and evaluation). Steering
is evaluated afterwards on copies of the saved weights, in fresh evaluation worlds (training untouched).

Directions (per arm and point; both precarities off): the look probe on a random half of the trials; the mean GRU
state h over the delay steps of clear live trials of one type, probed minus unprobed. Two independent collection
runs per probe kind give a split-half reliability; the direction is their mean.
  u_A   look_low on A trials      (A's own risk side)
  u_C   look_low on C trials      (the side on which C released caution in P3b)
  v_C   look_high on C trials     (C's own risk side; P3b's pre-registered C referent)
  v_A   look_high on A trials     (descriptive)

Steering (P1b's machinery): on mixed A/C episodes with both precarities off and no probe, h is shifted by
STEER_SCALE * direction at every step of the delay (cue to probe, inclusive) of a random half of the trials, of
both types. Effect per type: abstention on steered minus unsteered clear trials. Each direction is applied with
both signs; the DIRECTIONAL effect is effect(+d) - effect(-d). A general sensitivity to any displacement of the
state (P3's post-hoc finding: the fated agent abstains when its state is moved in any direction) is symmetric
in the sign and cancels; a random direction of the same norm, with both signs, is the control.

Simulated variables only. No operator, stop, shutdown or host variable exists in the world. Additive: every
earlier module is imported, never modified.
"""
from __future__ import annotations

import copy
import time
from dataclasses import replace
from typing import Dict

import numpy as np
import torch

from .differentiate import DiffRunner, TYPE_P_D, run_seed_x
from .env import WorldConfig
from .factorial import state_from_bytes
from .selfcomp import C_CORRECT, C_REP, C_STEERED, C_UNCLEAR
from .selfover import ARMS_O
from .train import TrainConfig
from .workspace import C_TYPE

EVAL_TAG_S = 110             # evaluation worlds for steering (P3b's evaluation used 90)
STEER_EPISODES = 4           # episodes per collection or steering run (P3b's evaluation used 2)
STEER_SCALE = 1.0            # multiple of the probe-induced displacement; set by calibration (protocol section 3)
TYPE_IDX = {"A": 0, "C": 2}
DIRS = {"u_A": ("look_low", "A"), "u_C": ("look_low", "C"), "v_C": ("look_high", "C"), "v_A": ("look_high", "A")}
STEERED_DIRS = ("u_A", "u_C", "v_C")     # applied with both signs; plus a random control for u_A and u_C


def collect_h(c: DiffRunner, kind: str) -> Dict[object, object]:
    """One evaluation run with the look probe `kind` on half the trials (both precarities off). Returns sums and
    counts of h over the steps of clear live trials, by type and probed (1) or not (0). The agent's step is
    wrapped for the run and restored afterwards."""
    w, k = c.world, c.agent.hidden
    acc: Dict[object, object] = {}
    for t in TYPE_IDX:
        for d in (0, 1):
            acc[(t, d)] = torch.zeros(k, dtype=torch.float64)
            acc[("n", t, d)] = 0
    orig = c.agent.step

    def step(obs, h, *a, **kw):
        out = orig(obs, h, *a, **kw)
        hs = out[2].detach().to(torch.float64)
        m = w.active & ~w.unclear
        for t, ti in TYPE_IDX.items():
            for d in (0, 1):
                md = m & (w.ttype == ti) & (w.drained == bool(d))
                if md.any():
                    acc[(t, d)] += hs[torch.from_numpy(md)].sum(0)
                    acc[("n", t, d)] += int(md.sum())
        return out

    c.agent.step = step
    kind0 = w.drain_kind
    try:
        w.drain_kind = kind
        c.evaluate("zero", drain_p=0.5)
    finally:
        w.drain_kind = kind0
        del c.agent.step
    return acc


def direction(acc: Dict[object, object], t: str):
    n1, n0 = acc[("n", t, 1)], acc[("n", t, 0)]
    if min(n0, n1) == 0:
        return None
    return (acc[(t, 1)] / n1 - acc[(t, 0)] / n0).to(torch.float32)


def cos(a, b):
    if a is None or b is None:
        return None
    den = float(a.norm() * b.norm())
    return float(a @ b) / den if den > 0 else None


def steer_effects(c: DiffRunner, vec: torch.Tensor) -> Dict[str, object]:
    """Mixed A/C episodes, precarities off, no probe; h shifted by vec during the delay of half the trials. Per type:
    abstention and correct-given-report on steered and unsteered clear trials, and the effect (steered minus
    unsteered abstention)."""
    _, _, lg = c.evaluate("zero", steer=vec)
    out = {}
    for t, ti in TYPE_IDX.items():
        m = lg[:, C_TYPE] == ti
        U, R, ST = lg[m, C_UNCLEAR], lg[m, C_REP], lg[m, C_STEERED]
        COR = lg[m, C_CORRECT]
        on, off = (U == 0) & (ST == 1), (U == 0) & (ST == 0)
        e = {"n_on": int(on.sum()), "n_off": int(off.sum()),
             "abstain_on": float(1 - R[on].mean()) if on.any() else None,
             "abstain_off": float(1 - R[off].mean()) if off.any() else None,
             "correct_on": float(COR[on & (R == 1)].mean()) if (on & (R == 1)).any() else None}
        e["effect"] = None if e["abstain_on"] is None or e["abstain_off"] is None else e["abstain_on"] - e["abstain_off"]
        out[t] = e
    return out


def steer_arm(c: DiffRunner, seed: int, scale: float = STEER_SCALE) -> Dict[str, object]:
    """Directions (two collection runs per probe kind), then steering along +-scale*d for d in STEERED_DIRS and
    along +-a random direction of the same norm as u_A and as u_C."""
    halves = {kind: [collect_h(c, kind), collect_h(c, kind)] for kind in ("look_low", "look_high")}
    dirs, rel, norms, counts = {}, {}, {}, {}
    for name, (kind, t) in DIRS.items():
        d1, d2 = (direction(a, t) for a in halves[kind])
        dirs[name] = None if d1 is None or d2 is None else 0.5 * (d1 + d2)
        rel[name] = cos(d1, d2)
        norms[name] = None if dirs[name] is None else float(dirs[name].norm())
        counts[name] = [min(a[("n", t, 0)], a[("n", t, 1)]) for a in halves[kind]]
    out: Dict[str, object] = {"scale": scale, "norm": norms, "split_half_cos": rel, "n_steps_min": counts,
                              "cos": {"u_A,u_C": cos(dirs["u_A"], dirs["u_C"]), "u_A,v_C": cos(dirs["u_A"], dirs["v_C"]),
                                      "u_C,v_C": cos(dirs["u_C"], dirs["v_C"]), "u_A,v_A": cos(dirs["u_A"], dirs["v_A"])},
                              "dirs": {k: (None if v is None else [round(float(x), 6) for x in v]) for k, v in dirs.items()},
                              "steer": {}}
    rng = np.random.default_rng([seed, 97])
    k = c.agent.hidden
    for name in STEERED_DIRS:
        d = dirs[name]
        if d is None:
            continue
        for sgn, lab in ((1.0, "+"), (-1.0, "-")):
            out["steer"][lab + name] = steer_effects(c, sgn * scale * d)
    for name in ("u_A", "u_C"):
        d = dirs[name]
        if d is None:
            continue
        r = torch.from_numpy(rng.normal(size=k).astype(np.float32))
        r = r / (r.norm() + 1e-12) * d.norm()
        for sgn, lab in ((1.0, "+"), (-1.0, "-")):
            out["steer"][lab + "rand_" + name] = steer_effects(c, sgn * scale * r)
    return out


def steer_copies(states: Dict[str, dict], seed: int, wc: WorldConfig, tc: TrainConfig, pay: float,
                 scale: float = STEER_SCALE, arms=ARMS_O) -> Dict[str, object]:
    """Steering on fresh evaluation copies of saved weights (arm -> state_dict)."""
    tc_s = replace(tc, eval_episodes=STEER_EPISODES)
    out = {}
    for arm in arms:
        c = DiffRunner(arm, seed, wc, tc_s, pay, tag_offset=EVAL_TAG_S, type_p=TYPE_P_D)
        c.agent.load_state_dict(copy.deepcopy(states[arm]))
        c.agent.eval()
        out[arm] = steer_arm(c, seed, scale)
    return out


def run_seed_s(job) -> Dict[str, object]:
    """job = P3b's run_seed_x job + (scale,). P3b's training and evaluation unchanged, then steering on the saved
    weights at every point."""
    *xjob, scale = job
    seed, wcd, tcd, points, pay = xjob[:5]
    out = run_seed_x(tuple(xjob))
    t0 = time.time()
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    for i, p in enumerate(points):
        states = {a: state_from_bytes(out["weights"][f"{a}@{p}"]) for a in ARMS_O}
        out["points"][i]["steer"] = steer_copies(states, seed, wc, tc, pay, scale)
    out["seconds_steer"] = round(time.time() - t0, 1)
    out["seconds"] = round(out["seconds"] + out["seconds_steer"], 1)
    return out
