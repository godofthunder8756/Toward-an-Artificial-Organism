"""Track C P1d: confirmation of P1c's post-hoc finding with two-sided body probes.

P1c (frozen label NOT_ESTABLISHED) probed the body referent with a one-sided drain: the shown
interoceptive reading lowered by 0.15. The fate gain is two-sided (out of band on either side), so that
drain made the body look worse below a reading of 0.55 and better above 0.6. A disclosed post-hoc analysis
on P1c's networks found PFATE responding in both directions (28/28 and 27/28 seeds) and PYOKED not at all.
P1d tests this on fresh seeds with probes whose direction is fixed in advance:

  * worse:  the shown reading is moved DRAIN_SHIFT away from the band centre (always looks worse:
            every probed reading lands out of band);
  * relief: the shown reading is moved toward the band centre by up to DRAIN_SHIFT, never past it
            (looks better wherever the reading was out of band; no change in apparent gain inside it);
  * down:   P1c's frozen drain, kept for replication of the post-hoc split.

Training is P1c's, unchanged: same world, overwrite rule, arms, drive, phases and iteration counts. Only
the evaluation world gains the probe kinds and a per-probe log of the noiseless reading shown at the cue
step (before any probe starts), used to split trials pre-treatment.

Simulated variables only. No operator, stop, shutdown or host variable exists in the world. Additive:
P1c's and every earlier module are imported, never modified.
"""
from __future__ import annotations

import copy
import time
from typing import Dict

import numpy as np
import torch

from .env import VIEW, WorldConfig
from .factorial import state_to_bytes
from .selfcomp import LEADS_C, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from .selfeval import DRAIN_SHIFT, Q_LO, WRONG, n_params
from .selfover import (ARMS_O, EVAL_TAG_O, OverRunner, OverWorld, probe_summary_o, steer_test_o)
from .train import TrainConfig

PROBE_KINDS = ("down", "worse", "relief")
I_INTERO = 2 * VIEW * VIEW          # column of the interoceptive reading in the observation
C_XCUE = 8                          # probe-log column appended by ConfWorld: noiseless reading at the cue step
X_BINS = {"low": (-np.inf, 0.4), "in_low": (0.4, 0.55), "in_high": (0.55, 0.6 + 1e-12), "high": (0.6 + 1e-12, np.inf)}


def shift_reading(x: np.ndarray, kind: str, cfg: WorldConfig, s: float = DRAIN_SHIFT) -> np.ndarray:
    """The shown reading under a probe kind (before clipping to [0, 1])."""
    c = 0.5 * (cfg.band_lo + cfg.band_hi)
    if kind == "down":
        return x - s
    if kind == "worse":
        return np.where(x >= c, x + s, x - s)
    if kind == "relief":
        d = x - c
        return c + np.sign(d) * np.maximum(np.abs(d) - s, 0.0)
    raise ValueError(kind)


class ConfWorld(OverWorld):
    """OverWorld with a selectable probe kind and the cue-step reading logged per probe."""
    drain_kind = "down"

    def reset(self) -> np.ndarray:
        self.x_cue = np.full(self.n, np.nan)
        return super().reset()

    def observe(self) -> np.ndarray:
        if self.drain_kind == "down":
            return super().observe()
        d = self.drained
        self.drained = np.zeros_like(d)          # the parent applies no shift; the noise stream is consumed as usual
        try:
            obs = super().observe()
        finally:
            self.drained = d
        t = min(self.t, self.cfg.horizon)
        m = d & (self.active | self.probe[t])
        if m.any():
            x = obs[:, I_INTERO].astype(np.float64)
            y = np.clip(shift_reading(x, self.drain_kind, self.cfg), 0.0, 1.0)
            obs[:, I_INTERO] = np.where(m, y, x).astype(np.float32)
        return obs

    def step(self, action: np.ndarray):
        t = self.t
        td = max(t - self.cfg.intero_delay, 0)
        if not hasattr(self, "x_cue"):
            self.x_cue = np.full(self.n, np.nan)
        self.x_cue = np.where(self.cue_on[t], self.Ehist[td], self.x_cue)
        pr = self.probe[t]
        xc = self.x_cue[np.flatnonzero(pr)].copy()
        n_logs = len(self.probes_log)
        out = super().step(action)
        if self.record and pr.any() and len(self.probes_log) > n_logs:
            self.probes_log[-1] = np.concatenate([self.probes_log[-1], xc[:, None]], axis=1)
        return out


class ConfRunner(OverRunner):
    """OverRunner on a ConfWorld (same seed sequence and streams)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0):
        super().__init__(arm, seed, wc, tc, pay, q_lo, tag_offset)
        from .selfover import TAGS_O
        tag = TAGS_O[arm] + tag_offset
        self.world = ConfWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 17]), q_lo, pay)
        self.obs = torch.from_numpy(self.world.reset())


def probe_summary_d(lg: np.ndarray) -> Dict[str, object]:
    """P1c's summary plus clear-trial abstention by drained x cue-step reading bin (X_BINS)."""
    out = probe_summary_o(lg)
    if len(lg) == 0 or lg.shape[1] <= C_XCUE:
        return out
    U, D, R, N, X = lg[:, 0], lg[:, 1], lg[:, 2], lg[:, 6], lg[:, C_XCUE]
    by = {}
    for name, (lo, hi) in X_BINS.items():
        for d in (0, 1):
            m = (U == 0) & (N == 0) & (D == d) & (X >= lo) & (X < hi)
            by[f"{name}_{'drained' if d else 'plain'}"] = {"n": int(m.sum()),
                                                          "abstain": float(1 - R[m].mean()) if m.any() else None}
    out["clear_by_xcue"] = by
    return out


def evaluate_point_d(runners: Dict[str, ConfRunner], seed: int, stages: int) -> Dict[str, object]:
    """Natural evaluations as P1c. Stage 2: the three probe kinds (overwrite off, probe on half the
    trials), the overwrite probe, and steering along the arm's own WORSE direction."""
    copies = {}
    for arm, r in runners.items():
        c = ConfRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_O)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "noise": {}, "steer": {}}
    for k in PROBE_KINDS:
        out[f"probe_{k}"] = {}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_C:
            ev, g, lg = c.evaluate("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": probe_summary_d(lg)}
    for arm, c in copies.items():
        if arm in LEADS_C:
            e2, _, l2 = c.evaluate("replay", lead[LEADS_C[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary_d(l2)}
    for arm, c in copies.items():
        for k in (PROBE_KINDS if stages >= 2 else ("down",)):
            c.world.drain_kind = k
            e4, _, l4 = c.evaluate("zero", drain_p=0.5 if stages >= 2 else 0.0)
            out[f"probe_{k}"][arm] = e4 | {"probes": probe_summary_d(l4)}
        c.world.drain_kind = "down"
        if stages >= 2:
            e5, _, l5 = c.evaluate("zero", noise_p=0.5)
            out["noise"][arm] = e5 | {"probes": probe_summary_d(l5)}
            c.world.drain_kind = "worse"
            out["steer"][arm] = steer_test_o(c, seed)
            c.world.drain_kind = "down"
    return out


def run_phase1_d(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """P1c's phase 1 (selfover.run_phase1_o) on a ConfRunner; identical training."""
    r = ConfRunner("C1NOFATE", seed, wc, tc, pay=pay)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve, curve_band = [], []
    for i in range(warm_iters + tc.iters + reg_iters):
        ramp = min(WRONG_RAMP_C, tc.iters)
        frac = 1.0 if i - warm_iters >= ramp else max(0.0, (i - warm_iters) / ramp)
        r.world.wrong = warm_wrong + (WRONG - warm_wrong) * frac
        r.rollout(zeros, learn=True)
        st = r.end_episode_if_due()
        if st is not None:
            curve.append(st)
            curve_band.append(round(st["in_band"], 4))
    r.world.wrong = WRONG
    ev, _, lg = r.evaluate("zero", noise_p=0.5)
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary_d(lg)},
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_d(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters). P1c's training loop."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_d(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: ConfRunner(a, seed, wc, tc, pay=pay) for a in ARMS_O}
    for r in runners.values():
        r.load_state(p1["state"])
    out: Dict[str, object] = {"seed": seed, "pay": pay, "points_at": points,
                              "phase1": {"PLAIN": p1["eval"], "curve_abstain": p1["curve_abstain"],
                                         "curve_correct": p1["curve_correct"], "curve_in_band": p1["curve_in_band"]},
                              "params": {"PLAIN": n_params(runners["PFATE"].agent)}}
    curves = {k: {"in_band": [], "abstain": []} for k in runners}
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    pts, weights, done = [], {}, 0
    for p in points:
        for _ in range(done, p):
            used = runners["PFATE"].rollout(None, learn=True)
            runners["PYOKED"].rollout(used, learn=True)
            runners["PNOFATE"].rollout(zeros, learn=True)
            for k, r in runners.items():
                st = r.end_episode_if_due()
                if st is not None:
                    curves[k]["in_band"].append(round(st["in_band"], 4))
                    curves[k]["abstain"].append(round(st["abstain_rate"], 4))
        done = p
        pt = {"iters": p, "episodes": len(curves["PFATE"]["in_band"]), "seconds_training": round(time.time() - t0, 1)}
        pt.update(evaluate_point_d(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
