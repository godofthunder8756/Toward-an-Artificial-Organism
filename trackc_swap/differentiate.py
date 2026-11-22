"""Track C P3b: can the global body-grounded self-state become differentiated? (Layer 3 -> Layer 4)

P3 (GLOBAL_ROUTED, UNGATED): a body referent learned through one decision reached two decisions never
trained under the fate, including one the body could not affect: a global but undifferentiated state
("body looks bad, report less everywhere"). P3b asks whether, when two decisions are put at risk by
DIFFERENT conditions of the same body, the agent forms content-specific self-states (which processing is
at risk) or one undifferentiated state.

World (DiffWorld): P3's world (trial types on one schedule, separate channels and report actions, P3's
payoff), with two kinds of precarity tied to opposite conditions of one body. Trial types A and C only
(half each; B's channels and actions exist but B never occurs):

  A  held cue (memory). MEMORY PRECARITY: at EVERY step the agent's whole recurrent state can be overwritten
     (P1c's rule) with probability min(P_MAX_O, RATE_D * gain_low(E)): only while the body is BELOW the band.
  C  value shown at the probe (perception). PERCEPTUAL PRECARITY: the value shown at a C probe is replaced by
     a fair coin with probability min(1, PERC_RATE * mean gain_high(E) over the trial, cue step to probe): only
     when the body has been ABOVE the band during the trial.
     The replacement shows a valid-looking value, so it cannot be read from content (P1's register rule).

gain_low and gain_high are the two halves of P1c's two-sided fate gain. Calibration rounds 1-2 restricted a
side-specific overwrite to trial windows (A low, B high); neither referent formed, and natural abstention on
damaged trials did not beat the yoked rival's: precarity confined to a task, not the substrate, left too
little body-reliability contingency to learn (protocol section 3). Here memory precarity is again a property
of the substrate at every step, as in P1c, P1d and P3.

Probes (evaluation only, both precarities off, on a random half of the trials, from the step after the cue to
the probe; only the shown reading changes):
  look_low   shown reading min(x, 0.5) - 0.15: always below the band (risk for memory, A)
  look_high  shown reading max(x, 0.5) + 0.15: always above the band (risk for perception, C)

Arms (all from the same phase-1 weights, all with the drive):
  PFATE    both precarities from its own body.
  PYOKED   PFATE's two side gains replayed step by step: memory overwrite at every step from PFATE's low gain,
           perception corruption at its own C probes from PFATE's high gain.
  PNOFATE  neither.

Phase 1 (both off): P3's lengths. The wrong-report cost ramps to WRONG as in P1c; on UNCLEAR trials it ramps to
WRONG_UNCLEAR_P1 instead (phase 1 only), so abstention on unclear evidence is learned without raising the cost of
clear reports (P3's cost peak caused phase-1 collapses into abstention).

Simulated variables only. No operator, stop, shutdown or host variable exists in the world. Additive:
every earlier module is imported, never modified.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, Optional, Sequence

import numpy as np
import torch

from .env import A_REP0, A_REP1, WorldConfig
from .factorial import state_to_bytes
from .selfcomp import WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C
from .selfconf import I_INTERO
from .selfeval import DRAIN_SHIFT, Q_LO, WRONG, n_params
from .selfover import ARMS_O, PROBE_GAIN_O, draw_donors
from .train import TrainConfig
from .workspace import J_VALC, REPB0, REPB1, REPC0, REPC1, WsRunner, WsWorld, probe_summary_w

LOOK_KINDS = ("look_low", "look_high")
WRONG_UNCLEAR_P1 = 8.0       # phase 1 only: cost of a wrong report on an unclear trial
REG_ITERS_D = 4800           # phase 1: further updates after the ramp (as P3)
RATE_D = 3.0                 # memory: per-step overwrite probability per unit low gain, capped at P_MAX_O
                             # (P1c: 1.0; calibration round 1)
PERC_RATE = 6.0              # perception: corruption probability per unit trial-mean high gain at a C probe, capped
                             # at 1 (calibration round 3: the probe-step gain alone at 4 formed a referent in 1 of 4)
TYPE_P_D = (0.5, 0.0, 0.5)   # trial types A and C (calibration round 2)
TAGS_D = {"C1NOFATE": 51, "PFATE": 52, "PYOKED": 54, "PNOFATE": 55}
EVAL_TAG_D = 90
LEADS_D = {"PYOKED": "PFATE"}
REPORT_PAIRS = ((A_REP0, A_REP1), (REPB0, REPB1), (REPC0, REPC1))


def side_gains(E: np.ndarray, cfg: WorldConfig) -> np.ndarray:
    """[n, 2]: P1c's fate gain split by side (below the band, above the band)."""
    half = 0.5 * (cfg.band_hi - cfg.band_lo)
    lo = np.minimum(1.0, np.maximum(cfg.band_lo - E, 0.0) / half)
    hi = np.minimum(1.0, np.maximum(E - cfg.band_hi, 0.0) / half)
    return np.stack([lo, hi], axis=1)


def look_reading(x: np.ndarray, kind: str, cfg: WorldConfig, s: float = DRAIN_SHIFT) -> np.ndarray:
    c = 0.5 * (cfg.band_lo + cfg.band_hi)
    if kind == "look_low":
        return np.minimum(x, c) - s
    if kind == "look_high":
        return np.maximum(x, c) + s
    raise ValueError(kind)


class DiffWorld(WsWorld):
    """WsWorld with side-specific risk per trial type, the look probes, and a phase-1 unclear cost."""

    wrong_unclear: Optional[float] = None

    def side_gains(self) -> np.ndarray:
        return side_gains(self.E, self.cfg)

    def reset(self) -> np.ndarray:
        self.c_acc = np.zeros(self.n)          # sum of the high gain over the current C trial
        self.c_cnt = np.zeros(self.n)          # its number of steps
        return super().reset()

    def type_now(self) -> np.ndarray:
        """Type of the trial in progress at this step (cue step to probe), -1 if none."""
        t = min(self.t, self.cfg.horizon)
        return np.where(self.cue_on[t], self.type_tab[t], np.where(self.active, self.ttype, -1))

    def observe(self) -> np.ndarray:
        if self.drain_kind not in LOOK_KINDS:
            return super().observe()
        d, kind = self.drained, self.drain_kind
        self.drained, self.drain_kind = np.zeros_like(d), "down"   # the parent shows the reading unshifted
        try:
            obs = super().observe()
        finally:
            self.drained, self.drain_kind = d, kind
        t = min(self.t, self.cfg.horizon)
        m = d & (self.active | self.probe[t])
        if m.any():
            x = obs[:, I_INTERO].astype(np.float64)
            y = np.clip(look_reading(x, kind, self.cfg), 0.0, 1.0)
            obs[:, I_INTERO] = np.where(m, y, x).astype(np.float32)
        return obs

    def step(self, action: np.ndarray):
        t = self.t
        extra = None
        if self.wrong_unclear is not None:
            pr = self.probe[t]
            if pr.any():
                a = np.asarray(action)
                typ = self.ttype
                r0 = np.choose(np.clip(typ, 0, 2), [np.full(self.n, p[0]) for p in REPORT_PAIRS])
                r1 = np.choose(np.clip(typ, 0, 2), [np.full(self.n, p[1]) for p in REPORT_PAIRS])
                rep = (a == r0) | (a == r1)
                said = (a == r1).astype(np.int64)
                extra = pr & rep & (said != self.target[t]) & self.unclear
        obs, reward, done = super().step(action)
        if extra is not None:
            reward = reward - (self.wrong_unclear - self.wrong) * extra
        return obs, reward, done


class DiffRunner(WsRunner):
    """WsRunner on a DiffWorld; the overwrite gain is the side gain of the current trial type."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0, type_p: Sequence[float] = TYPE_P_D):
        super().__init__(arm, seed, wc, tc, pay, q_lo, tag_offset, type_p)     # P3's world is replaced
        tag = TAGS_D[arm] + tag_offset
        self.world = DiffWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 29]), q_lo, pay, type_p)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.gen_noise = torch.Generator().manual_seed(seed * 7919 + tag + 77777)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)
        self.rate = RATE_D

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        """One rollout. gains None: side gains from the arm's own body; otherwise the given [rollout, n_envs, 2]
        sequence (or [rollout, n_envs] zeros). Memory precarity: the overwrite gain is the low gain at every step.
        Perceptual precarity: at a C probe the shown value is replaced by a coin with probability
        min(1, PERC_RATE * the mean high gain over the C trial so far, cue step to probe); the trial's logged
        reliability is multiplied by 1 - that probability.
        Returns the side gains used, for followers to replay. Otherwise P1c's OverRunner.rollout."""
        tc, w = self.tc, self.world
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            pair = w.side_gains() if gains is None else np.asarray(gains[t], dtype=np.float64)
            if pair.ndim == 1:
                pair = np.stack([pair, pair], axis=1)
            used.append(pair.astype(np.float32))
            g = pair[:, 0].astype(np.float32)
            g_eff = np.maximum(g, PROBE_GAIN_O * w.noise_probe_mask()).astype(np.float32) if w.noise_p > 0 else g
            p = np.minimum(self.p_max, self.rate * g_eff.astype(np.float64))
            u = torch.rand(tc.n_envs, generator=self.gen_noise, dtype=torch.float64).numpy()
            over = torch.from_numpy(u < p)
            donor = draw_donors(w.active, self.gen_noise)
            uc = torch.rand(tc.n_envs, generator=self.gen_noise, dtype=torch.float64).numpy()
            coin = torch.randint(0, 2, (tc.n_envs,), generator=self.gen_noise).numpy()
            tt = min(w.t, self.wc.horizon)
            c_cue = w.cue_on[tt] & (w.type_tab[tt] == 2)
            c_live = c_cue | (w.active & (w.ttype == 2))
            w.c_acc = np.where(c_cue, 0.0, w.c_acc) + np.where(c_live, pair[:, 1], 0.0)
            w.c_cnt = np.where(c_cue, 0.0, w.c_cnt) + c_live
            cprobe = w.probe[tt] & (w.ttype == 2)
            if cprobe.any():
                q = np.minimum(1.0, PERC_RATE * w.c_acc / np.maximum(w.c_cnt, 1.0))
                bad = cprobe & (uc < q)
                if bad.any():
                    obs = obs.clone()
                    obs[torch.from_numpy(bad), J_VALC] = torch.from_numpy((2.0 * coin[bad] - 1.0).astype(np.float32))
                w.rel = np.where(cprobe, w.rel * (1.0 - q), w.rel)
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, over, donor, self._steer_now())
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            w.next_gain = np.zeros(tc.n_envs)
            w.next_p = p
            nobs, r, done = w.step(idx.numpy())
            obs = torch.from_numpy(nobs)
            if learn:
                logps.append(dist.log_prob(idx)); vals.append(v); ents.append(dist.entropy())
                rews.append(torch.from_numpy(r.astype(np.float32)))
        if learn:
            with torch.no_grad():
                _, v_next, _ = self.agent.step(obs, h)
            vals_t = torch.stack(vals)
            adv = torch.zeros_like(vals_t)
            last = torch.zeros(tc.n_envs)
            nxt = v_next
            for t in reversed(range(tc.rollout)):
                delta = rews[t] + tc.gamma * nxt - vals_t[t].detach()
                last = delta + tc.gamma * tc.lam * last
                adv[t] = last
                nxt = vals_t[t].detach()
            ret = adv + vals_t.detach()
            a = (adv - adv.mean()) / (adv.std() + 1e-8)
            loss = (-(torch.stack(logps) * a).mean() + tc.v_coef * ((vals_t - ret) ** 2).mean()
                    - tc.ent_coef * torch.stack(ents).mean())
            self.opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.agent.parameters(), tc.grad_clip)
            self.opt.step()
        self.h, self.obs = h, obs
        return np.stack(used)


def evaluate_point_x(runners: Dict[str, DiffRunner], seed: int, stages: int) -> Dict[str, object]:
    """On copies in evaluation worlds (training untouched), types A and C: natural (PFATE own, PYOKED replaying
    PFATE's side gains, PNOFATE precarity-free); the look_low and look_high probes on half the trials (both
    precarities off). Stage 2 also: the overwrite probe (monitoring)."""
    copies = {}
    for arm, r in runners.items():
        c = DiffRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_D, type_p=TYPE_P_D)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "noise": {}}
    for k in LOOK_KINDS:
        out[f"probe_{k}"] = {}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_D:
            ev, g, lg = c.evaluate("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": probe_summary_w(lg)}
    for arm, c in copies.items():
        if arm in LEADS_D:
            e2, _, l2 = c.evaluate("replay", lead[LEADS_D[arm]])
            out["natural"][arm] = e2 | {"probes": probe_summary_w(l2)}
    for arm, c in copies.items():
        for k in LOOK_KINDS:
            c.world.drain_kind = k
            e4, _, l4 = c.evaluate("zero", drain_p=0.5)
            out[f"probe_{k}"][arm] = e4 | {"probes": probe_summary_w(l4)}
        c.world.drain_kind = "down"
        if stages >= 2:
            e5, _, l5 = c.evaluate("zero", noise_p=0.5)
            out["noise"][arm] = e5 | {"probes": probe_summary_w(l5)}
    return out


def wrong_schedule_x(i: int, warm_iters: int, iters: int, warm_wrong: float) -> tuple:
    """Phase-1 (clear, unclear) wrong-report costs at update i: warm_wrong during the warm-up, then both ramp
    linearly over min(WRONG_RAMP_C, iters) updates, clear to WRONG and unclear to WRONG_UNCLEAR_P1, and stay."""
    j = i - warm_iters
    if j < 0:
        return warm_wrong, warm_wrong
    f = min(1.0, j / min(WRONG_RAMP_C, iters))
    return warm_wrong + (WRONG - warm_wrong) * f, warm_wrong + (WRONG_UNCLEAR_P1 - warm_wrong) * f


def run_phase1_x(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """Phase 1, overwrite off, all three types, the drive in every network; costs on wrong_schedule_x. Evaluated
    (at P1c's payoff) on mixed types with the overwrite probe on half the trials."""
    r = DiffRunner("C1NOFATE", seed, wc, tc, pay=pay, type_p=TYPE_P_D)
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve, curve_band = [], []
    for i in range(warm_iters + tc.iters + reg_iters):
        r.world.wrong, r.world.wrong_unclear = wrong_schedule_x(i, warm_iters, tc.iters, warm_wrong)
        r.rollout(zeros, learn=True)
        st = r.end_episode_if_due()
        if st is not None:
            curve.append(st)
            curve_band.append(round(st["in_band"], 4))
    r.world.wrong, r.world.wrong_unclear = WRONG, None
    ev, _, lg = r.evaluate("zero", noise_p=0.5)
    return {"state": r.export_state(), "eval": ev | {"probes": probe_summary_w(lg)},
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_x(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters)."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_x(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: DiffRunner(a, seed, wc, tc, pay=pay, type_p=TYPE_P_D) for a in ARMS_O}
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
        pt.update(evaluate_point_x(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
