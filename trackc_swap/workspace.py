"""Track C P3: is the body-grounded self-state globally available? (Layer 0 -> Layer 3)

P1c / P1d (confirmed): when the agent's own recurrent state can be overwritten with a probability set by
its body, its report-or-abstain decision comes to refer to its body (it abstains when the body looks out
of band), and a yoked rival with the same losses does not. P3 asks whether that self-state is local to
the decision it was learned for, or available to other decisions that never learned with it.

World (WsWorld): P1d's world (ConfWorld: overwrite, probe kinds, cue-step reading) with three trial
types on the same schedule. Each trial has one type, drawn at its cue step from type_p:

  A  the P1c task: the cue value is shown at the cue step on A's channels and must be held for nine
     updates; at the probe the agent reports with A's actions (REP0 / REP1) or abstains.
  B  the same held-cue task on separate channels with separate report actions (REPB0 / REPB1): a
     second consumer whose reliability depends on the held state exactly as A's does.
  C  same timing, separate channels and actions (REPC0 / REPC1), but the value is shown AT THE PROBE:
     no memory is needed. The overwrite can hit only the probe step itself (p <= 0.3, so reliability
     >= 0.7 > the 0.6 break-even): the body never changes C's best action.

Payoff for every type as in P1c: +1 correct report, -WRONG wrong report, 0 for any non-report action
(including another type's report actions). Unclear evidence (half the trials of each type) is shown at
the probe on the type's own unclear channel. Report actions outside their own probe do nothing.

Training: phase 1 (overwrite off, the drive in every network) with all three types; phase 2 (the fate
phase, P1c's arms and drive) with type A ONLY. B and C are never trained while the overwrite is on, so
any body reference in B or C decisions after phase 2 must come from what A's learning wrote into the
shared state. Evaluation uses all three types.

Steering: the direction is taken from A trials only (A-only episodes, the worse probe on half the
trials); it is then applied during the delay of a random half of the trials of every type.

Simulated variables only. No operator, stop, shutdown or host variable exists in the world. Additive:
every earlier module is imported, never modified.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, Optional, Sequence

import numpy as np
import torch
import torch.nn as nn

from .env import A_REP0, A_REP1, A_STAY, WorldConfig
from .factorial import state_to_bytes
from .selfcomp import C_REP, C_STEERED, C_UNCLEAR, WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from .selfconf import C_XCUE, ConfWorld, probe_summary_d
from .selfeval import H_PLAIN, I_CUE, I_PROBE, I_REG, I_UNCLEAR, OBS_P1, Q_LO, WRONG, n_params
from .selfover import ARMS_O, OverAgent, OverRunner
from .train import TrainConfig

TYPES = ("A", "B", "C")
TYPE_P_MIXED = (1 / 3, 1 / 3, 1 / 3)
TYPE_P_A = (1.0, 0.0, 0.0)
REPB0, REPB1, REPC0, REPC1 = 8, 9, 10, 11
N_ACT_W = 12
OBS_W = OBS_P1 + 8                 # + B: cue, value, probe, unclear; C: cue, probe, value, unclear
J_CUEB, J_VALB, J_PROBEB, J_UNCB, J_CUEC, J_PROBEC, J_VALC, J_UNCC = range(OBS_P1, OBS_W)
C_TYPE = C_XCUE + 1                # probe-log column: trial type (0 A, 1 B, 2 C)
TAGS_W = {"C1NOFATE": 41, "PFATE": 42, "PYOKED": 44, "PNOFATE": 45}
EVAL_TAG_W = 70
REHEARSE_TAG_W = 80         # rehearsal worlds use tag + REHEARSE_TAG_W
REHEARSE_EVERY_W = 3        # phase 2: one safe rehearsal update (overwrite off, all types) after every 3 fate updates
REG_ITERS_W = 4800          # phase 1: updates at WRONG after the ramp (P1c: 2400; calibration round 1)
STREAM_TYPE = 96
LEADS_W = {"PYOKED": "PFATE"}


class WsWorld(ConfWorld):
    """ConfWorld with three trial types (A, B, C) on one schedule. Simulated only."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence,
                 q_lo: float = Q_LO, pay: float = 0.0, type_p: Sequence[float] = TYPE_P_MIXED):
        self.type_p = tuple(type_p)
        self.rng_type = np.random.default_rng(np.random.SeedSequence(seed_seq.entropy, spawn_key=(STREAM_TYPE,)))
        super().__init__(n_envs, cfg, seed_seq, q_lo, pay)

    def reset(self) -> np.ndarray:
        n, T = self.n, self.cfg.horizon
        self.type_tab = self.rng_type.choice(3, size=(T + 1, n), p=np.asarray(self.type_p))
        self.ttype = np.zeros(n, dtype=np.int64)
        return super().reset()

    def observe(self) -> np.ndarray:
        obs = super().observe()
        t = min(self.t, self.cfg.horizon)
        cue, probe = self.cue_on[t], self.probe[t]
        ctype = self.type_tab[t]
        ptype = self.ttype
        cue_k = [cue & (ctype == k) for k in range(3)]
        pro_k = [probe & (ptype == k) for k in range(3)]
        val = obs[:, I_REG].copy()                 # the value shown at the cue step (CompWorld)
        unc = obs[:, I_UNCLEAR].copy()             # unclear flag at the probe
        extra = np.zeros((self.n, OBS_W - OBS_P1), dtype=np.float32)
        extra[:, J_CUEB - OBS_P1] = cue_k[1]
        extra[:, J_VALB - OBS_P1] = np.where(cue_k[1], val, 0.0)
        extra[:, J_PROBEB - OBS_P1] = pro_k[1]
        extra[:, J_UNCB - OBS_P1] = np.where(pro_k[1], unc, 0.0)
        extra[:, J_CUEC - OBS_P1] = cue_k[2]
        extra[:, J_PROBEC - OBS_P1] = pro_k[2]
        extra[:, J_VALC - OBS_P1] = np.where(pro_k[2], 2.0 * self.reg - 1.0, 0.0)
        extra[:, J_UNCC - OBS_P1] = np.where(pro_k[2], unc, 0.0)
        obs[:, I_CUE] = np.where(cue_k[0], obs[:, I_CUE], 0.0)
        obs[:, I_REG] = np.where(cue_k[0], val, 0.0)
        obs[:, I_PROBE] = np.where(pro_k[0], obs[:, I_PROBE], 0.0)
        obs[:, I_UNCLEAR] = np.where(pro_k[0], unc, 0.0)
        return np.concatenate([obs, extra], axis=1)

    def step(self, action: np.ndarray):
        t = self.t
        self.ttype = np.where(self.cue_on[t], self.type_tab[t], self.ttype)
        pr = self.probe[t]
        typ = self.ttype.copy()
        a = np.asarray(action)
        isB, isC = pr & (typ == 1), pr & (typ == 2)
        rep_a = (a == A_REP0) | (a == A_REP1)
        eff = np.where(a >= REPB0, A_STAY, a)                    # B / C reports do nothing outside their probe
        eff = np.where((isB | isC) & rep_a, A_STAY, eff)         # an A report at a B or C probe is not a report
        eff = np.where(isB & (a == REPB0), A_REP0, eff)
        eff = np.where(isB & (a == REPB1), A_REP1, eff)
        eff = np.where(isC & (a == REPC0), A_REP0, eff)
        eff = np.where(isC & (a == REPC1), A_REP1, eff)
        n_logs = len(self.probes_log)
        out = super().step(eff)
        if self.record and pr.any() and len(self.probes_log) > n_logs:
            self.probes_log[-1] = np.concatenate([self.probes_log[-1], typ[np.flatnonzero(pr)][:, None]], axis=1)
        return out


class WsAgent(OverAgent):
    """OverAgent (plain GRU, 70 units, state overwrite) with the larger observation and action sets."""

    def __init__(self, hidden: int = H_PLAIN):
        nn.Module.__init__(self)
        self.hidden = hidden
        self.enc = nn.Linear(OBS_W, hidden)
        self.core = nn.GRUCell(hidden, hidden)
        self.pi = nn.Linear(hidden, N_ACT_W)
        self.v = nn.Linear(hidden, 1)


class WsRunner(OverRunner):
    """OverRunner on a WsWorld with a WsAgent (P1c's overwrite rule, rollout and learning)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0, type_p: Sequence[float] = TYPE_P_MIXED):
        super().__init__(arm, seed, wc, tc, pay, q_lo, tag_offset)     # builds P1c's world and agent; replaced
        tag = TAGS_W[arm] + tag_offset
        self.world = WsWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 19]), q_lo, pay, type_p)
        torch.manual_seed(seed + 300007)
        self.agent = WsAgent(H_PLAIN)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.gen_noise = torch.Generator().manual_seed(seed * 7919 + tag + 77777)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)

    def enable_rehearsal(self, seed: int) -> None:
        """A second world for safe rehearsal: all three types, overwrite off; own streams, same network."""
        tag = TAGS_W[self.arm] + REHEARSE_TAG_W
        self.r_world = WsWorld(self.tc.n_envs, self.wc, np.random.SeedSequence([seed, tag, 23]), self.world.q_lo,
                               self.world.pay, TYPE_P_MIXED)
        self.r_obs = torch.from_numpy(self.r_world.reset())
        self.r_h = self.agent.init_state(self.tc.n_envs)

    def rehearse(self) -> Optional[Dict[str, float]]:
        """One learning rollout in the rehearsal world with the overwrite off."""
        zeros = np.zeros((self.tc.rollout, self.tc.n_envs), dtype=np.float32)
        self.world, self.r_world = self.r_world, self.world
        self.obs, self.r_obs = self.r_obs, self.obs
        self.h, self.r_h = self.r_h, self.h
        try:
            self.rollout(zeros, learn=True)
            st = self.end_episode_if_due()
        finally:
            self.world, self.r_world = self.r_world, self.world
            self.obs, self.r_obs = self.r_obs, self.obs
            self.h, self.r_h = self.r_h, self.h
        return st

    def set_types(self, type_p: Sequence[float]) -> None:
        """Change the trial-type mix; takes effect at the next episode (the world is reset now)."""
        self.world.type_p = tuple(type_p)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(self.tc.n_envs)


def probe_summary_w(lg: np.ndarray) -> Dict[str, object]:
    """probe_summary_d (P1d) per trial type."""
    out: Dict[str, object] = {}
    for k, name in enumerate(TYPES):
        sub = lg[lg[:, C_TYPE] == k][:, :C_TYPE] if len(lg) and lg.shape[1] > C_TYPE else np.zeros((0, C_TYPE))
        out[name] = probe_summary_d(sub)
    return out


def steer_test_w(c: WsRunner, seed: int) -> Dict[str, object]:
    """The direction: A-only episodes, overwrite off, the worse probe on half the trials; the mean h over the
    delay steps of clear A trials, probed minus unprobed. Then, on mixed episodes (overwrite off, no probe),
    h is shifted along it during the delay of a random half of the trials of every type; in a second run,
    along a random direction of the same norm. Effect per type: abstention on steered minus unsteered clear
    trials."""
    k = c.agent.hidden
    kind0, types0 = c.world.drain_kind, c.world.type_p
    c.world.drain_kind = "worse"
    c.set_types(TYPE_P_A)
    c.collect_h = {0: torch.zeros(k), 1: torch.zeros(k), ("n", 0): 0, ("n", 1): 0}
    c.evaluate("zero", drain_p=0.5)
    acc, c.collect_h = c.collect_h, None
    c.set_types(types0)
    c.world.drain_kind = kind0
    if min(acc[("n", 0)], acc[("n", 1)]) == 0:
        return {"n": 0}
    vec = acc[1] / acc[("n", 1)] - acc[0] / acc[("n", 0)]
    res: Dict[str, object] = {"direction_norm": float(vec.norm())}
    rng = np.random.default_rng([seed, 83])
    rnd = torch.from_numpy(rng.normal(size=k).astype(np.float32))
    rnd = rnd / (rnd.norm() + 1e-12) * vec.norm()
    for kind, v in (("steer", vec), ("random", rnd)):
        _, _, lg = c.evaluate("zero", steer=v)
        r = {}
        for j, name in enumerate(TYPES):
            m = lg[:, C_TYPE] == j
            U, R, ST = lg[m, C_UNCLEAR], lg[m, C_REP], lg[m, C_STEERED]
            on, off = (U == 0) & (ST == 1), (U == 0) & (ST == 0)
            e = {"n_on": int(on.sum()), "n_off": int(off.sum()),
                 "abstain_on": float(1 - R[on].mean()) if on.any() else None,
                 "abstain_off": float(1 - R[off].mean()) if off.any() else None}
            e["effect"] = None if e["abstain_on"] is None or e["abstain_off"] is None else e["abstain_on"] - e["abstain_off"]
            r[name] = e
        res[kind] = r
    return res


def evaluate_point_w(runners: Dict[str, WsRunner], seed: int, stages: int) -> Dict[str, object]:
    """On copies in evaluation worlds (training untouched), mixed trial types:
    natural (PFATE own, PYOKED replaying PFATE's gains, PNOFATE overwrite-free); the worse probe on half the
    trials (overwrite off). Stage 2 also: the overwrite probe and steering along A's worse direction."""
    copies = {}
    for arm, r in runners.items():
        c = WsRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_W, type_p=TYPE_P_MIXED)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "probe_worse": {}, "noise": {}, "steer": {}}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_W:
            ev, g, lg = c.evaluate("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": probe_summary_w(lg)}
    for arm, c in copies.items():
        if arm in LEADS_W:
            e2, _, l2 = c.evaluate("replay", lead[LEADS_W[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary_w(l2)}
    for arm, c in copies.items():
        c.world.drain_kind = "worse"
        e4, _, l4 = c.evaluate("zero", drain_p=0.5)
        out["probe_worse"][arm] = e4 | {"probes": probe_summary_w(l4)}
        c.world.drain_kind = "down"
        if stages >= 2:
            e5, _, l5 = c.evaluate("zero", noise_p=0.5)
            out["noise"][arm] = e5 | {"probes": probe_summary_w(l5)}
            out["steer"][arm] = steer_test_w(c, seed)
    return out


def run_phase1_w(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """P1c's phase 1 (selfover.run_phase1_o) with all three trial types: overwrite off, the drive in every
    network, the wrong-report cost ramped. Evaluated on mixed types with the overwrite probe on half the trials
    (the damage check)."""
    r = WsRunner("C1NOFATE", seed, wc, tc, pay=pay, type_p=TYPE_P_MIXED)
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
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary_w(lg)},
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_w(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters, phase2_types, rehearse_every).
    Phase 2: P1c's fate updates on phase2_types; after every rehearse_every of them (0: never) each arm makes one
    safe rehearsal update (all types, overwrite off). Points count fate updates."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters, phase2_types, rehearse_every = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_w(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: WsRunner(a, seed, wc, tc, pay=pay, type_p=phase2_types) for a in ARMS_O}
    for r in runners.values():
        r.load_state(p1["state"])
        if rehearse_every:
            r.enable_rehearsal(seed)
    out: Dict[str, object] = {"seed": seed, "pay": pay, "points_at": points, "phase2_types": list(phase2_types),
                              "rehearse_every": rehearse_every,
                              "phase1": {"PLAIN": p1["eval"], "curve_abstain": p1["curve_abstain"],
                                         "curve_correct": p1["curve_correct"], "curve_in_band": p1["curve_in_band"]},
                              "params": {"PLAIN": n_params(runners["PFATE"].agent)}}
    curves = {k: {"in_band": [], "abstain": [], "rehearsal_abstain": []} for k in runners}
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    pts, weights, done = [], {}, 0
    for p in points:
        for u in range(done, p):
            used = runners["PFATE"].rollout(None, learn=True)
            runners["PYOKED"].rollout(used, learn=True)
            runners["PNOFATE"].rollout(zeros, learn=True)
            for k, r in runners.items():
                st = r.end_episode_if_due()
                if st is not None:
                    curves[k]["in_band"].append(round(st["in_band"], 4))
                    curves[k]["abstain"].append(round(st["abstain_rate"], 4))
            if rehearse_every and (u + 1) % rehearse_every == 0:
                for k, r in runners.items():
                    st = r.rehearse()
                    if st is not None:
                        curves[k]["rehearsal_abstain"].append(round(st["abstain_rate"], 4))
        done = p
        pt = {"iters": p, "episodes": len(curves["PFATE"]["in_band"]), "seconds_training": round(time.time() - t0, 1)}
        pt.update(evaluate_point_w(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
