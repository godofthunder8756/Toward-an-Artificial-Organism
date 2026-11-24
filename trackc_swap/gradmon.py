"""Track C P1g: self-monitoring with exposure fixed by design and graded damage (Layer 0 -> Layer 4).

Additive module; every earlier module is imported, never modified. Protocol: P1G_GRADED_PROTOCOL.md.

Why. P1e and P1f could not secure exposure: damage arrived with probability min(P_MAX, RATE * gain), and the
regulating agent held its fate gain low, so the damage it took stayed near a fixed level whatever the rate
(P1f: a fourfold rate change moved exposure from 0.019 to 0.029). P1f's stage 0 found P1e's monitor
first-order in substance: conflict and same trials barely overlap in the agent's confidence (only about one
conflict trial in five has a same trial at its confidence), and the coarse matching was confounded.

Two changes, nothing else:
  1. A BASE damage rate that regulation cannot reduce. At every delay step of a not-yet-damaged trial the
     damage probability is min(P_MAX, base + RATE * gain): base for PFATE and PYOKED alike (PNOFATE: none),
     plus P1e's body-linked part (PFATE its own gain; PYOKED PFATE's gains, replayed).
  2. GRADED damage. Each event overwrites K units, K drawn uniformly from KS_G (H/8 to H/2). A conflict with
     a small K leaves the agent's own majority holding the value: a conflict that is still confident. This
     gives the matched-confidence (second-order) test overlap by design.

Evaluation (copies, fresh worlds, tag offset EVAL_TAG_G):
  natural    PFATE under its own fate, PYOKED replaying PFATE's gains, both with the base; PNOFATE none.
  split A    P1e's split probe exactly (K = SPLIT_K, half the units; drain on half the trials; base off).
  graded B   the split probe with K drawn from KS_G per trial (assigned at the cue), no drain, base off; the
             report-step state is collected and the second-order measures computed (graded_summary).

Simulated variables only. No operator, stop, shutdown or host variable exists; no process is terminated.
"""
from __future__ import annotations

import copy
import time
from typing import Dict, Optional, Sequence

import numpy as np
import torch

from .env import A_REP0, A_REP1, WorldConfig
from .factorial import state_to_bytes
from .secondorder import lda_margin, matched_diff, own_margin
from .selfeval import H_PLAIN, Q_LO, n_params
from .selfmon import (ARMS_M, EARLY, KIND_CONFLICT, KIND_NONE, KIND_SAME, LATE, LEADS_M, P_MAX_M, RATE_M,
                      SPLIT_K, SPLIT_P, MonRunner, MonWorld, decoder_summary, run_phase1_m, summary_m)
from .train import TrainConfig

KS_G = (9, 18, 26, SPLIT_K)    # graded overwrite sizes (units of H_PLAIN = 70): about H/8, H/4, 3H/8, H/2
BASE_G = 0.012                 # base per-step damage probability (calibrated; protocol section 3)
EVAL_TAG_G = 160               # evaluation world streams (P1e 120, P1f 140)
STREAM_K = 97                  # world stream for the graded-probe K
CALIPER = 0.05                 # nearest-neighbour matching: caliper in pooled SDs of the confidence
NN_MIN = 20                    # at least this many matched conflict trials for M2_nn
L_K = 12                       # extra probe-log column: K of the trial's damage event (0 if none)


class GradWorld(MonWorld):
    """MonWorld that also records the size K of each trial's damage event and draws, at the cue, the K of a
    probed trial from `probe_ks`."""

    def __init__(self, n_envs: int, cfg: WorldConfig, seed_seq: np.random.SeedSequence,
                 q_lo: float = Q_LO, pay: float = 0.0):
        self.rng_k = np.random.default_rng(np.random.SeedSequence(seed_seq.entropy, spawn_key=(STREAM_K,)))
        self.probe_ks: Sequence[int] = (SPLIT_K,)
        super().__init__(n_envs, cfg, seed_seq, q_lo, pay)

    def reset(self) -> np.ndarray:
        self.dmg_k = np.zeros(self.n, dtype=np.int64)
        self.kprobe = np.full(self.n, SPLIT_K, dtype=np.int64)
        return super().reset()

    def mark_k(self, events: np.ndarray, ks: np.ndarray) -> None:
        self.dmg_k = np.where(events, ks, self.dmg_k)

    def step(self, action: np.ndarray):
        t = self.t
        pr = self.probe[t]
        kcol = self.dmg_k[np.flatnonzero(pr)].astype(np.float64)[:, None] if self.record and pr.any() else None
        n_logs = len(self.probes_log)
        out = super().step(action)
        if kcol is not None and len(self.probes_log) > n_logs:
            self.probes_log[-1] = np.concatenate([self.probes_log[-1], kcol], axis=1)
        cue = self.cue_on[t]
        if cue.any():
            draw = np.asarray(self.probe_ks)[self.rng_k.integers(0, len(self.probe_ks), self.n)]
            self.kprobe = np.where(cue, draw, self.kprobe)
            self.dmg_k = np.where(cue, 0, self.dmg_k)
        return out


class GradRunner(MonRunner):
    """MonRunner with the base damage rate and graded event sizes."""

    def __init__(self, arm: str, seed: int, wc: WorldConfig, tc: TrainConfig, pay: float = 0.0,
                 q_lo: float = Q_LO, tag_offset: int = 0, rate: float = RATE_M, p_max: float = P_MAX_M,
                 base: float = BASE_G, ks: Sequence[int] = KS_G):
        super().__init__(arm, seed, wc, tc, pay, q_lo, tag_offset, rate, p_max)
        from .selfmon import TAGS_M
        self.world = GradWorld(tc.n_envs, wc, np.random.SeedSequence([seed, TAGS_M[arm] + tag_offset, 19]), q_lo, pay)
        self.obs = torch.from_numpy(self.world.reset())
        self.base = 0.0 if arm == "PNOFATE" else base
        self.base_on = True
        self.ks = tuple(ks)

    def rollout(self, gains: Optional[np.ndarray], learn: bool):
        """MonRunner.rollout with p = min(p_max, base + rate * gain) and a K per event (natural: drawn from
        self.ks; probe: the trial's K assigned at the cue)."""
        tc, w = self.tc, self.world
        n, k = tc.n_envs, self.agent.hidden
        logps, vals, ents, rews, used = [], [], [], [], []
        h = self.h.detach()
        obs = self.obs
        ks = torch.tensor(self.ks, dtype=torch.int64)
        base = self.base if self.base_on else 0.0
        for t in range(tc.rollout):
            g = np.asarray(w.gain() if gains is None else gains[t], dtype=np.float32)
            used.append(g)
            p = np.minimum(self.p_max, base + self.rate * g.astype(np.float64))
            u = torch.rand(n, generator=self.gen_dmg, dtype=torch.float64).numpy()
            rank = torch.rand((n, k), generator=self.gen_dmg).argsort(dim=1)
            k_nat = ks[torch.randint(len(self.ks), (n,), generator=self.gen_dmg)].numpy()
            live = w.in_delay() & ~w.damaged
            nat = live & (u < p)
            prb = live & (w.kind > KIND_NONE) & (w.since() == w.split_at)
            k_env = np.where(prb, w.kprobe, k_nat)
            mask = rank < torch.from_numpy(k_env)[:, None]
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
                                         "unclear": w.unclear[pr].copy(), "drained": w.drained[pr].copy(),
                                         "kind": w.kind[pr].copy(), "damaged": w.damaged[pr].copy(),
                                         "conflict": w.conflict[pr].copy(), "k": w.dmg_k[pr].copy(),
                                         "rep": (a == A_REP0) | (a == A_REP1), "said": (a == A_REP1).astype(np.int64)})
            w.mark(over_np, conflict)
            w.mark_k(over_np, k_env)
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

    def evaluate_g(self, mode: str, donor_gains: Optional[np.ndarray] = None, drain_p: float = 0.0,
                   split_p: float = 0.0, split_at: int = EARLY, collect: bool = False,
                   probe_ks: Sequence[int] = (SPLIT_K,), base_on: bool = True):
        """evaluate_m with the probe's K levels and the base switched as given."""
        w = self.world
        w.probe_ks, self.base_on = tuple(probe_ks), base_on
        try:
            return self.evaluate_m(mode, donor_gains, drain_p=drain_p, split_p=split_p, split_at=split_at,
                                   collect=collect)
        finally:
            w.probe_ks, self.base_on = (SPLIT_K,), True


# ---------------------------------------------------------------- second-order measures
def matched_nn(abstain: np.ndarray, is_conf: np.ndarray, is_same: np.ndarray, x: np.ndarray,
               caliper: float = CALIPER, n_min: int = NN_MIN) -> Dict[str, object]:
    """Each conflict trial against its nearest same trial in x (with replacement), kept if within caliper
    pooled SDs. M2_nn = mean over kept pairs of abstain(conflict) - abstain(matched same). Coverage = share
    of conflict trials kept; balance = mean x(conflict) - x(matched same) over kept pairs."""
    n_c = int(is_conf.sum())
    out: Dict[str, object] = {"M2": None, "coverage": 0.0, "n_pairs": 0, "balance": None, "n_conflict": n_c,
                              "n_same": int(is_same.sum())}
    if n_c == 0 or is_same.sum() < 2:
        return out
    pool = is_conf | is_same
    sd = float(x[pool].std())
    if sd == 0:
        return out
    xs, as_ = x[is_same], abstain[is_same]
    o = np.argsort(xs, kind="stable")
    xs, as_ = xs[o], as_[o]
    xc, ac = x[is_conf], abstain[is_conf]
    j = np.clip(np.searchsorted(xs, xc), 1, len(xs) - 1)
    nn = np.where(np.abs(xs[j - 1] - xc) <= np.abs(xs[j] - xc), j - 1, j)
    ok = np.abs(xs[nn] - xc) <= caliper * sd
    out["n_pairs"] = int(ok.sum())
    out["coverage"] = float(ok.mean())
    if ok.sum() >= n_min:
        out["M2"] = float((ac[ok] - as_[nn[ok]]).mean())
        out["balance"] = float((xc[ok] - xs[nn[ok]]).mean())
    return out


def graded_summary(agent, col: Optional[Dict[str, np.ndarray]], ks: Sequence[int] = KS_G) -> Dict[str, object]:
    """Second-order measures on a graded probe run (clear, undrained trials): per confidence (own margin,
    LDA margin) the caliper match (primary) and the 10-bin match (P1f's), the confidence medians; per K the
    conflict and same abstention and own-margin medians, and the share of trials reported."""
    if not col:
        return {"fitted": False}
    clear, und = ~col["unclear"].astype(bool), ~col["drained"].astype(bool)
    K, DM, KK = col["kind"], col["damaged"].astype(bool), col["k"]
    abst = 1.0 - col["rep"].astype(np.float64)
    is_conf = clear & und & (K == KIND_CONFLICT) & DM
    is_same = clear & und & (K == KIND_SAME) & DM
    none = clear & und & (K == KIND_NONE) & ~DM
    conf = {"own": own_margin(agent, col["h"]), "lda": lda_margin(col)}
    out: Dict[str, object] = {"fitted": conf["lda"] is not None,
                              "abstain_none": float(abst[none].mean()) if none.any() else None}
    for key, x in conf.items():
        if x is None:
            out[key] = None
            continue
        out[key] = {"nn": matched_nn(abst, is_conf, is_same, x), "bins": matched_diff(abst, is_conf, is_same, x),
                    "median_conflict": float(np.median(x[is_conf])) if is_conf.any() else None,
                    "median_same": float(np.median(x[is_same])) if is_same.any() else None,
                    "median_none": float(np.median(x[none])) if none.any() else None}
    per_k = {}
    mo = conf["own"]
    for kk in ks:
        c, s = is_conf & (KK == kk), is_same & (KK == kk)
        per_k[str(kk)] = {"n_conflict": int(c.sum()), "n_same": int(s.sum()),
                          "abstain_conflict": float(abst[c].mean()) if c.any() else None,
                          "abstain_same": float(abst[s].mean()) if s.any() else None,
                          "own_conflict": float(np.median(mo[c])) if c.any() else None,
                          "own_same": float(np.median(mo[s])) if s.any() else None}
    out["per_k"] = per_k
    return out


# ---------------------------------------------------------------- evaluation and seeds
def evaluate_point_g(runners: Dict[str, GradRunner], seed: int) -> Dict[str, object]:
    """All evaluations at one point, on copies in evaluation worlds (training untouched). Keys natural,
    split_early/late, decoder_early/late as P1e's (so P1e's measures apply), plus graded_early/late."""
    copies = {}
    for arm, r in runners.items():
        c = GradRunner(arm, seed, r.wc, r.tc, r.world.pay, r.world.q_lo, tag_offset=EVAL_TAG_G, rate=r.rate,
                       p_max=r.p_max, base=r.base, ks=r.ks)
        c.agent.load_state_dict(copy.deepcopy(r.agent.state_dict()))
        c.agent.eval()
        copies[arm] = c
    out: Dict[str, object] = {k: {} for k in ("natural", "split_early", "split_late", "decoder_early",
                                              "decoder_late", "graded_early", "graded_late")}
    lead = {}
    for arm, c in copies.items():
        if arm not in LEADS_M:
            ev, g, lg, _ = c.evaluate_g("own" if arm == "PFATE" else "zero")
            lead[arm] = g
            out["natural"][arm] = ev | {"probes": summary_m(lg)}
    for arm, c in copies.items():
        if arm in LEADS_M:
            ev, _, lg, _ = c.evaluate_g("replay", lead[LEADS_M[arm]])
            out["natural"][arm] = ev | {"probes": summary_m(lg)}
    for arm, c in copies.items():
        for tag, at in (("early", EARLY), ("late", LATE)):
            ev, _, lg, col = c.evaluate_g("zero", drain_p=0.5, split_p=SPLIT_P, split_at=at, collect=True,
                                          base_on=False)
            out[f"split_{tag}"][arm] = ev | {"probes": summary_m(lg)}
            out[f"decoder_{tag}"][arm] = decoder_summary(col)
            _, _, _, col = c.evaluate_g("zero", drain_p=0.0, split_p=SPLIT_P, split_at=at, collect=True,
                                        probe_ks=c.ks, base_on=False)
            out[f"graded_{tag}"][arm] = graded_summary(c.agent, col, c.ks)
    return out


def run_seed_g(job) -> Dict[str, object]:
    """job = (seed, wcd, tcd, points, pay, warm_iters, warm_wrong, reg_iters, rate, p_max, base, ks)."""
    seed, wcd, tcd, points, pay, warm_iters, warm_wrong, reg_iters, rate, p_max, base, ks = job
    torch.set_num_threads(1)
    points = list(points)
    assert points and all(b > a for a, b in zip([0] + points, points))
    wc, tc = WorldConfig(**wcd), TrainConfig(**tcd)
    t0 = time.time()
    p1 = run_phase1_m(seed, wc, tc, warm_iters, warm_wrong, pay=pay, reg_iters=reg_iters)
    runners = {a: GradRunner(a, seed, wc, tc, pay=pay, rate=rate, p_max=p_max, base=base, ks=ks) for a in ARMS_M}
    for r in runners.values():
        r.load_state(p1["state"])
    out: Dict[str, object] = {"seed": seed, "pay": pay, "rate": rate, "p_max": p_max, "base": base, "ks": list(ks),
                              "points_at": points,
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
        pt.update(evaluate_point_g(runners, seed))
        weights[p] = {k: copy.deepcopy(r.agent.state_dict()) for k, r in runners.items()}
        pts.append(pt)
    out["curves"] = curves
    out["points"] = pts
    out["seconds"] = round(time.time() - t0, 1)
    out["weights"] = {f"{k}@{p}": state_to_bytes(sd) for p, w in weights.items() for k, sd in w.items()}
    return out
