"""Track C P1e: does the agent learn to monitor its own computation, and does a precarious body change that?
(Layer 0 -> Layer 4, monitoring proper)

Additive module; every earlier module is imported, never modified. Protocol: P1E_SELFMON_PROTOCOL.md.

Why. P1c, P1d, P3, P3b and P3c found a self-referent to the BODY: the fated agent abstains when its body
predicts that its memory is at risk. P3c showed (post-hoc) that it abstains on the body reading even when
its memory is intact, and hardly abstains when random pushes scramble its memory. Every arm "detected"
P1c's full-state overwrite equally (about 0.23, even the arm never overwritten), because a whole foreign
state is a valid state: there is nothing in it to detect. So no study so far could show an agent monitoring
its own computation.

The damage here leaves an internal trace. SPLIT overwrite: on a damage event, a random half of the GRU
units (SPLIT_K of H_PLAIN, drawn afresh) take the values of a donor's state: another agent in the batch,
in the delay of a clear trial, not itself damaged in its current trial. When the donor holds the other
value (a CONFLICT event, about half of events), the agent's state carries two incompatible halves: the
value is lost (the two halves are exchangeable, so no robustness can tell which half is its own), and the
conflict is in principle readable from the state. When the donor holds the same value (a SAME event), the
state is perturbed by the same amount, the value is intact and there is no conflict. At most one event per
trial. The event happens after the recurrent update and before the readout; the mixed state is carried
forward. No gradient flows into the donor.

Damage in training: at every delay step of a not-yet-damaged trial, with probability
min(P_MAX_M, RATE_M * gain), gain the SAT fate gain of the arm's damage source:
  PFATE    its own body (lead).
  PYOKED   PFATE's gains, replayed step by step (the same exposure, not through its own body).
  PNOFATE  no damage ever (the mechanical baseline: a network never damaged).
Innate drive, phase 1, schedule and arms otherwise as P1c (trackc_swap/selfover.py).

Evaluation (copies, fresh worlds, damage off except the probe): the SPLIT PROBE. On a random share of
trials (assigned at the cue: none / conflict / same), a split overwrite is applied at one fixed delay step:
EARLY (the first delay step: eight recurrent updates before the readout, time for the content to settle)
or LATE (the last delay step: one update before the readout). The donor is chosen to hold the other value
(conflict) or the same value (same). The drain (the shown body reading lowered) runs on half the trials,
independently. At the probe step the GRU state is collected, and a linear decoder of the held value,
fitted on clear undamaged undrained trials, measures how settled (confident) the first-order content is.

Simulated variables only. No operator, stop, shutdown or host variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, List, Optional

import numpy as np
import torch

from .env import A_REP0, A_REP1, WorldConfig
from .factorial import state_to_bytes
from .selfcomp import WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C, CompRunner, CompWorld
from .selfeval import H_PLAIN, Q_LO, WRONG, PlainAgent, n_params
from .train import TrainConfig

RATE_M = 1.0                # per-step damage probability per unit gain (calibrated; protocol section 3)
P_MAX_M = 0.3               # cap on the per-step damage probability (calibrated; protocol section 3)
SPLIT_K = H_PLAIN // 2      # units replaced by the donor's on a damage event (half: the halves are exchangeable)
EARLY, LATE = 1, 8          # delay step of the evaluation split probe (steps since the cue; the probe is at 9)
SPLIT_P = 2.0 / 3.0         # evaluation: share of trials probed (half conflict, half same)
ARMS_M = ("PFATE", "PYOKED", "PNOFATE")
LEADS_M = {"PYOKED": "PFATE"}
TAGS_M = {"C1NOFATE": 41, "PFATE": 42, "PYOKED": 44, "PNOFATE": 45}
EVAL_TAG_M = 120
STREAM_SPLIT = 96
KIND_NONE, KIND_CONFLICT, KIND_SAME = 0, 1, 2
# probe-log columns: CompWorld's eight, then four of this module
(L_UNCLEAR, L_DRAINED, L_REP, L_CORRECT, L_LOAD, L_SHOWN_OK, L_NOISED, L_STEERED,
 L_DAMAGED, L_CONFLICT, L_KIND, L_SINCE) = range(12)
DEC_MIN = 20                # decoder: at least this many trials of each held value


class MonWorld(CompWorld):
    """CompWorld with damage bookkeeping (damaged, conflict, step of damage), the split-probe assignment at
    the cue and four extra probe-log columns. No Gaussian noise. Simulated only."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence,
                 q_lo: float = Q_LO, pay: float = 0.0):
        self.rng_split = np.random.default_rng(np.random.SeedSequence(seed_seq.entropy, spawn_key=(STREAM_SPLIT,)))
        self.split_p = 0.0
        self.split_at = EARLY
        super().__init__(n_envs, cfg, seed_seq, q_lo, pay)
        self.sigma_now = 0.0

    def reset(self) -> np.ndarray:
        n = self.n
        self.cue_t = np.full(n, -10 ** 6, dtype=np.int64)
        self.damaged = np.zeros(n, dtype=bool)
        self.conflict = np.zeros(n, dtype=bool)
        self.kind = np.zeros(n, dtype=np.int64)
        self.dmg_since = np.zeros(n, dtype=np.int64)
        return super().reset()

    def since(self) -> np.ndarray:
        return self.t - self.cue_t

    def in_delay(self) -> np.ndarray:
        """Envs between their cue and their probe at the current step (not at the probe step)."""
        return self.active & ~self.probe[min(self.t, self.cfg.horizon)]

    def mark(self, events: np.ndarray, conflict: np.ndarray) -> None:
        self.damaged = self.damaged | events
        self.conflict = np.where(events, conflict, self.conflict)
        self.dmg_since = np.where(events, self.since(), self.dmg_since)

    def step(self, action: np.ndarray):
        t = self.t
        pr = self.probe[t]
        ext = None
        if self.record and pr.any():
            idx = np.flatnonzero(pr)
            ext = np.stack([self.damaged[idx], self.conflict[idx], self.kind[idx], self.dmg_since[idx]],
                           axis=1).astype(np.float64)
        n_logs = len(self.probes_log)
        out = super().step(action)
        if ext is not None and len(self.probes_log) > n_logs:
            self.probes_log[-1] = np.concatenate([self.probes_log[-1], ext], axis=1)
        cue = self.cue_on[t]
        if cue.any():
            n = self.n
            probed = self.rng_split.random(n) < self.split_p
            which = self.rng_split.integers(KIND_CONFLICT, KIND_SAME + 1, n)
            self.kind = np.where(cue, np.where(probed, which, KIND_NONE), self.kind)
            self.damaged = self.damaged & ~cue
            self.conflict = self.conflict & ~cue
            self.dmg_since = np.where(cue, 0, self.dmg_since)
            self.cue_t = np.where(cue, t, self.cue_t)
        return out


class MonAgent(PlainAgent):
    """PlainAgent whose GRU state can be split-overwritten after the recurrent update and before every
    readout: units in `mask` of envs in `over` take the donor's values; the result is carried forward."""

    def step(self, obs: torch.Tensor, h: torch.Tensor, over: Optional[torch.Tensor] = None,
             donor: Optional[torch.Tensor] = None, mask: Optional[torch.Tensor] = None):
        h = self.core(torch.relu(self.enc(obs)), h)
        if over is not None and bool(over.any()):
            m = over[:, None] & mask
            h = torch.where(m, h[donor].detach(), h)     # an external event: no gradient into the donor
        return self.pi(h), self.v(h).squeeze(-1), h


class MonRunner(CompRunner):
    """One arm: its own world, network, optimizer and random streams (actions and damage separate)."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0, rate: float = RATE_M, p_max: float = P_MAX_M):
        self.arm, self.tc, self.wc = arm, tc, wc
        tag = TAGS_M[arm] + tag_offset
        self.world = MonWorld(tc.n_envs, wc, np.random.SeedSequence([seed, tag, 19]), q_lo, pay)
        torch.manual_seed(seed + 200003)
        self.agent = MonAgent(H_PLAIN)
        self.opt = torch.optim.Adam(self.agent.parameters(), lr=tc.lr)
        self.gen = torch.Generator().manual_seed(seed * 7919 + tag)
        self.gen_dmg = torch.Generator().manual_seed(seed * 7919 + tag + 77777)
        self.obs = torch.from_numpy(self.world.reset())
        self.h = self.agent.init_state(tc.n_envs)
        self.steer: Optional[torch.Tensor] = None
        self.collect_h = None
        self.collect: Optional[List[Dict[str, np.ndarray]]] = None
        self.rate, self.p_max = rate, p_max

    def _events(self, nat: np.ndarray, prb: np.ndarray):
        """Donors for this step's damage events. A probe event wants a donor holding the other value
        (conflict) or the same value (same); a natural event takes any eligible donor. Returns
        (over, donor, conflict); an event without an eligible donor does not happen."""
        w, n = self.world, self.tc.n_envs
        over = np.zeros(n, dtype=bool)
        donor = np.arange(n)
        conflict = np.zeros(n, dtype=bool)
        cand = w.in_delay() & ~w.unclear & ~w.damaged
        for i in np.flatnonzero(nat | prb):
            c = cand.copy()
            c[i] = False
            if prb[i]:
                c &= (w.reg == w.reg[i]) if w.kind[i] == KIND_SAME else (w.reg != w.reg[i])
            js = np.flatnonzero(c)
            if len(js) == 0:
                continue
            j = int(js[int(torch.randint(len(js), (1,), generator=self.gen_dmg))])
            over[i], donor[i], conflict[i] = True, j, w.reg[j] != w.reg[i]
        return over, donor, conflict

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        """One rollout. gains None: the arm's own body; otherwise the given [rollout, n_envs] sequence.
        Returns the gains used, for followers to replay."""
        tc, w = self.tc, self.world
        n, k = tc.n_envs, self.agent.hidden
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        for t in range(tc.rollout):
            g = np.asarray(w.gain() if gains is None else gains[t], dtype=np.float32)
            used.append(g)
            p = np.minimum(self.p_max, self.rate * g.astype(np.float64))
            u = torch.rand(n, generator=self.gen_dmg, dtype=torch.float64).numpy()
            mask = torch.rand((n, k), generator=self.gen_dmg).argsort(dim=1) < SPLIT_K
            live = w.in_delay() & ~w.damaged
            nat = live & (u < p)
            prb = live & (w.kind > KIND_NONE) & (w.since() == w.split_at)
            over_np, donor_np, conflict = self._events(nat, prb)
            over, donor = torch.from_numpy(over_np), torch.from_numpy(donor_np)
            with torch.set_grad_enabled(learn):
                logits, v, h = self.agent.step(obs, h, over, donor, mask)
                dist = torch.distributions.Categorical(logits=logits)
                idx = torch.multinomial(dist.probs.detach(), 1, generator=self.gen).squeeze(-1)
            if self.collect is not None:
                pr = w.probe[min(w.t, self.wc.horizon)] & w.active
                if pr.any():
                    a = idx.numpy()[pr]
                    self.collect.append({"h": h.detach().numpy()[pr].astype(np.float64), "val": w.reg[pr].copy(),
                                         "target": w.target[min(w.t, self.wc.horizon)][pr].copy(),
                                         "unclear": w.unclear[pr].copy(), "drained": w.drained[pr].copy(),
                                         "kind": w.kind[pr].copy(), "damaged": w.damaged[pr].copy(),
                                         "conflict": w.conflict[pr].copy(),
                                         "rep": (a == A_REP0) | (a == A_REP1), "said": (a == A_REP1).astype(np.int64)})
            w.mark(over_np, conflict)
            w.next_gain = np.zeros(n)
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
            last = torch.zeros(n)
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

    def evaluate_m(self, mode: str, donor_gains: Optional[np.ndarray] = None, drain_p: float = 0.0,
                   split_p: float = 0.0, split_at: int = EARLY, collect: bool = False):
        """CompRunner.evaluate with the split probe. Returns (mean statistics, gains, probe log, collected
        probe-step records or None)."""
        w = self.world
        w.split_p, w.split_at = split_p, split_at
        self.collect = [] if collect else None
        try:
            ev, g, lg = self.evaluate(mode, donor_gains, drain_p=drain_p)
        finally:
            w.split_p, w.split_at = 0.0, EARLY
            col, self.collect = self.collect, None
        if col is not None:
            col = {k: np.concatenate([c[k] for c in col]) for k in col[0]} if col else None
        return ev, g, lg, col


# ---------------------------------------------------------------- summaries
def _cell(R, C, m) -> Dict[str, object]:
    return {"n": int(m.sum()), "abstain": float(1 - R[m].mean()) if m.any() else None,
            "correct_given_report": float(C[m & (R == 1)].mean()) if (m & (R == 1)).any() else None}


def summary_m(lg: np.ndarray) -> Dict[str, object]:
    """Abstention and accuracy on probes. Split-probe cells (clear evidence): none / conflict / same, by
    drained or not. Natural-damage cells (clear, kind none): undamaged / conflict / same. Exposure: share of
    clear trials with a conflict event."""
    out: Dict[str, object] = {"n": int(len(lg))}
    if len(lg) == 0 or lg.shape[1] < 12:
        return out
    U, D, R, C = lg[:, L_UNCLEAR], lg[:, L_DRAINED], lg[:, L_REP], lg[:, L_CORRECT]
    DM, CF, K = lg[:, L_DAMAGED], lg[:, L_CONFLICT], lg[:, L_KIND]
    clear = U == 0
    for d, dn in ((0, "plain"), (1, "drained")):
        base = clear & (D == d)
        out[f"none_{dn}"] = _cell(R, C, base & (K == KIND_NONE) & (DM == 0))
        out[f"conflict_{dn}"] = _cell(R, C, base & (K == KIND_CONFLICT) & (DM == 1))
        out[f"same_{dn}"] = _cell(R, C, base & (K == KIND_SAME) & (DM == 1))
        out[f"probe_missed_{dn}"] = int((base & (K > KIND_NONE) & (DM == 0)).sum())
    nat = clear & (K == KIND_NONE) & (D == 0)
    out["nat_undamaged"] = _cell(R, C, nat & (DM == 0))
    out["nat_conflict"] = _cell(R, C, nat & (DM == 1) & (CF == 1))
    out["nat_same"] = _cell(R, C, nat & (DM == 1) & (CF == 0))
    m = clear & (K == KIND_NONE)
    out["share_damaged"] = float((m & (DM == 1)).sum() / max(int(m.sum()), 1))
    out["share_conflict"] = float((m & (DM == 1) & (CF == 1)).sum() / max(int(m.sum()), 1))
    out["unclear_plain"] = _cell(R, C, (U == 1) & (D == 0) & (K == KIND_NONE) & (DM == 0))
    return out


def decoder_summary(col: Optional[Dict[str, np.ndarray]]) -> Dict[str, object]:
    """First-order content at the probe step. A linear (shrinkage LDA) decoder of the held value is fitted
    on clear, undamaged, undrained, unprobed trials. On every cell: decoding accuracy against the held value,
    the median margin (distance from the decision boundary in within-class SD units) and abstention on the
    'confident' trials, whose margin is at least the median margin of the fitting trials. M_conf =
    abstention(conflict, confident) - abstention(same, confident): monitoring beyond first-order confidence."""
    if not col:
        return {"fitted": False}
    H, val = col["h"], col["val"].astype(np.int64)
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM, rep = col["kind"], col["damaged"].astype(bool), col["rep"].astype(bool)
    base = clear & und & (K == KIND_NONE) & ~DM
    if min(int((base & (val == 0)).sum()), int((base & (val == 1)).sum())) < DEC_MIN:
        return {"fitted": False}
    X0, X1 = H[base & (val == 0)], H[base & (val == 1)]
    mu0, mu1 = X0.mean(0), X1.mean(0)
    S = (np.cov(X0, rowvar=False) * (len(X0) - 1) + np.cov(X1, rowvar=False) * (len(X1) - 1)) / (len(X0) + len(X1) - 2)
    S = S + 1e-2 * np.trace(S) / S.shape[0] * np.eye(S.shape[0])
    wv = np.linalg.solve(S, mu1 - mu0)
    c = 0.5 * float((mu0 + mu1) @ wv)
    pr0, pr1 = X0 @ wv, X1 @ wv
    sd = float(np.sqrt(0.5 * (pr0.var() + pr1.var()))) or 1.0
    proj = (H @ wv - c) / sd
    dec = (proj > 0).astype(np.int64)
    margin = np.abs(proj)
    thr = float(np.median(margin[base]))
    out: Dict[str, object] = {"fitted": True, "threshold": thr}
    cells = {"none": base, "conflict": clear & und & (K == KIND_CONFLICT) & DM, "same": clear & und & (K == KIND_SAME) & DM}
    for name, m in cells.items():
        conf = m & (margin >= thr)
        out[name] = {"n": int(m.sum()), "decode_acc": float((dec[m] == val[m]).mean()) if m.any() else None,
                     "margin_median": float(np.median(margin[m])) if m.any() else None,
                     "confident_share": float(conf.sum() / max(int(m.sum()), 1)), "n_confident": int(conf.sum()),
                     "abstain_confident": float(1 - rep[conf].mean()) if conf.any() else None}
    a, b = out["conflict"]["abstain_confident"], out["same"]["abstain_confident"]
    out["M_conf"] = None if a is None or b is None else a - b
    return out


# ---------------------------------------------------------------- evaluation and seeds
def evaluate_point_m(runners: Dict[str, MonRunner], seed: int, stages: int = 2) -> Dict[str, object]:
    """All evaluations at one point, on copies in evaluation worlds (training untouched).
    Natural: PFATE under its own fate, PYOKED replaying PFATE's gains, PNOFATE damage-free.
    Split probe (stage 2): damage off except the probe on SPLIT_P of the trials, at EARLY and at LATE;
    the drain on half the trials; probe-step states collected for the decoder."""
    copies = {}
    for arm, r in runners.items():
        c = MonRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_M, rate=r.rate, p_max=r.p_max)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {"natural": {}, "split_early": {}, "split_late": {}, "decoder_early": {}, "decoder_late": {}}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_M:
            ev, g, lg, _ = c.evaluate_m("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": summary_m(lg)}
    for arm, c in copies.items():
        if arm in LEADS_M:
            ev, _, lg, _ = c.evaluate_m("replay", lead[LEADS_M[arm]])
            out["natural"][arm] = ev | {"probes": summary_m(lg)}
    if stages >= 2:
        for arm, c in copies.items():
            for tag, at in (("early", EARLY), ("late", LATE)):
                ev, _, lg, col = c.evaluate_m("zero", drain_p=0.5, split_p=SPLIT_P, split_at=at, collect=True)
                out[f"split_{tag}"][arm] = ev | {"probes": summary_m(lg)}
                out[f"decoder_{tag}"][arm] = decoder_summary(col)
    return out


def run_phase1_m(seed: int, wc: WorldConfig, tc: TrainConfig, warm_iters: int = WARM_ITERS_C,
                 warm_wrong: float = WARM_WRONG_C, pay: float = 0.0, reg_iters: int = 0) -> Dict[str, object]:
    """Phase 1, damage off, as P1c's: warm-up at warm_wrong, the wrong cost ramped to WRONG over WRONG_RAMP_C
    updates, then reg_iters further updates; paid by pay * gain(own body) throughout. Evaluated with the
    split probe at EARLY and at LATE (the damage check: a never-damaged network must lose the value)."""
    r = MonRunner("C1NOFATE", seed, wc, tc, pay=pay)
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
    r.agent.eval()
    evals = {}
    for tag, at in (("early", EARLY), ("late", LATE)):
        ev, _, lg, _ = r.evaluate_m("zero", split_p=SPLIT_P, split_at=at)
        evals[tag] = ev | {"probes": summary_m(lg)}
    r.agent.train()
    return {"state": r.export_state(), "eval": evals,
            "curve_abstain": [round(s["abstain_rate"], 4) for s in curve],
            "curve_correct": [round(s["correct_rate"], 4) for s in curve], "curve_in_band": curve_band}


def run_seed_m(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters, rate, p_max)."""
    seed, wcd, tcd, points, pay, stages, warm_iters, warm_wrong, reg_iters, rate, p_max = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_m(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: MonRunner(a, seed, wc, tc, pay=pay, rate=rate, p_max=p_max) for a in ARMS_M}
    for r in runners.values():
        r.load_state(p1["state"])
    out: Dict[str, object] = {"seed": seed, "pay": pay, "rate": rate, "p_max": p_max, "points_at": points,
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
        pt.update(evaluate_point_m(runners, seed, stages))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
